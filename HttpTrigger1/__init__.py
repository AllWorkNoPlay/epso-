import logging

import azure.functions as func
import azure.cosmos

import requests
from bs4 import BeautifulSoup
import os
import glob

settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://wr-epso.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', '2QSLJRiHCarFJm5duZaoXhxS4fNdrP641IUyQnAbPkc4mwBGktvEvmOMWAuXnZ25S00bZMoyJ09kACDbfRLaQQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'wr-epso'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'jobs'),
}

HOST = settings['host']
MASTER_KEY = settings['master_key']
DATABASE_ID = settings['database_id']
CONTAINER_ID = settings['container_id']

class JobRow:
    def __init__(self, soup):
        self.soup = soup

    def find_value(self, tag, class_name):
        element = self.soup.find(tag, class_=class_name, default=None)
        if element:
            subelement = element.find(class_='field-content')
            return subelement.text
        else:
            return None

    @property
    def title(self):
        return self.find_value('span', 'views-field-title')

    @property
    def grade(self):
        return self.find_value('span', 'views-field-field-epso-grade')

    @property
    def domain(self):
        return self.find_value('div', 'views-field-field-epso-domain')

    @property
    def institution(self):
        return self.find_value('span', 'views-field-field-epso-institution')

    @property
    def location(self):
        return self.find_value('span', 'views-field-field-epso-location')

    @property
    def deadline(self):
        return self.find_value('span', 'views-field-field-epso-deadline')


def scrape_table(url, page=1):
    # Send an HTTP GET request to the URL of the page
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')

    
    
    
    # Returns a list of names in list files.
    print("Using glob.glob()")
    files = glob.glob('**/page1.html', 
                    recursive = True)
    
    assert len(files) == 1

    with open(files[0], 'r', encoding="utf8") as f:
        html_content = f.read()

    # Parse the response as HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the job-row items on the page
    job_rows = soup.find_all('div', class_='job-row')

    # Create a list to store the scraped data
    data = []

    # Iterate over the job-row items
    for job_row in job_rows:
        # Create a JobRow object for the job-row item
        job_row_obj = JobRow(job_row)

        # Extract the desired information from the JobRow object
        title = job_row_obj.title
        grade = job_row_obj.grade
        domain = job_row_obj.domain
        institution = job_row_obj.institution
        location = job_row_obj.location
        deadline = job_row_obj.deadline

        # Store the extracted data in a dictionary
        job_data = {
            'title': title,
            'grade': grade,
            'domain': domain,
            'institution': institution,
            'location': location,
            'deadline': deadline
        }

        # Add the dictionary to the list of data
        data.append(job_data)

    # Find the next li element in nav
    next_li = soup.find('li', class_='ecl-pagination__item--next')
    next_url = next_li.find('a').attrs['href']

    # If the next li was found, scrape the next page
    # if next_li:
    #     next_page = page + 1
    #     data.extend(scrape_table(next_url, page=next_page))

    return data

def update_db(job_rows):
    # Connect to the Cosmos DB account
    client = azure.cosmos.CosmosClient(url_connection=HOST, auth={
        'masterKey': MASTER_KEY
    })

    # Get the database and collection
    database = client.get_database_client(DATABASE_ID)
    container = database.get_container_client(CONTAINER_ID)


    # Iterate over the job-row items
    for job_row in job_rows:
        # Create a JobRow object for the job-row item
        job_row_obj = JobRow(job_row)

        # Extract the desired information from the JobRow object
        title = job_row_obj.title
        domain = job_row_obj.domain
        institution = job_row_obj.institution
        location = job_row_obj.location
        deadline = job_row_obj.deadline

        # Create a dictionary to store the data
        data = {
            'title': title,
            'domain': domain,
            'institution': institution,
            'location': location,
            'deadline': deadline
        }

        # Upsert the data into the Cosmos DB collection
        container.create_item(data, if_exists='replace')

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Set the URL of the page to scrape
    url = 'https://epso.europa.eu/en/job-opportunities/open-for-application'

    # Scrape the table
    job_rows = scrape_table(url)

    return 'Scrape complete!'
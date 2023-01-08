import time
from bs4 import BeautifulSoup
import os
import glob
import requests
from urllib.parse import urldefrag, urljoin

from HttpTrigger1.jobrow import JobRow

# TODO: FIX Does not read the grade 

class MyScraper0:
    def __init__(self):
        self.data = []


    def scrape(self, url, page=1):
        # Send an HTTP GET request to the URL of the page
        response = requests.get(url)
        
        # Parse the response as HTML
        soup = BeautifulSoup(response.content, 'html.parser')

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

        # If the next li was found, scrape the next page
        if next_li:
            next_url = next_li.find('a').attrs['href']
            next_page = page + 1
            base_url, fragment = urldefrag(url)
            absolute_next_url = urljoin(base_url, next_url)
            time.sleep(1)
            data.extend(self.scrape(absolute_next_url, page=next_page))

        return data


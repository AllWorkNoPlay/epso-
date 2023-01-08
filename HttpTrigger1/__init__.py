import logging
import azure.functions as func

from HttpTrigger1.scraper import MyScraper
from HttpTrigger1.scraper_0 import MyScraper0



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Set the URL of the page to scrape
    url = 'https://epso.europa.eu/en/job-opportunities/open-for-application'

    # scraper = MyScraper0()
    scraper = MyScraper()

    data = scraper.scrape(url)


    return 'Scrape complete!'
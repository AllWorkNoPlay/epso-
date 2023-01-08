import json
import logging
import azure.functions as func

from HttpTrigger1.scraper import scraper
from HttpTrigger1.blobstorage import blobstorage


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Set the URL of the page to scrape
    url = 'https://epso.europa.eu/en/job-opportunities/open-for-application'

    # scraper = MyScraper0()
    my_scraper = scraper()

    data = my_scraper.scrape(url)

    logging.info('Job data scraped from web.')

    json_string = json.dumps([d.__dict__ for d in data])

    my_blobstorage = blobstorage()
    my_blobstorage.store(json_string)

    logging.info('Job data stored in azure blob.')


    return 'Scrape complete!'
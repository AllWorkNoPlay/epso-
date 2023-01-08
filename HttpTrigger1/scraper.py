from bs4 import BeautifulSoup
import requests
from urllib.parse import urldefrag, urljoin

from HttpTrigger1.tableitem import TableItem

class MyScraper:
    def __init__(self):
        self.data = []


    def scrape(self, url, page=1):
          # Send an HTTP GET request to the URL of the page
        response = requests.get(url)
        
        # Parse the response as HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all tables with class "cols-6"
        tables = soup.find_all('table', class_='cols-6')

        # Extract the data from each table and store it in a list of TableItem instances
        data = []
        for table in tables:

            # Find the table caption
            captionelement = table.find('caption')
            if (captionelement):
                caption = captionelement.text.strip()
            else:
                caption = 'None'

            # Find all table rows
            rows = table.find_all('tr')

            # Extract the data from each row and store it in a list of TableItem instances
            # data = []
            for row in rows:
                cells = row.find_all('td')
                if cells:
                    # Extract the data from each cell and store it in a TableItem instance
                    item = TableItem(
                        job_title=cells[0].text.strip(),
                        domains=cells[1].text.strip(),
                        grade=cells[2].text.strip(),
                        institution=cells[3].text.strip(),
                        location=cells[4].text.strip(),
                        deadline=cells[5].text.strip(),
                        caption=caption
                    )
                    data.append(item)

        # Find the next li element in nav
        next_li = soup.find('li', class_='ecl-pagination__item--next')

        # If the next li was found, scrape the next page
        if next_li:
            next_url = next_li.find('a').attrs['href']
            next_page = page + 1
            base_url, fragment = urldefrag(url)
            absolute_next_url = urljoin(base_url, next_url)
            data.extend(self.scrape(absolute_next_url, page=next_page))

        return data

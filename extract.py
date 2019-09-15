import requests
import urllib
import pandas as pd
from bs4 import BeautifulSoup

class HTMLTableParser:
    
    def parse_url(self, url):
        #Store the contents of the website under doc
        response = requests.get(url)
        #Parse data that are stored between <tr>..</tr> of HTML
        soup = BeautifulSoup(response.text, 'lxml') # Parse the HTML as a string 
        tables = soup.find_all('table', {'class': 'wikitable'})
        return tables

    def parse_html_table(self, table):
        n_columns = 0
        n_rows=0
        first = True
        # Find number of rows and columns
        # we also find the column titles if we can
        rows = table.find_all('tr')
        for row in rows:
            if first:
                cols_names = row.find_all('th')
                first = False
            else:
                cols = row.find_all('td')


            
url = 'https://stardewvalleywiki.com/Crops'
hp = HTMLTableParser()
tables = hp.parse_url(url) # Grabbing the table from the tuple
hp.parse_html_table(tables[2])
print(tables[2])
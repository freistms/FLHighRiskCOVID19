from bs4 import BeautifulSoup
import requests
import sqlite3
import logging

WIKI_FL_COUNTY_DATA = 'https://en.wikipedia.org/wiki/List_of_counties_in_Florida'

def harvest():
    logging.info('**** Gathering county data')

    # Retrieve and parse page using beautiful soup
    counties_page = requests.get(WIKI_FL_COUNTY_DATA)
    counties_page_soup = BeautifulSoup(counties_page.content, 'html.parser')

    rows = counties_page_soup.select('table.wikitable.sortable tbody tr')
    for row in rows:
        try:
            county_name = row.find('th').get_text().lower().replace('county', '').strip()
            logging.debug("Processing County: {0}".format(county_name))

            # Parse Table Values
            data_vals = row.select('td')
            seat = data_vals[1].get_text().lower()
            density = float(data_vals[5].get_text().strip())
            population = int(data_vals[6].get_text().strip().replace(',',''))
            area = data_vals[7].get_text()
            area = int(area.split()[0].replace(',', ''))

            # Stoe value in SQL
            store_value(county_name, seat, density, population, area)
        except Exception as e:
            pass


def store_value(name, seat, density, population, area):
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    cur.execute('''INSERT OR REPLACE INTO Counties
                     (name, seat, density, population, area_sq_mi) 
                     VALUES ( ?, ?, ?, ?, ? )''',
                     (name, seat, density, population, area) )
    conn.commit()
    cur.close()
    conn.close()

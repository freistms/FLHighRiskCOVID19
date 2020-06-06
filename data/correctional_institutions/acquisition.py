from bs4 import BeautifulSoup
import requests
import googlemaps
import sqlite3
import logging


FLORIDA_INSTITUTION_INDEX = 'http://www.dc.state.fl.us/ci/index.html'
FLORIDA_INSTITUTION_INST = 'http://www.dc.state.fl.us/ci/{0}'

def harvest(api_key=None):
    logging.info('**** Gathering institution data')

    # Retrieve and parse page using beautiful soup
    index_page = requests.get(FLORIDA_INSTITUTION_INDEX)
    index_page_soup = BeautifulSoup(index_page.content, 'html.parser')

    # Google Maps API Setup
    google_maps = googlemaps.Client(key=api_key)

    # Get anchor tags at a spot that looks like ours.  Still getting some fluf but it looks like I can prune them out
    #   by removing those that have a forward slash in their href.  Build a list of instituions and their links.
    #   I also don't think we want offices
    institutions = []
    anchor_tags = index_page_soup.select('div[aria-label="Institution Navigation"] ul li ul.menu li a')
    for anchor_tag in anchor_tags:
        href = anchor_tag['href']
        text = anchor_tag.get_text()
        if '/' not in href and 'office' not in text.lower():
            institutions.append(((href, text)))

    # For each institution, retrieve its page and get desired details
    for institution in institutions:
        logging.debug('Processing Institution: {0}'.format(institution[1]))

        address = county_name = capacity = gender = age = ''

        institution_page = requests.get(FLORIDA_INSTITUTION_INST.format(institution[0]))
        institution_page_soup = BeautifulSoup(institution_page.content, 'html.parser')

        # Get address and clean
        address_soup = institution_page_soup.select('div.facAddress')
        address_pieces = []
        for possible_piece in address_soup[0].get_text().replace('Address', '').strip().splitlines():
            if 'mailing' in possible_piece.lower():
                break
            possible_piece_stripped = possible_piece.strip()
            if possible_piece_stripped:
                address_pieces.append(possible_piece_stripped)
        address = ' '.join(address_pieces)

        # Get county from google maps geocode API.  Code modified from stack overflow.
        try:
            location = google_maps.geocode(address)
            target_string = 'administrative_area_level_2'
            for item in location[0]['address_components']:
                if target_string in item['types']:
                    county_name = item['long_name'].lower().replace('county', '').strip()
                    break
                else:
                    pass
        except:
            # Handle cases we have found manually - log error if new
            if '3420 N.E. 168th Street Okeechobee, Florida 34972-4824' in address:
                county_name = 'okeechobee'
            else:
                logging.warning('Unable to determine county for {0} - {1}'.format(institution[1], address))
                county_name = None

        # Get remaining values from table on page
        general_info_trs = institution_page_soup.select('table.dcCSStableAlias tr')
        try:
            for general_info_tr in general_info_trs:
                th = general_info_tr.find('th').get_text()
                if 'capacity' in th.lower():
                    capacity = int(general_info_tr.find('td').get_text().split()[0].replace(',',''))
                if 'gender' in th.lower():
                    gender = general_info_tr.find('td').get_text()
                if 'adult' in th.lower():
                    age = general_info_tr.find('td').get_text()
        except:
            logging.warning('Unable to include {0} due to invalid chart data'.format(institution[1]))
            continue

        # Store record in SQL DB
        store_value(institution[1], FLORIDA_INSTITUTION_INST.format(institution[0]), address, county_name, capacity, gender, age)


def store_value(name, url, address, county, capacity, gender, age):
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    if county:
        cur.execute('SELECT id FROM Counties WHERE name = ? ', (county, ))
        county_id = cur.fetchone()[0]
    else:
        county_id = None

    cur.execute('''INSERT OR REPLACE INTO CorrectionalInstitutions
                     (name, url, address, to_county, capacity, gender, age)
                     VALUES ( ?, ?, ?, ?, ?, ?, ? )''',
                     (name, url, address, county_id, capacity, gender, age) )
    conn.commit()
    cur.close()
    conn.close()

# csv file generated from https://www.floridahealthfinder.gov/facilitylocator/FacilitySearch.aspx?cc=35
#  Click search, export to excel, place in data folder here

import sqlite3
import logging
import csv

NAME_ROW = 5
STREET_ADDRESS_ROW = 6
STREET_CITY_ROW = 8
STREET_STATE_ROW = 9
STREET_ZIP_ROW = 10
STREET_COUNTY_ROW = 11
BEDS_ROW = 23

def harvest():
    logging.info('**** Gathering nursing home data')

    with open('data/nursing_homes/FloridaHealthFinder-FacilitiesExport.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        nursing_homes = []
        for row in csv_reader:
            if line_count > 0 and len(row) > 5:
                nursing_homes.append(row)
            line_count += 1

    for nursing_home in nursing_homes:
        name = nursing_home[NAME_ROW]
        logging.debug('Processing Nursing Home: {0}'.format(name))
        address = '{0} {1}, {2} {3}'.format(nursing_home[STREET_ADDRESS_ROW], nursing_home[STREET_CITY_ROW], nursing_home[STREET_STATE_ROW], nursing_home[STREET_ZIP_ROW])
        county = nursing_home[STREET_COUNTY_ROW].lower()
        beds = int(nursing_home[BEDS_ROW])
        store_value(name, address, county, beds)


def store_value(name, address, county, beds):
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    if county:
        cur.execute('SELECT id FROM Counties WHERE name = ? ', (county, ))
        county_id = cur.fetchone()[0]
    else:
        logging.warning('County was not found looking up: {0}'.format(county))
        county_id = None

    cur.execute('''INSERT OR REPLACE INTO NursingHomes (name, address, to_county, beds) VALUES ( ?, ?, ?, ?)''',
                     (name, address, county_id,beds) )
    conn.commit()
    cur.close()
    conn.close()

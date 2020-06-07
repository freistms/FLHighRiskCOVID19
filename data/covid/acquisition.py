from bs4 import BeautifulSoup
import requests
import googlemaps
import sqlite3
import logging
import json

COVID_JSON_LOCATION = 'https://opendata.arcgis.com/datasets/a7887f1940b34bf5a02c6f7f27a5cb2c_0.geojson'

def harvest():
    logging.info('**** Gathering covid data by county')
    counties_page = requests.get(COVID_JSON_LOCATION)
    data = json.loads(counties_page.content.decode())

    # Get the feature properteis dictionary from the returned json and remove the columns we will not be storing
    for feature in data['features']:
        properties = feature['properties']
        county = properties['County_1'].lower().replace('dade','miami-dade')
        if county=='unknown':
            county = None

        logging.debug("Processing County: {0}".format(county))
        del properties['FID']
        del properties['OBJECTID_12_13']
        del properties['DEPCODE']
        del properties['COUNTY']
        del properties['COUNTYNAME']
        del properties['County_1']
        del properties['State']
        del properties['Chart_MedAge']
        del properties['SHAPE_Length']
        del properties['SHAPE_Area']
        store_value(county, properties)


def store_value(county, properties):
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    # Look up our county table row reference
    if county:
        cur.execute('SELECT id FROM Counties WHERE name = ? ', (county, ))
        county_id = cur.fetchone()[0]
    else:
        county_id = None

    # This is a little tricky.  For the SQL insert i'm using the keys and values from the feature properties dictionary
    #   to fill out the command.  This works because our DB table has the same column names.  We have to add in the
    #   the foreign key value we calculated to our county table, making it look more complicated heh.
    cur.execute('INSERT OR REPLACE INTO Covid (to_county,' + ','.join(properties.keys()) + ') VALUES (' + ','.join(['?']*(len(properties.keys())+1)) + ')', tuple([county_id] + list(properties.values())))

    conn.commit()
    cur.close()
    conn.close()

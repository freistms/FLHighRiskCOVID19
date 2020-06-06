from bs4 import BeautifulSoup
import requests
import sqlite3
import logging

INST_COVID_URL = 'http://www.dc.state.fl.us/comm/covid-19.html#stats'

TRANSLATIONS = {"CFRC" : "Central Florida Reception Center",
                "FWRC" : "Florida Women's Reception Center",
                "Mayo Annex" : "Mayo",
                "NWFRC" : "Northwest Florida Reception Center",
                "RMC": "Reception and Medical Center",
                "SFRC": "South Florida Reception Center"}

FACILITY_ROW = 0
INMATE_SECURITY_QUARANTNE_ROW = 1
INMATE_MEDICAL_QUARANTNE_ROW = 2
INMATE_MEDICAL_ISOLATION_ROW = 3
INMATE_PENDING_TESTS_ROW = 4
INMATE_NEGATIVE_TESTS_ROW = 5
INMATE_POSITIVE_TESTS_ROW = 6
STAFF_POSITIVE_TESTS_ROW = 7

def harvest():
    logging.info('**** Gathering institution covid data')

    # Retrieve and parse page using beautiful soup
    inst_covid_page = requests.get(INST_COVID_URL)
    inst_cofid_page_soup = BeautifulSoup(inst_covid_page.content, 'html.parser')

    rows = inst_cofid_page_soup.select('table tr')
    for row in rows:
        try:
            cells = row.select('td')
            if len(cells) != 8:
                continue

            # Normalize facility name for lookup
            facility = cells[FACILITY_ROW].get_text().split('Operated')[0].split(' CI')[0].split(' CF')[0].strip()
            facility = TRANSLATIONS.get(facility, facility)
            logging.debug('Processing: {0}'.format(facility))

            if 'Community Corrections Region' in facility or 'Totals' in facility:
                continue

            isq = int(cells[INMATE_SECURITY_QUARANTNE_ROW].get_text().strip())
            imq = int(cells[INMATE_MEDICAL_QUARANTNE_ROW].get_text().strip())
            imi = int(cells[INMATE_MEDICAL_ISOLATION_ROW].get_text().strip())
            ipendt = int(cells[INMATE_PENDING_TESTS_ROW].get_text().strip())
            inegt = int(cells[INMATE_NEGATIVE_TESTS_ROW].get_text().strip())
            ipost = int(cells[INMATE_POSITIVE_TESTS_ROW].get_text().strip())
            spost = int(cells[STAFF_POSITIVE_TESTS_ROW].get_text().strip())

            store_value(facility, isq, imq, imi, ipendt, inegt, ipost, spost)

        except Exception as e:
            logging.warning('Error processing: {0}'.format(facility))


def store_value(facility, isq, imq, imi, ipendt, inegt, ipost, spost):
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    try:
        cur.execute('SELECT id FROM CorrectionalInstitutions WHERE name LIKE ?', ('%' + facility + '%', ))
        facility_id = cur.fetchone()[0]
    except:
        logging.warning('Unable to find in our Correctional Institutional Data: {0}'.format(facility))
        facility_id = None

    cur.execute('''INSERT OR REPLACE INTO CorrectionalInstitutionsCovid
                     (to_correctonal_institution, inmate_security_quarantine, inmate_medical_quarantine, inmate_medical_isolation, inmate_pending_tests, inmate_negative_tests, inmate_positive_tests, staff_positive_tests)
                     VALUES ( ?, ?, ?, ?, ?, ?, ?, ? )''',
                     (facility_id, isq, imq, imi, ipendt, inegt, ipost, spost) )
    conn.commit()
    cur.close()
    conn.close()

import requests
import sqlite3

from pdfminer.high_level import extract_text

DOH_PDF_URL = 'http://ww11.doh.state.fl.us/comm/_partners/action/report_archive/ltcf/ltcf_latest.pdf'

def harvest():

    # Pull down the pdf locally.  Seems easiest way to work with pdf library.  Extract pdf text.
    r = requests.get(DOH_PDF_URL)
    with open("data/covid/doh_pdf.pdf", 'wb') as f:
        f.write(r.content)
    text = extract_text('data/covid/doh_pdf.pdf')

    # The following hacking of this text is based on analysis of an existing response.  Somewhat brittle implementation.
    #   Stuff before 'Faility Name' is junk.  After that I an split on two newlines and get columns.  The first page
    #   has a couple special cases as the numeric columns have totals on top.  We will get all the columns for the page
    #   and then zip the resuls together into tuples, then create sql entries, then on to next page.

    text = text.replace('\xa0', ' ')
    text = text.split('Facility Name')[1]
    columns = text.split('\n\n')

    index = 1
    first_page = True
    for column in columns:

        # Recognize a page start.  At this point we need to process previous page and reset stuffs.
        if index == 8:

            # process last page
            for (county, facility, positive_r, positive_s) in zip(counties, facilities, positive_residents, positive_staff):
                store_value(county, facility, positive_r, positive_s)

            first_page = False
            index = 1
            counties = []
            facilities = []
            positive_residents = []
            positive_staff = []

        # Columns with small number of values look like stuff we do not want.  Hopefully we don't hit a situation with
        #   a small last page (nowhere close right now)

        special_case_twofor = False
        if "Provider Type" in column and "Update Time" in column:
            special_case_twofor = True

        vals = column.split('\n')
        if len(vals) < 5:
            continue

        # Grab columns we care about
        if index % 7 == 1:
            counties = [val.strip().replace('‐','-').lower() for val in vals]
        if index % 7 == 2:
            facilities = [val.strip().lower() for val in vals]
        if index % 7 == 5:
            positive_residents = [int(val.replace(',','').strip()) for val in vals]
            if first_page:
                positive_residents = positive_residents[1:]
        if index % 7 == 0:
            positive_staff = [int(val.replace(',','').strip()) for val in vals]
            if first_page:
                positive_staff = positive_staff[1:]

        index += 1
        if special_case_twofor:
            index += 1

def store_value(county, name, resident_positive, staff_positive):
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    if county:
        cur.execute('SELECT id FROM Counties WHERE name = ? ', (county, ))
        county_id = cur.fetchone()[0]
    else:
        county_id = None

    cur.execute('''INSERT OR REPLACE INTO NursingHomeCovid
                     (to_county, name, resident_positive_tests, staff_positive_tests)
                     VALUES ( ?, ?, ?, ?)''',
                     (county_id, name, resident_positive, staff_positive) )
    conn.commit()
    cur.close()
    conn.close()
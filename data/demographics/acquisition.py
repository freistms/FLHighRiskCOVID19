# Excel file with demographics is from https://www.bebr.ufl.edu/population/data

import sqlite3
import logging
import xlrd

def harvest():
    logging.info('**** Gathering demographics data')
    wb = xlrd.open_workbook("data/demographics/estimates_2019.xlsx")

    # Process under 17 sheet
    sheet = wb.sheet_by_index(12)
    vals = parse_demo_sheet(sheet)
    for (county, percent, number) in vals:
        store_value('FloridaDemographics17AndUnder', county, percent, number)

    # Process over 65 sheet
    sheet = wb.sheet_by_index(13)
    vals = parse_demo_sheet(sheet)
    for (county, percent, number) in vals:
        store_value('FloridaDemographics65AndOver', county, percent, number)

    # Process over Black sheet
    sheet = wb.sheet_by_index(14)
    vals = parse_demo_sheet(sheet)
    for (county, percent, number) in vals:
        store_value('FloridaDemographicsBlack', county, percent, number)

    # Process over Hispanic sheet
    sheet = wb.sheet_by_index(15)
    vals = parse_demo_sheet(sheet)
    for (county, percent, number) in vals:
        store_value('FloridaDemographicsHispanic', county, percent, number)

def parse_demo_sheet(sheet):
    vals = []
    for row in sheet.get_rows():
        try:
            county_num = int(row[0].value)
            county = row[1].value.lower()
            percent = float(row[2].value)
            number = int(float(row[3].value))
            vals.append((county, percent, number))
        except:
            pass

        try:
            county_num = int(row[6].value)
            county = row[7].value.lower()
            percent = float(row[8].value)
            number = int(float(row[9].value))
            vals.append((county, percent, number))
        except:
            pass
    return vals


def store_value(table, county, percent, number):
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    if county:
        cur.execute('SELECT id FROM Counties WHERE name = ? ', (county, ))
        county_id = cur.fetchone()[0]
    else:
        logging.warning('County was not found looking up: {0}'.format(county))
        county_id = None

    cur.execute('''INSERT OR REPLACE INTO {0} (to_county, percent, number) VALUES ( ?, ?, ?)'''.format(table),
                     (county_id, percent, number) )
    conn.commit()
    cur.close()
    conn.close()

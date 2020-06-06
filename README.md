# Florida Dense Vulnerable Population COVID-19 Analysis
An analysis of the impact of nursing homes and correctional institutions on Florida counties

# Environment Requirements
- Python 3
- Virual Environment

# Environment Setup
- Clone repository

# Refreshing Data
This analysis uses data from Wikipedia, the Florida Deaprtment of Corrections, ArcGIS, and the Google GeoCode API, and
Florida Health Finder. There is a database included in this repo with harvested information.  If you would like to 
update to the most current data
- Configure [Google API key](https://developers.google.com/places/web-service/get-api-key) in GOOGLE_API_KEY in refresh_data.py
- Create a new nursing home csv by going [here](https://www.floridahealthfinder.gov/facilitylocator/FacilitySearch.aspx?cc=35), clicking search, export to excel, place file in data/nursing_homes/
- cd into project root directory
- Execute refresh_data.py 

# Running Analysys
- cd into project root directory
- Execute analysis.py
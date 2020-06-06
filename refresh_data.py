import logging

from data.database import db
from data.correctional_institutions import  acquisition as correctional_institutions_acquisition
from data.counties import acquisition as counties_acquisition
from data.covid import acquisition as covid_acquisition
from data.nursing_homes import acquisition as nursing_home_acquisition
from data.covid import acquisition_ci_specific as covid_ci_acquisition

LOGGING_LEVEL = logging.DEBUG
GOOGLE_API_KEY = 'AIzaSyBUylmCwdPG3gRlBIVwq0aDVZI8OYGWNak'

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    db.drop_tables()

    db.init_county_database()
    counties_acquisition.harvest()

    db.init_institution_database()
    correctional_institutions_acquisition.harvest(api_key=GOOGLE_API_KEY)

    db.init_covid_database()
    covid_acquisition.harvest()

    db.init_nursing_home_database()
    nursing_home_acquisition.harvest()

    db.init_institution_covid_database()
    covid_ci_acquisition.harvest()
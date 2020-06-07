import sqlite3

def drop_tables():
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()
    cur.executescript('''
        DROP TABLE IF EXISTS FloridaDemographicsHispanic;
        DROP TABLE IF EXISTS FloridaDemographicsBlack;
        DROP TABLE IF EXISTS FloridaDemographics65AndOver;
        DROP TABLE IF EXISTS FloridaDemographics17AndUnder;
        DROP TABLE IF EXISTS NursingHomeCovid;
        DROP TABLE IF EXISTS CorrectionalInstitutionsCovid;
        DROP TABLE IF EXISTS NursingHomes;
        DROP TABLE IF EXISTS CorrectionalInstitutions;
        DROP TABLE IF EXISTS Covid;
        DROP TABLE IF EXISTS Counties; ''')
    cur.close()
    conn.close()


def init_county_database():
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS Counties;

        CREATE TABLE Counties (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT UNIQUE,
            seat TEXT,
            density REAL,
            population INTEGER,
            area_sq_mi INTEGER
        ); ''')

    cur.close()
    conn.close()

def init_institution_database():
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS CorrectionalInstitutions;

        CREATE TABLE CorrectionalInstitutions (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            to_county INTEGER,
            name TEXT UNIQUE,
            url TEXT UNIQUE,
            address TEXT,
            capacity INTEGER,
            gender TEXT,
            age TEXT,
            FOREIGN KEY(to_county) REFERENCES Counties(id)
        ); ''')

    cur.close()
    conn.close()

def init_covid_database():
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS Covid;

        CREATE TABLE Covid (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            to_county INTEGER,
            PUIsTotal INTEGER,
            Age_0_4 INTEGER,
            Age_5_14 INTEGER,
            Age_15_24 INTEGER,
            Age_25_34 INTEGER,
            Age_35_44 INTEGER,
            Age_45_54 INTEGER,
            Age_55_64 INTEGER,
            Age_65_74 INTEGER,
            Age_75_84 INTEGER,
            Age_85plus INTEGER,
            Age_Unkn INTEGER,
            PUIAgeRange TEXT,
            PUIAgeMedian INTEGER,
            PUIFemale INTEGER,
            PUIMale INTEGER,
            PUISexUnkn INTEGER,
            PUIFLRes INTEGER,
            PUINotFLRes INTEGER,
            PUIFLResOut INTEGER,
            PUIContNo INTEGER,
            PUIContUnkn INTEGER,
            PUIAgeAvrg TEXT,
            PUITravelNo INTEGER,
            PUITravelYes INTEGER,
            TPositive INTEGER,
            TNegative INTEGER,
            TInconc INTEGER,
            TPending INTEGER,
            T_Total_Res INTEGER,
            T_LabPrivate_Res INTEGER,
            T_LabDOH_Res INTEGER,
            T_LabPrivate_NonRes INTEGER,
            T_LabDOH_NonRes INTEGER,
            C_Female INTEGER,
            C_Male INTEGER,
            C_SexUnkn INTEGER,
            C_AllResTypes INTEGER,
            C_Age_0_4 INTEGER,
            C_Age_5_14 INTEGER,
            C_Age_15_24 INTEGER,
            C_Age_25_34 INTEGER,
            C_Age_35_44 INTEGER,
            C_Age_45_54 INTEGER,
            C_Age_55_64 INTEGER,
            C_Age_65_74 INTEGER,
            C_Age_75_84 INTEGER,
            C_Age_85plus INTEGER,
            C_Age_Unkn INTEGER,
            C_AgeRange TEXT,
            C_AgeMedian TEXT,
            C_RaceWhite INTEGER,
            C_RaceBlack INTEGER,
            C_RaceOther INTEGER,
            C_RaceUnknown INTEGER,
            C_HispanicYES INTEGER,
            C_HispanicNO INTEGER,
            C_HispanicUnk INTEGER,
            C_EDYes_Res INTEGER,
            C_EDYes_NonRes INTEGER,
            C_HospYes_Res INTEGER,
            C_HospYes_NonRes INTEGER,
            C_NonResDeaths INTEGER,
            C_FLResDeaths INTEGER,
            CasesAll INTEGER,
            C_Men INTEGER,
            C_Women INTEGER,
            C_FLRes INTEGER,
            C_NotFLRes INTEGER,
            C_FLResOut INTEGER,
            T_NegRes INTEGER,
            T_NegNotFLRes INTEGER,
            T_total INTEGER,
            T_negative INTEGER,
            T_positive INTEGER,
            Deaths INTEGER,
            EverMon INTEGER,
            MonNow INTEGER,            
            FOREIGN KEY(to_county) REFERENCES Counties(id)
        ); ''')


    cur.close()
    conn.close()

def init_nursing_home_database():
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS NursingHomes;

        CREATE TABLE NursingHomes (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            to_county INTEGER,
            name TEXT UNIQUE,
            address TEXT,
            beds INTEGER,
            FOREIGN KEY(to_county) REFERENCES Counties(id)
        ); ''')

    cur.close()
    conn.close()

def init_institution_covid_database():
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS CorrectionalInstitutionsCovid;

        CREATE TABLE CorrectionalInstitutionsCovid (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            to_correctonal_institution INTEGER,
            inmate_security_quarantine INTEGER,
            inmate_medical_quarantine INTEGER,
            inmate_medical_isolation INTEGER,
            inmate_pending_tests INTEGER,
            inmate_negative_tests INTEGER,
            inmate_positive_tests INTEGER,
            staff_positive_tests INTEGER,
            FOREIGN KEY(to_correctonal_institution) REFERENCES CorrectionalInstitutions(id)
        ); ''')

    cur.close()
    conn.close()

def init_nursinghome_covid_database():
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS NursingHomeCovid;

        CREATE TABLE NursingHomeCovid (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            to_county INTEGER,
            name TEXT UNIQUE,
            resident_positive_tests INTEGER,
            staff_positive_tests INTEGER,
            FOREIGN KEY(to_county) REFERENCES Counties(id)
        ); ''')

    cur.close()
    conn.close()

def init_florida_demographics_17_under():
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS FloridaDemographics17AndUnder;

        CREATE TABLE FloridaDemographics17AndUnder (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            to_county INTEGER,
            percent REAL,
            number INTEGER,
            FOREIGN KEY(to_county) REFERENCES Counties(id)
        ); ''')

    cur.close()
    conn.close()

def init_florida_demographics_65_over():
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS FloridaDemographics65AndOver;

        CREATE TABLE FloridaDemographics65AndOver (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            to_county INTEGER,
            percent REAL,
            number INTEGER,
            FOREIGN KEY(to_county) REFERENCES Counties(id)
        ); ''')

    cur.close()
    conn.close()

def init_florida_demographics_black():
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS FloridaDemographicsBlack;

        CREATE TABLE FloridaDemographicsBlack (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            to_county INTEGER,
            percent REAL,
            number INTEGER,
            FOREIGN KEY(to_county) REFERENCES Counties(id)
        ); ''')

    cur.close()
    conn.close()

def init_florida_demographics_hispanic():
    conn = sqlite3.connect('data/database/floridacovid.sqlite')
    cur = conn.cursor()

    cur.executescript('''
        DROP TABLE IF EXISTS FloridaDemographicsHispanic;

        CREATE TABLE FloridaDemographicsHispanic (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            to_county INTEGER,
            percent REAL,
            number INTEGER,
            FOREIGN KEY(to_county) REFERENCES Counties(id)
        ); ''')

    cur.close()
    conn.close()
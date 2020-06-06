import pandas as pd
import sqlite3

# Read SQL DBs into DataFrames
conn = sqlite3.connect("data/database/floridacovid.sqlite")
counties_df = pd.read_sql_query("SELECT * FROM Counties;", conn)
correctional_institutions_df = pd.read_sql_query("SELECT * from CorrectionalInstitutions;", conn)
correctional_institutions_covid_df = pd.read_sql_query("SELECT * from CorrectionalInstitutionsCovid;", conn)
covid_df = pd.read_sql_query("SELECT * from Covid;", conn)
nursing_homes_df = pd.read_sql_query("SELECT * from NursingHomes;", conn)

print(counties_df)
print(correctional_institutions_df)
print(correctional_institutions_covid_df)
print(covid_df)
print(nursing_homes_df)
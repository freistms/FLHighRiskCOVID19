import pandas as pd
import sqlite3

# Read SQL DBs into DataFrames
conn = sqlite3.connect("data/database/floridacovid.sqlite")
counties_df = pd.read_sql_query("SELECT * FROM Counties;", conn)
correctional_institutions_df = pd.read_sql_query("SELECT * from CorrectionalInstitutions;", conn)
correctional_institutions_covid_df = pd.read_sql_query("SELECT * from CorrectionalInstitutionsCovid;", conn)
covid_df = pd.read_sql_query("SELECT * from Covid;", conn)
nursing_homes_df = pd.read_sql_query("SELECT * from NursingHomes;", conn)
nursing_home_covid_df = pd.read_sql_query("SELECT * from NursingHomeCovid;", conn)

#Drop Unnecessary Columns in DataFrames
correctional_institutions_df = correctional_institutions_df.drop(['name', 'url', 'address', 'gender', 'age'], axis=1)
correctional_institutions_covid_df = correctional_institutions_covid_df.drop(['inmate_security_quarantine', 'inmate_medical_quarantine', 'inmate_medical_isolation', 'inmate_pending_tests'], axis=1)
nursing_homes_df = nursing_homes_df.drop(['name', 'address', 'id'], axis=1)
nursing_home_covid_df = nursing_home_covid_df.drop(['id'], axis=1)
# nursing_home_covid_df = nursing_home_covid_df.drop(['name'], axis=1)


#Sum Total Beds by County for SNF
nursing_homes_df = nursing_homes_df.groupby('to_county').sum().reset_index()
#Sum Total Cases by County for SNF
nursing_home_covid_df = nursing_home_covid_df.groupby('to_county').sum().reset_index()
merge_snf_df = pd.merge(left=nursing_homes_df, right=nursing_home_covid_df, how='outer', left_on='to_county', right_on='to_county')

#Join CI data on available beds with COVID cases
covidci_df = pd.merge(left=correctional_institutions_df, right=correctional_institutions_covid_df, how='outer', left_on='id', right_on='to_correctonal_institution')
#Drop Unnecessary Columns in DataFrames
covidci_df = covidci_df.drop(['id_x', 'id_y', 'to_correctonal_institution'], axis=1)
#Fill NAN values with zero for summing functions
covidci_df["inmate_positive_tests"] = covidci_df["inmate_positive_tests"].fillna(0)
covidci_df["inmate_negative_tests"] = covidci_df["inmate_negative_tests"].fillna(0)
covidci_df["staff_positive_tests"] = covidci_df["staff_positive_tests"].fillna(0)
#Sum Total Cases by County for CI
covidci_df = covidci_df.groupby('to_county').sum().reset_index()

#Join County Data on CI with County Data on SNF
covidcisnf_df = pd.merge(left=covidci_df, right=merge_snf_df, how='outer', left_on='to_county', right_on='to_county')
covidcisnf_df = covidcisnf_df.rename(columns={"staff_positive_tests_x":"CI_Staff_Positives", "staff_positive_tests_y":"SNF_Staff_Positives"})

#Drop Unnecessary Columns in County Data on COVID cases
covid_df = covid_df[['to_county','TPositive','T_positive','TNegative','T_negative','T_total','T_Total_Res','C_AgeMedian',
                     'C_RaceWhite','C_RaceBlack', 'C_RaceOther', 'C_RaceUnknown', 'C_HispanicYES', 'C_HispanicNO', 'C_HispanicUnk',
                     'C_EDYes_Res', 'C_HospYes_Res','Deaths']]
#Join DataFrame on County Population Data with County COVID Data
covidcounty_df = pd.merge(left=counties_df, right=covid_df, how='outer', left_on='id', right_on='to_county')
covidcounty_df = covidcounty_df.drop(['to_county'], axis=1)

#Join County Data with SNF and CI Data
final_df = pd.merge(left=covidcounty_df, right=covidcisnf_df, how='outer', left_on='id', right_on='to_county')




pd.set_option("display.max_rows", None, "display.max_columns", None)
print(covidcounty_df)



# correctional_institutions_df = correctional_institutions_df.groupby("to_county").capacity.sum().reset_index()



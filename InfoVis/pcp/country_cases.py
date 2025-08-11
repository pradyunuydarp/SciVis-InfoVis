
import pandas as pd
import numpy as np


df = pd.read_csv('./ContainmentStringency_ConfirmedCases.csv')

NUMBER_OF_COUNTRIES = 20



# Get the top 10 countries that appear first in the dataset
top_countries = df.CountryName.unique()[:NUMBER_OF_COUNTRIES]

# Get the data for the top 10 countries
sorted_df = df[df['CountryName'].isin(top_countries)]

#Converting the Date column to datetime
sorted_df['Date'] = pd.to_datetime(sorted_df['Date'])

# Extract the year and month from the Date column
sorted_df['YearMonth'] = sorted_df['Date'].dt.to_period('M')

# Group by CountryName and YearMonth, then take the first row of each group
monthly_df = sorted_df.groupby(['CountryName', 'YearMonth']).first().reset_index()

country_cases_dict = {}

for country in monthly_df['CountryName'].unique():
    country_data = monthly_df[monthly_df['CountryName'] == country]
    country_cases_dict[country] = list(zip(country_data['YearMonth'].astype(str), country_data['Cases at end of month']))

#interpolating the missing values
for country in country_cases_dict:
    cases = country_cases_dict[country]
    cases = dict(cases)
    sorted_keys = sorted(cases.keys())
    for i in range(1, len(sorted_keys)):
        if cases[sorted_keys[i]] is None:
            cases[sorted_keys[i]] = cases[sorted_keys[i-1]]
    country_cases_dict[country] = list(cases.items())

# Convert the dictionary into a DataFrame
import pandas as pd

# Original dictionary data
data = country_cases_dict

# Convert the dictionary into a DataFrame
country_dataframes = []
for country, values in data.items():
    # Create a DataFrame for each country with Date and Value columns
    country_df = pd.DataFrame(values, columns=["Date", "Value"])
    country_df["Country"] = country  # Add a column for country name
    country_dataframes.append(country_df)

# Concatenate all country DataFrames into one
result_df = pd.concat(country_dataframes, ignore_index=True)

for country, values in country_cases_dict.items():
    formatted_values = [f"{value if value is not None else 'null'}" for _, value in values]
    countries = ['Germany', 'Turkey', 'Argentina', 'Italy', 'Indonesia',
                 'Iran', 'Poland', 'Colombia', 'Malaysia', 'South Africa', 'Peru',
                 'Ukraine', 'Mexico', 'Canada', 'Romania', 'Netherlands', 'Chile',
                 'Czech Republic', 'Pakistan']

    for country in countries:
        if country in country_cases_dict:
            values = country_cases_dict[country]
            formatted_values = [f"{value if value is not None else 'null'}" for _, value in values]


# Ordered list of countries as per given order
countries_order = [
    'Germany', 'Turkey', 'Argentina', 'Italy', 'Indonesia',
    'Iran', 'Poland', 'Colombia', 'Malaysia', 'South Africa', 'Peru',
    'Ukraine', 'Mexico', 'Canada', 'Romania', 'Netherlands', 'Chile',
    'Czech Republic', 'Pakistan'
]

# List of year_month values from 2020-03 to 2021-06
year_months = [
    '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08',
    '2020-09', '2020-10', '2020-11', '2020-12', '2021-01', '2021-02',
    '2021-03', '2021-04', '2021-05', '2021-06'
]

dimension = []
for i in range(len(year_months)):
    values = []
    for country in countries_order:
        if country in country_cases_dict and i < len(country_cases_dict[country]):
            values.append(country_cases_dict[country][i][1])
        else:
            values.append(None)
    dimension.append({"label": year_months[i], "values": values})

#Interpolate the values where they are missing also taking care of consecutive missing values
for i in range(1, len(dimension)):
    for j in range(len(dimension[i]["values"])):
        if dimension[i]["values"][j] is None:
            dimension[i]["values"][j] = dimension[i-1]["values"][j]

for x in dimension:
    print(f'{x},')





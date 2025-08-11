# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# %%
df = pd.read_csv('./confirmed_cases.csv')

# %%
df_new = df[['country_name', 'Nov2021']]
df_new

df_new.to_csv('updated_nonh.csv', index=False)

# %%
df_selected = df_usa[['CountryCode', 'RegionName', 'RegionCode', 'Date', 'ConfirmedCases']].copy()
df_selected

# %%
import pandas as pd


df_selected['Date'] = pd.to_datetime(df_selected['Date'], format='%Y%m%d')


df_selected['Month'] = df_selected['Date'].dt.to_period('M')


df_selected['ConfirmedCases'] = df_selected['ConfirmedCases'].fillna(method='ffill')

monthly_region_data = (
    df_selected
    .groupby(['RegionCode', 'Month'])['ConfirmedCases']
    .last()
    .groupby(level=0)
    .diff()
    .fillna(0)
    .reset_index()
)


monthly_region_data.rename(columns={'ConfirmedCases': 'MonthlyCases'}, inplace=True)

monthly_region_data


# %%
monthly_region_data.to_csv('monthly_region_data.csv',index=False)

# %%
region_codes = df_usa['RegionCode'].unique()
print(region_codes)

# %%
from io import StringIO


df = pd.read_csv("./confirmed_cases.csv")


filtered_df = df[df['Nov2021'] > 500000.0]

# Displaying the filtered result
filtered_df.to_csv('./updated_nonh2.csv', index=False)
filtered_df.head()

# %%




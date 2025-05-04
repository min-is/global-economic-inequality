import pandas as pd
import numpy as np
from functools import reduce

# URLs to datasets
gini_path = 'https://raw.githubusercontent.com/min-is/global-economic-inequality/refs/heads/main/data/raw/ginidata.csv'
gdp_capita_path = 'https://raw.githubusercontent.com/min-is/global-economic-inequality/refs/heads/main/data/raw/gdpcapita.csv'
gdp_current_path = 'https://raw.githubusercontent.com/min-is/global-economic-inequality/refs/heads/main/data/raw/gdpcurrent.csv'
gdp_growth_path = 'https://raw.githubusercontent.com/min-is/global-economic-inequality/refs/heads/main/data/raw/gdpgrowth.csv'

def clean_gini_data(gini_path):
    df = pd.read_csv(gini_path)
    df.columns = [col.split(' [')[0].strip() for col in df.columns]

    id_vars = ['Series Name', 'Series Code', 'Country Name', 'Country Code']
    df = df.melt(id_vars=id_vars, var_name='Year', value_name='Gini Index')
    df['Year'] = df['Year'].astype(int)
    df['Gini Index'] = pd.to_numeric(df['Gini Index'], errors='coerce')

    return df[['Country Name', 'Country Code', 'Year', 'Gini Index']]

def clean_gdp_capita(gdp_capita_path):
    df = pd.read_csv(gdp_capita_path, skiprows=4)
    expected_cols = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'] + [str(y) for y in range(1960, 2025)]
    df = df.iloc[:, :len(expected_cols)]
    df.columns = expected_cols

    id_vars = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
    df = df.melt(id_vars=id_vars, var_name='Year', value_name='GDP_per_capita')
    df['Year'] = df['Year'].astype(int)
    df['GDP_per_capita'] = pd.to_numeric(df['GDP_per_capita'], errors='coerce')

    return df[['Country Name', 'Country Code', 'Year', 'GDP_per_capita']]

def clean_gdp_current(gdp_current_path):
    df = pd.read_csv(gdp_current_path, skiprows=4)
    expected_cols = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'] + [str(y) for y in range(1960, 2025)]
    df = df.iloc[:, :len(expected_cols)]
    df.columns = expected_cols

    id_vars = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
    df = df.melt(id_vars=id_vars, var_name='Year', value_name='GDP_current')
    df['Year'] = df['Year'].astype(int)
    df['GDP_current'] = pd.to_numeric(df['GDP_current'], errors='coerce')

    return df[['Country Name', 'Country Code', 'Year', 'GDP_current']]

def clean_gdp_growth(gdp_growth_path):
    df = pd.read_csv(gdp_growth_path, skiprows=4)
    expected_cols = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'] + [str(y) for y in range(1960, 2025)]
    df = df.iloc[:, :len(expected_cols)]
    df.columns = expected_cols

    id_vars = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
    df = df.melt(id_vars=id_vars, var_name='Year', value_name='GDP_growth')
    df['Year'] = df['Year'].astype(int)
    df['GDP_growth'] = pd.to_numeric(df['GDP_growth'], errors='coerce')

    return df[['Country Name', 'Country Code', 'Year', 'GDP_growth']]

def merge_datasets(dfs):
    merged_df = reduce(lambda left, right: pd.merge(left, right, on=['Country Name', 'Country Code', 'Year'], how='outer'), dfs)
    merged_df['Decade'] = (merged_df['Year'] // 10) * 10
    return merged_df

def handle_missing_values(df):
    df['Data Completeness'] = df[['Gini Index', 'GDP_per_capita', 'GDP_current', 'GDP_growth']].notnull().mean(axis=1)
    df = df[df['Data Completeness'] >= 0.5]

    for col in ['Gini Index', 'GDP_per_capita', 'GDP_current', 'GDP_growth']:
        df[col] = df.groupby('Country Code').apply(
            lambda group: group.set_index(pd.to_datetime(group['Year'], format='%Y'))[col]
            .interpolate(method='time', limit_direction='both')
            .reset_index(drop=True)
        ).reset_index(drop=True)

    return df.drop(columns='Data Completeness')


# Clean each dataset
gini_clean = clean_gini_data(gini_path)
gdp_capita_clean = clean_gdp_capita(gdp_capita_path)
gdp_current_clean = clean_gdp_current(gdp_current_path)
gdp_growth_clean = clean_gdp_growth(gdp_growth_path)

# Merge all cleaned datasets
merged_df = merge_datasets([gini_clean, gdp_capita_clean, gdp_current_clean, gdp_growth_clean])

# Handle missing values
final_data = handle_missing_values(merged_df)

# Export to CSV
final_data.to_csv('global_economic_data.csv', index=False)

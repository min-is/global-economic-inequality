import pandas as pd
import os

def tableau():
    data = pd.read_csv('data/final/inequality_data.csv')
    
    # Create output directory
    os.makedirs('visualization/tableau', exist_ok=True)
    
    # 1. Create main dataset for Tableau
    
    g20_countries = ['USA', 'CAN', 'MEX', 'BRA', 'ARG', 'GBR', 'DEU', 'FRA', 'ITA', 
                     'RUS', 'TUR', 'SAU', 'ZAF', 'CHN', 'JPN', 'KOR', 'IND', 'IDN', 'AUS']
    
    asean_countries = ['BRN', 'KHM', 'IDN', 'LAO', 'MYS', 'MMR', 'PHL', 'SGP', 'THA', 'VNM']
    
    data['is_g20'] = data['country_code'].isin(g20_countries)
    data['is_asean'] = data['country_code'].isin(asean_countries)
    
    data.to_csv('visualization/tableau/inequality_data_tableau.csv', index=False)
    
    # 2. Create aggregated datasets for specific visualizations
    
    if 'region' in data.columns:
        regional_data = data.groupby(['year', 'region']).agg({
            'gdp_per_capita': 'mean',
            'gini_index': 'mean',
            'education_expenditure': 'mean',
            'health_expenditure': 'mean',
            'life_expectancy': 'mean'
        }).reset_index()
        
        regional_data.to_csv('visualization/tableau/regional_averages_tableau.csv', index=False)
    
    econ_bloc_data = []
    
    for year, year_data in data.groupby('year'):
        # G20 average
        g20_rows = year_data[year_data['is_g20'] == True]
        if len(g20_rows) > 0:
            econ_bloc_data.append({
                'year': year,
                'economic_bloc': 'G20',
                'countries_count': len(g20_rows),
                'avg_gdp_per_capita': g20_rows['gdp_per_capita'].mean(),
                'avg_gini_index': g20_rows['gini_index'].mean(),
                'avg_education_expenditure': g20_rows['education_expenditure'].mean(),
                'avg_health_expenditure': g20_rows['health_expenditure'].mean(),
                'avg_life_expectancy': g20_rows['life_expectancy'].mean()
            })
        
        # ASEAN average
        asean_rows = year_data[year_data['is_asean'] == True]
        if len(asean_rows) > 0:
            econ_bloc_data.append({
                'year': year,
                'economic_bloc': 'ASEAN',
                'countries_count': len(asean_rows),
                'avg_gdp_per_capita': asean_rows['gdp_per_capita'].mean(),
                'avg_gini_index': asean_rows['gini_index'].mean(),
                'avg_education_expenditure': asean_rows['education_expenditure'].mean(),
                'avg_health_expenditure': asean_rows['health_expenditure'].mean(),
                'avg_life_expectancy': asean_rows['life_expectancy'].mean()
            })
        
        # Rest of world average
        row_avg = year_data[~((year_data['is_g20'] == True) | (year_data['is_asean'] == True))]
        if len(row_avg) > 0:
            econ_bloc_data.append({
                'year': year,
                'economic_bloc': 'Rest of World',
                'countries_count': len(row_avg),
                'avg_gdp_per_capita': row_avg['gdp_per_capita'].mean(),
                'avg_gini_index': row_avg['gini_index'].mean(),
                'avg_education_expenditure': row_avg['education_expenditure'].mean(),
                'avg_health_expenditure': row_avg['health_expenditure'].mean(),
                'avg_life_expectancy': row_avg['life_expectancy'].mean()
            })
    
    # Convert to DataFrame and save
    econ_bloc_df = pd.DataFrame(econ_bloc_data)
    econ_bloc_df.to_csv('visualization/tableau/economic_bloc_averages_tableau.csv', index=False)
    
    print("Data prepared for Tableau visualizations successfully.")

if __name__ == "__main__":
    tableau()
import pandas as pd
import numpy as np

def calculate_inequality_metrics():
    data = pd.read_csv('data/final/inequality_data.csv')
    
    yearly_metrics = []
    
    for year, year_data in data.groupby('year'):
        if len(year_data) < 10:  # Skip years with too little data
            continue
            
        # Calculate coefficient of variation for GDP per capita
        gdp_cv = year_data['gdp_per_capita'].std() / year_data['gdp_per_capita'].mean() if year_data['gdp_per_capita'].mean() > 0 else np.nan
        
        # Calculate average Gini index
        avg_gini = year_data['gini_index'].mean()
        
        # Calculate 90/10 percentile ratio for GDP
        p90 = np.nanpercentile(year_data['gdp_per_capita'], 90)
        p10 = np.nanpercentile(year_data['gdp_per_capita'], 10)
        p90_p10_ratio = p90 / p10 if p10 > 0 else np.nan
        
        # Add metrics to list
        yearly_metrics.append({
            'year': year,
            'countries_count': len(year_data),
            'gdp_coefficient_variation': gdp_cv,
            'avg_gini_index': avg_gini,
            'gdp_p90_p10_ratio': p90_p10_ratio
        })
    
    metrics_df = pd.DataFrame(yearly_metrics)
    metrics_df.to_csv('data/processed/yearly_inequality_metrics.csv', index=False)
    print(f"Calculated inequality metrics for {len(metrics_df)} years.")
    
    # Regional inequality analysis
    if 'region' in data.columns:
        regional_metrics = []
        
        for year, year_data in data.groupby('year'):
            if len(year_data) < 20:  # Skip years with too little data
                continue
                
            for region, region_data in year_data.groupby('region'):
                if len(region_data) < 3:  # Skip regions with too few countries
                    continue
                    
                # regional metrics
                regional_metrics.append({
                    'year': year,
                    'region': region,
                    'countries_count': len(region_data),
                    'avg_gdp_per_capita': region_data['gdp_per_capita'].mean(),
                    'avg_gini_index': region_data['gini_index'].mean(),
                    'avg_life_expectancy': region_data['life_expectancy'].mean(),
                    'avg_education_expenditure': region_data['education_expenditure'].mean(),
                    'avg_health_expenditure': region_data['health_expenditure'].mean()
                })
        
        regional_df = pd.DataFrame(regional_metrics)
        regional_df.to_csv('data/processed/regional_inequality_metrics.csv', index=False)
        print(f"Calculated regional metrics for {len(regional_df)} region-year combinations.")

if __name__ == "__main__":
    calculate_inequality_metrics()
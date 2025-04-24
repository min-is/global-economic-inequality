import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

def perform_regression_analysis():
    data = pd.read_csv('data/final/inequality_data.csv')

    results = []
    
    recent_years = sorted(data['year'].unique(), reverse=True)
    
    for year in recent_years:
        year_data = data[data['year'] == year]
        
        if (year_data['gdp_per_capita'].notna().sum() >= 30 and
            year_data['life_expectancy'].notna().sum() >= 30):
            
            print(f"Performing regression analysis for year {year}")
            
            reg_data = year_data.dropna(subset=['gdp_per_capita', 'life_expectancy'])
            
            reg_data['log_gdp'] = np.log(reg_data['gdp_per_capita'])
            
            X = sm.add_constant(reg_data['log_gdp'])
            y = reg_data['life_expectancy']
            
            model = sm.OLS(y, X).fit()
            
            results.append({
                'year': year,
                'intercept': model.params[0],
                'log_gdp_coefficient': model.params[1],
                'r_squared': model.rsquared,
                'p_value': model.pvalues[1],
                'n_observations': model.nobs,
                'std_error': model.bse[1]
            })
            
            # Also run by region if region data is available
            if 'region' in reg_data.columns:
                for region, region_data in reg_data.groupby('region'):
                    if len(region_data) >= 5:  # Only run if we have enough countries
                        X_region = sm.add_constant(region_data['log_gdp'])
                        y_region = region_data['life_expectancy']
                        
                        try:
                            region_model = sm.OLS(y_region, X_region).fit()
                            
                            results.append({
                                'year': year,
                                'region': region,
                                'intercept': region_model.params[0],
                                'log_gdp_coefficient': region_model.params[1],
                                'r_squared': region_model.rsquared,
                                'p_value': region_model.pvalues[1],
                                'n_observations': region_model.nobs,
                                'std_error': region_model.bse[1]
                            })
                        except:
                            print(f"Could not run regression for region {region} in year {year}")
            
            break
    
    regression_df = pd.DataFrame(results)
    regression_df.to_csv('data/processed/gdp_life_expectancy_regression.csv', index=False)
    
    print(f"Regression analysis complete: {len(regression_df)} models.")

if __name__ == "__main__":
    perform_regression_analysis()
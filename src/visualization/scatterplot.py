import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import os

def create_scatter_plots():
    data = pd.read_csv('data/final/inequality_data.csv')
    
    recent_years = sorted(data['year'].unique(), reverse=True)
    
    for year in recent_years:
        year_data = data[data['year'] == year]
        
        if (year_data['gdp_per_capita'].notna().sum() >= 50 and
            year_data['life_expectancy'].notna().sum() >= 50):
            
            print(f"Creating scatter plots for year {year}")
            
            plot_data = year_data.dropna(subset=['gdp_per_capita', 'life_expectancy']).copy()
            plot_data['log_gdp'] = np.log10(plot_data['gdp_per_capita'])
            
            os.makedirs('visualization/python', exist_ok=True)
            os.makedirs('reports/figures', exist_ok=True)

            plt.figure(figsize=(12, 8))
            
            # Plot by region if available
            if 'region' in plot_data.columns:
                for region, region_data in plot_data.groupby('region'):
                    if len(region_data) >= 5: 
                        plt.scatter(
                            region_data['log_gdp'],
                            region_data['life_expectancy'],
                            alpha=0.7,
                            label=region,
                            s=50
                        )
                        
                        # Fit regression line
                        if len(region_data) > 1:
                            X = region_data['log_gdp'].values.reshape(-1, 1)
                            y = region_data['life_expectancy'].values
                            
                            model = LinearRegression()
                            model.fit(X, y)
                            
                            # Create prediction line
                            x_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
                            y_pred = model.predict(x_range)
                            
                            plt.plot(x_range, y_pred, linestyle='--', alpha=0.7)
            else:
                # Simple scatter plot
                plt.scatter(
                    plot_data['log_gdp'],
                    plot_data['life_expectancy'],
                    alpha=0.7,
                    s=50
                )
            
            # Fit 
            X_all = plot_data['log_gdp'].values.reshape(-1, 1)
            y_all = plot_data['life_expectancy'].values
            
            model_all = LinearRegression()
            model_all.fit(X_all, y_all)
            
            # prediction line
            x_range_all = np.linspace(X_all.min(), X_all.max(), 100).reshape(-1, 1)
            y_pred_all = model_all.predict(x_range_all)
            
            plt.plot(x_range_all, y_pred_all, color='black', linewidth=2, label='Overall trend')
            
            plt.xlabel('Log GDP per Capita', fontsize=14)
            plt.ylabel('Life Expectancy (years)', fontsize=14)
            plt.title(f'GDP per Capita vs Life Expectancy ({year})', fontsize=16)

            r_squared = model_all.score(X_all, y_all)
            slope = model_all.coef_[0]
            intercept = model_all.intercept_
            
            plt.text(
                0.05, 0.05, 
                f'Life Expectancy = {slope:.2f} × log(GDP) + {intercept:.2f}\nR² = {r_squared:.2f}',
                transform=plt.gca().transAxes,
                fontsize=12,
                bbox=dict(facecolor='white', alpha=0.7)
            )

            if 'region' in plot_data.columns:
                plt.legend(title='Region', loc='lower right')
            
            plt.grid(alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(f'reports/figures/gdp_life_expectancy_{year}.png', dpi=300)
            plt.close()
            
            break 

if __name__ == "__main__":
    create_scatter_plots()
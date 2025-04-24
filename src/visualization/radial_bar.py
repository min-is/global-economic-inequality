import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_radial_bar_plots():

    data = pd.read_csv('data/final/inequality_data.csv')
    
    recent_years = sorted(data['year'].unique(), reverse=True)
    
    for year in recent_years:
        year_data = data[data['year'] == year]
        
        if (year_data['education_expenditure'].notna().sum() >= 30 and
            year_data['health_expenditure'].notna().sum() >= 30):
            
            print(f"Creating radial bar plots for year {year}")
            
            # Group by region
            if 'region' in year_data.columns:
                regional_data = year_data.groupby('region').agg({
                    'education_expenditure': 'mean',
                    'health_expenditure': 'mean'
                }).reset_index()
                
                regional_data = regional_data.sort_values('education_expenditure')
                
                os.makedirs('visualization/python', exist_ok=True)
                os.makedirs('reports/figures', exist_ok=True)
                
                # Create the radial bar plot for education expenditure
                fig = plt.figure(figsize=(10, 10))
                ax = fig.add_subplot(111, polar=True)
                
                # Number of regions
                N = len(regional_data)
                
                width = 2 * np.pi / N
                angles = np.linspace(0, 2*np.pi, N, endpoint=False)
                
                bars = ax.bar(
                    angles, 
                    regional_data['education_expenditure'], 
                    width=width * 0.8, 
                    bottom=0.0,
                    alpha=0.7,
                    color=sns.color_palette("viridis", N)
                )
                
                # region labels
                for angle, region, value in zip(angles, regional_data['region'], regional_data['education_expenditure']):
                    ax.text(
                        angle, 
                        value + 0.1, 
                        f"{region}\n({value:.1f}%)", 
                        ha='center', 
                        va='center', 
                        rotation=angle * 180/np.pi,
                        rotation_mode="anchor"
                    )
                
                # Remove grid and tick labels
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_title(f'Regional Education Expenditure (% of GDP) - {year}', fontsize=15)

                plt.tight_layout()
                plt.savefig(f'reports/figures/education_radial_{year}.png', dpi=300)
                plt.close()
                

                fig = plt.figure(figsize=(10, 10))
                ax = fig.add_subplot(111, polar=True)
                
                # Plot bars
                bars = ax.bar(
                    angles, 
                    regional_data['health_expenditure'], 
                    width=width * 0.8, 
                    bottom=0.0,
                    alpha=0.7,
                    color=sns.color_palette("magma", N)
                )
                
                for angle, region, value in zip(angles, regional_data['region'], regional_data['health_expenditure']):
                    ax.text(
                        angle, 
                        value + 0.1, 
                        f"{region}\n({value:.1f}%)", 
                        ha='center', 
                        va='center', 
                        rotation=angle * 180/np.pi,
                        rotation_mode="anchor"
                    )
                
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_title(f'Regional Health Expenditure (% of GDP) - {year}', fontsize=15)
                
                # Save figure
                plt.tight_layout()
                plt.savefig(f'reports/figures/health_radial_{year}.png', dpi=300)
                plt.close()
            
            break  

if __name__ == "__main__":
    create_radial_bar_plots()
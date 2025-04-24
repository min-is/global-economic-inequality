import pandas as pd
import plotly.express as px
import os

def create_choropleth_maps():

    data = pd.read_csv('data/final/inequality_data.csv')

    recent_years = sorted(data['year'].unique(), reverse=True)
    
    for year in recent_years:
        year_data = data[data['year'] == year]

        if (year_data['gdp_per_capita'].notna().sum() >= len(year_data) * 0.7 and
            year_data['gini_index'].notna().sum() >= len(year_data) * 0.5):
            
            print(f"Creating choropleth maps for year {year}")
            
            # GDP per capita map
            fig_gdp = px.choropleth(
                year_data,
                locations='country_code',
                color='gdp_per_capita',
                hover_name='country_name',
                color_continuous_scale='YlGnBu',
                title=f'GDP per Capita by Country ({year})',
                labels={'gdp_per_capita': 'GDP per Capita (USD)'},
                projection='natural earth'
            )
            
            # Improve layout
            fig_gdp.update_layout(
                margin=dict(l=0, r=0, t=40, b=0),
                coloraxis_colorbar=dict(title='USD')
            )
            
            # Create output directory if it doesn't exist
            os.makedirs('visualization/python', exist_ok=True)
            os.makedirs('reports/figures', exist_ok=True)
            
            fig_gdp.write_html(f'visualization/python/gdp_per_capita_map_{year}.html')
            fig_gdp.write_image(f'reports/figures/gdp_per_capita_map_{year}.png', width=1200, height=800)
            
            # Gini index map
            gini_data = year_data.dropna(subset=['gini_index'])
            
            if len(gini_data) >= 30:  # Only create if we have enough data
                fig_gini = px.choropleth(
                    gini_data,
                    locations='country_code',
                    color='gini_index',
                    hover_name='country_name',
                    color_continuous_scale='Reds',
                    title=f'GINI Index by Country ({year})',
                    labels={'gini_index': 'GINI Index'},
                    projection='natural earth'
                )
                
                # Improve layout
                fig_gini.update_layout(
                    margin=dict(l=0, r=0, t=40, b=0),
                    coloraxis_colorbar=dict(title='GINI')
                )
                
                fig_gini.write_html(f'visualization/python/gini_index_map_{year}.html')
                fig_gini.write_image(f'reports/figures/gini_index_map_{year}.png', width=1200, height=800)
            
            break  # Stop after creating maps for the most recent year with good data

if __name__ == "__main__":
    create_choropleth_maps()
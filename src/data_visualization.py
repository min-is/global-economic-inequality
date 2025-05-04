import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio
pio.renderers.default = 'browser'


path = 'https://raw.githubusercontent.com/min-is/global-economic-inequality/refs/heads/main/data/processed/global_economic_data.csv'
df = pd.read_csv(path)

df.rename(columns={
    'country_code': 'Country Code',
    'country_name': 'Country Name',
    'year': 'Year',
    'gini_index': 'Gini Index',
    'gdp_per_capita': 'GDP_per_capita',
    'gdp_current': 'GDP_current',
    'gdp_growth': 'GDP_growth',
    'decade': 'Decade'
}, inplace=True)

def create_choropleth_map(metric='GDP_per_capita'):
    fig = px.choropleth(
        df.dropna(subset=[metric]),
        locations="Country Code",
        color=metric,
        hover_name="Country Name",
        animation_frame="Year",
        color_continuous_scale=px.colors.sequential.Plasma,
        range_color=(df[metric].quantile(0.1), df[metric].quantile(0.9)),
        labels={metric: metric.replace('_', ' ').title()},
        title=f"Global {metric.replace('_', ' ').title()} Evolution (2000-2023)"
    )
    
    fig.update_layout(
        coloraxis_colorbar=dict(
            title='Log Scale' if 'gdp' in metric.lower() else 'Scale',
            tickvals=np.logspace(
                np.log10(df[metric].min()), 
                np.log10(df[metric].max()), 
                num=5
            ) if 'gdp' in metric.lower() else None
        ),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        )
    )
    return fig

def create_radial_plot():
    plt.figure(figsize=(12, 12))
    ax = plt.subplot(111, polar=True)
    
    decade_data = df.groupby('Decade').agg({
        'GDP_growth': 'mean',
        'GDP_per_capita': 'mean',
        'Gini Index': 'mean'
    }).reset_index()
    
    categories = list(decade_data['Decade'].astype(str))
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    width = 2 * np.pi / N * 0.8
    
    for i, metric in enumerate(['GDP_growth', 'GDP_per_capita', 'Gini Index']):
        values = decade_data[metric].values
        values /= values.max()  # Normalize
        ax.bar(
            angles + i*width/3,
            values,
            width=width/3,
            label=metric.replace('_', ' ').title(),
            alpha=0.8
        )
    
    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles)
    ax.set_xticklabels(categories)
    
    plt.title('Decadal Economic Performance Analysis', y=1.08)
    plt.legend(loc='upper right')
    return plt

def create_scatter_analysis(year=2023):
    year_df = df[df['Year'] == year].dropna(subset=['GDP_per_capita', 'Gini Index'])
    
    fig = px.scatter(
        year_df,
        x='GDP_per_capita',
        y='Gini Index',
        size='GDP_current',
        color='Country Name',
        hover_name='Country Name',
        log_x=True,
        trendline='lowess',
        title=f"Wealth vs Inequality ({year})",
        labels={
            'GDP_per_capita': 'GDP per Capita (USD, log scale)',
            'Gini Index': 'Income Inequality (Gini Index)'
        }
    )
    
    fig.update_layout(
        xaxis=dict(
            type='log',
            range=[np.log10(year_df['GDP_per_capita'].min()), 
                   np.log10(year_df['GDP_per_capita'].max())]
        ),
        yaxis=dict(range=[year_df['Gini Index'].min(), year_df['Gini Index'].max()])
    )
    return fig

def create_country_comparison(countries):
    country_df = df[df['Country Name'].isin(countries)]
    
    fig = go.Figure()
    
    for country in countries:
        # gdp per capita
        fig.add_trace(go.Scatter(
            x=country_df[country_df['Country Name'] == country]['Year'],
            y=country_df[country_df['Country Name'] == country]['GDP_per_capita'],
            name=f"{country} GDP/cap",
            yaxis='y1'
        ))
        
        # gini index
        fig.add_trace(go.Scatter(
            x=country_df[country_df['Country Name'] == country]['Year'],
            y=country_df[country_df['Country Name'] == country]['Gini Index'],
            name=f"{country} Gini",
            yaxis='y2',
            line=dict(dash='dot')
        ))
    
    fig.update_layout(
        title="Country Economic Comparison",
        yaxis=dict(title='GDP per Capita (USD)', type='log'),
        yaxis2=dict(
            title='Gini Index',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified'
    )
    return fig

if __name__ == "__main__":
    choropleth_fig = create_choropleth_map('GDP_per_capita')
    choropleth_fig.show()
    
    radial_plot = create_radial_plot()
    radial_plot.show()
    
    scatter_fig = create_scatter_analysis(2023)
    scatter_fig.show()
    
    comparison_fig = create_country_comparison(['United States of America', 'China', 'India', 'Germany'])
    comparison_fig.show()

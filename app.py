import os
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Bootstrap theme
external_stylesheets = [dbc.themes.LUX]

# Initialize Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server  # For Heroku

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/min-is/global-economic-inequality/main/data/processed/global_economic_data.csv")
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

# Visualization functions (as before)
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
        margin=dict(l=20, r=20, t=60, b=20),
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
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(
            type='log',
            range=[np.log10(year_df['GDP_per_capita'].min()), 
                   np.log10(year_df['GDP_per_capita'].max())]
        ),
        yaxis=dict(range=[year_df['Gini Index'].min(), year_df['Gini Index'].max()])
    )
    return fig

def create_country_comparison(countries):
    country_df = df[df['Country Name'].isin(countries)].copy()
    
    # Convert Year to numeric and filter valid range
    country_df['Year'] = pd.to_numeric(country_df['Year'], errors='coerce')
    country_df = country_df[(country_df['Year'] >= 2000) & (country_df['Year'] <= 2023)]
    
    # Handle missing values
    country_df['GDP_per_capita'] = country_df['GDP_per_capita'].interpolate()
    country_df['Gini Index'] = country_df.groupby('Country Name')['Gini Index'].ffill().bfill()
    
    fig = go.Figure()
    
    for country in countries:
        country_data = country_df[country_df['Country Name'] == country]
        
        # GDP per Capita (Primary Axis)
        fig.add_trace(go.Scatter(
            x=country_data['Year'],
            y=country_data['GDP_per_capita'],
            name=f"{country} GDP/cap",
            yaxis='y1',
            line=dict(width=2)
        ))
        
        # Gini Index (Secondary Axis)
        fig.add_trace(go.Scatter(
            x=country_data['Year'],
            y=country_data['Gini Index'],
            name=f"{country} Gini",
            yaxis='y2',
            line=dict(dash='dot', width=2)
        ))
    
    fig.update_layout(
        title="Country Economic Comparison (2000-2023)",
        xaxis=dict(title='Year', tickmode='linear'),
        yaxis=dict(
            title='GDP per Capita (USD)',
            type='log',
            range=[2, 5]  # Log range for 100 to 100,000 USD
        ),
        yaxis2=dict(
            title='Gini Index',
            overlaying='y',
            side='right',
            range=[20, 60]  # Standard Gini scale range
        ),
        hovermode='x unified',
        legend=dict(x=1.1, y=1.1)
    )
    return fig


# App Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("🌍 Global Economic Inequality Dashboard", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Select Economic Metric", className="card-title"),
                    dcc.Dropdown(
                        id='variable-dropdown',
                        options=[
                            {'label': 'GDP per capita', 'value': 'GDP_per_capita'},
                            {'label': 'Gini Index', 'value': 'Gini Index'},
                        ],
                        value='GDP_per_capita',
                        clearable=False,
                        style={'color': '#000'}
                    ),
                ])
            ], className="mb-4 shadow-sm")
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Choropleth Map", className="card-title"),
                    dcc.Loading(dcc.Graph(id='choropleth-map', config={'displayModeBar': False}), type="circle")
                ])
            ], className="mb-4 shadow-sm")
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Wealth vs Inequality (2023)", className="card-title"),
                    dcc.Loading(dcc.Graph(id='scatter-plot', config={'displayModeBar': False}), type="circle")
                ])
            ], className="mb-4 shadow-sm")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Country Comparison", className="card-title"),
                    dcc.Loading(dcc.Graph(id='country-comparison', config={'displayModeBar': False}), type="circle")
                ])
            ], className="mb-4 shadow-sm")
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col(html.Footer([
            html.Hr(),
            html.P("Made with ❤️ using Dash & Plotly", className="text-center text-muted")
        ]), width=12)
    ])
], fluid=True, style={'backgroundColor': '#f8f9fa'})

# Callbacks
@app.callback(
    Output('choropleth-map', 'figure'),
    Input('variable-dropdown', 'value')
)
def update_figure(selected_variable):
    return create_choropleth_map(selected_variable)

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('variable-dropdown', 'value')
)
def update_scatter_plot(selected_variable):
    return create_scatter_analysis(2023)


@app.callback(
    Output('country-comparison', 'figure'),
    Input('variable-dropdown', 'value')
)
def update_country_comparison(selected_variable):
    return create_country_comparison(['United States', 'China', 'India', 'Germany'])

if __name__ == '__main__':
    app.run_server(debug=False)

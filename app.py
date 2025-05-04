import os
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Load your cleaned data
df = pd.read_csv("https://raw.githubusercontent.com/min-is/global-economic-inequality/main/data/processed/global_economic_data.csv")

# Create a choropleth map
def create_choropleth_map(variable='GDP_per_capita'):
    fig = px.choropleth(
        df,
        locations="country_code",
        color=variable,
        hover_name="country_name",
        animation_frame="year",
        color_continuous_scale=px.colors.sequential.Plasma,
        projection="natural earth"
    )
    fig.update_layout(title=f"Global {variable} Over Time")
    return fig

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Global Economic Inequality"),
    dcc.Dropdown(
        id='variable-dropdown',
        options=[
            {'label': 'GDP per capita', 'value': 'GDP_per_capita'},
            {'label': 'Gini Index', 'value': 'gini_index'},
            {'label': 'HDI', 'value': 'HDI'}
        ],
        value='GDP_per_capita'
    ),
    dcc.Graph(id='choropleth-map')
])

# Callback to update graph
@app.callback(
    dash.dependencies.Output('choropleth-map', 'figure'),
    [dash.dependencies.Input('variable-dropdown', 'value')]
)
def update_figure(selected_variable):
    return create_choropleth_map(selected_variable)

# Run app locally (for Heroku, PORT is set dynamically)
if __name__ == '__main__':
    app.run_server(debug=True, port=int(os.environ.get("PORT", 8050)), host="0.0.0.0")

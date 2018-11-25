
# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 
# 
# 1) The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# 
# 2) The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 
# 

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

df = pd.read_csv('nama_10_gdp/nama_10_gdp_1_Data.csv')

eu_synonyms = [
    'European Union (current composition)',
    'European Union (without United Kingdom)',
    'European Union (15 countries)',
    'Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)',
    'Euro area (19 countries)',
    'Euro area (12 countries)']

df_cleaned = df[df["Value"] != ":"]                        # drop not available values
x = df_cleaned["GEO"].isin(eu_synonyms)

df_cleaned.drop(df_cleaned[df_cleaned["GEO"].isin(eu_synonyms)].index, inplace=True)  # remove EU aggregate values
df_cleaned.reset_index(inplace=True, drop=True)

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators = df_cleaned["NA_ITEM"].unique()   # define indicators for drop-down (NA_ITEMS)
available_units = df_cleaned["UNIT"].unique()           # define indicators for drop-down (UNIT)
available_countries = df_cleaned["GEO"].unique()        # define indicators for drop-down (GEO)


app.layout = html.Div([
    html.Div([
        html.H1(
            children = "First Task (Scatterplot)",
            style = {'font-family': 'Arial, Helvetica, sans-serif', 'text-align': 'center'}
        ),
        html.Div([                                      # drop-down for indicator 1 (x-axis)
            html.P(
                children = 'Select first indicator:',
                style = {'font-size': '12px', 'font-family': 'Arial, Helvetica, sans-serif', 'color': 'red'}
            ),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(                             # lin vs log radio button
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
                )
        ],
        style={'width': '33.33%', 'float': 'left', 'display': 'inline-block'}),

        html.Div([                                      # drop-down for indicator 2 (y-axis)
            html.P(
                children = 'Select second indicator:',
                style = {'font-size': '12px', 'font-family': 'Arial, Helvetica, sans-serif', 'color': 'red'}
            ),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure'
            ),
            dcc.RadioItems(                             # lin vs log radio button
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '33.33%', 'margin-left': 'auto', 'margin-right': 'auto', 'display': 'inline-block'}),
        
        html.Div([                                      # drop-down for unit
            html.P(
                children = 'Select unit:',
                style = {'font-size': '12px', 'font-family': 'Arial, Helvetica, sans-serif', 'color': 'red'}
            ),
                dcc.Dropdown(
                id='unit_selection',
                options=[{'label': i, 'value': i} for i in available_units],
                value='Current prices, million euro'
            )
        ],style={'width': '33.33%', 'float': 'right', 'display': 'inline-block'})
    ]),
  
    dcc.Graph(id='indicator-graphic-task1'),
    
    html.Div([
        html.P(
                children = 'Select a year:',
                style = {'font-size': '12px', 'font-family': 'Arial, Helvetica, sans-serif', 'color': 'red'}
            ),
        dcc.Slider(                                         # slider for year 
            id='year--slider',
            min=df_cleaned['TIME'].min(),
            max=df_cleaned['TIME'].max(),
            value=df_cleaned['TIME'].max(),
            step=None,
            marks={str(year): str(year) for year in df_cleaned['TIME'].unique()}
        )
    ],
        style={'width': '90%', 'margin' : 'auto'}),
    
    # task 2
    
    html.Div([
    ], 
        style = {'margin': '65px 65px 10px 10px', 'background-color': 'black', 'height': '2px'}
    ),
    
    html.H1(
            children = "Second Task (Line Chart)",
            style = {'font-family': 'Arial, Helvetica, sans-serif', 'text-align': 'center'}
        ),
    
    html.Div([

        html.Div([                                      # drop-down for country
            html.P(
                children = 'Select country:',
                style = {'font-size': '12px', 'font-family': 'Arial, Helvetica, sans-serif', 'color': 'red'}
            ),
            dcc.Dropdown(
                id='country_selection',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Belgium'
            )
        ],
        style={'width': '33.33%', 'float': "left",'display': 'inline-block'}),

        html.Div([                                      # drop-down for indicator
            html.P(
                children = 'Select indicator:',
                style = {'font-size': '12px', 'font-family': 'Arial, Helvetica, sans-serif', 'color': 'red'}
            ),
            dcc.Dropdown(
                id='indicator_selection',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )   
        ],
        style={'width': '33.33%', "margin-left": "auto", "margin-right": "auto", 'display': 'inline-block'}),
        
        html.Div([                                      
            html.P(
                children = 'Select unit:',
                style = {'font-size': '12px', 'font-family': 'Arial, Helvetica, sans-serif', 'color': 'red'}
            ),
            dcc.Dropdown(                               # drop-down for unit
                id='unit_selection',
                options=[{'label': i, 'value': i} for i in available_units],
                value='Current prices, million euro'
            )
        ],
        style={'width': '33.33%', "float": "right", 'display': 'inline-block'})         
    ]),
    
    dcc.Graph(id='indicator-graphic-task2')

])

@app.callback(                                          # define app with output and input variables
    dash.dependencies.Output('indicator-graphic-task1', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('unit_selection', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, unit_value,
                 xaxis_type, yaxis_type,
                 year_value):
    
    dff = df_cleaned[(df_cleaned['TIME'] == year_value) & (df_cleaned['UNIT'] == unit_value)]   # filter by year and unit
    

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 90, 'b': 70, 't': 70, 'r': 90},
            hovermode='closest'
        )
    }

@app.callback(                                          # define app with output and input variables
    dash.dependencies.Output('indicator-graphic-task2', 'figure'),
    [dash.dependencies.Input('country_selection', 'value'),
     dash.dependencies.Input('indicator_selection', 'value'),
     dash.dependencies.Input('unit_selection', 'value')])

def update_graph(country_name, indicator_name, unit_value):
    
    dff = df_cleaned[(df_cleaned['GEO'] == country_name) 
                     & (df_cleaned['NA_ITEM'] == indicator_name)
                     & (df_cleaned['UNIT'] == unit_value)]   # filter by country, indicator and unit

    
    return {
        'data': [go.Scatter(
            x=dff['TIME'].unique(),
            y=dff['Value'],
            text=dff["Value"],
            mode='lines'
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Years'
            },
            yaxis={
                'title': indicator_name
            },
            margin={'l': 90, 'b': 70, 't': 70, 'r': 90},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

if __name__ == '__main__':
    app.run_server()


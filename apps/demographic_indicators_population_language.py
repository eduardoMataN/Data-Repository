
import pandas as pd
import plotly.express as px
import dash as dash
from dash import dcc, ctx
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pathlib
from app import app
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from apps.common_items import *

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_population= pd.read_excel(DATA_PATH.joinpath("Population by Language Spoken by County.xlsx"))
df_population['Value']=pd.to_numeric(df_population['Value'])
df_total= pd.read_excel(DATA_PATH.joinpath("Total Population.xlsx"))
df_total['Value']=pd.to_numeric(df_total['Value'])
df_pop_race=pd.read_excel(DATA_PATH.joinpath("Population Race.xlsx"))
df_pop_race['Population']=pd.to_numeric(df_pop_race['Population'])
df_fert=pd.read_excel(DATA_PATH.joinpath("Fertility Rates.xlsx"))

layout=html.Div(children=[
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.H2(children=['Population by Language Spoken'], style={'color':'#041E42'}), 
                TILE_HR
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['County'], style={'font-weight':'bold'}), # type: ignore
                    dcc.Dropdown(id='select-county-pop', # type: ignore
                        options=[{'label':x, 'value':x} for x in sorted(df_population.County.unique())],
                        multi=False,
                        value=df_population['County'].unique()[0],
                        optionHeight=90),
                        html.Br()
                ])
            ]),
            dbc.Col([
                html.Div([
                html.Label(['Language Spoken'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-language-pop',
                options=[{'label':x, 'value':x} for x in sorted(df_population.Language.unique())],
                multi=False,
                value=df_population['Language'].unique()[0],
                optionHeight=90)
                ]),
                
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='population-graph',
                          figure={})
            ]),
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Units: Individuals', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Last Update: March 2020', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Source: USA Gov', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-language', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-language')
            ],  style={'margin-left': '0px', 'margin-right':'1px'})
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ])
])

@app.callback(
    Output('download-language','data'),
    Input('download-bttn-language', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_population.to_excel, 'Population by Language Spoken.xlsx')

@app.callback(
    Output(component_id='population-graph', component_property='figure'),
    [Input(component_id='select-county-pop', component_property='value'),
    Input(component_id='select-language-pop', component_property='value')]
)
def generate_chart(county1, language1):
    dfpop1=df_population.copy()
    dfpop1=dfpop1[(dfpop1['County']==county1)&(dfpop1['Language']==language1)]
    fig_line=px.line(dfpop1, x='Year', y='Value', color='Age')
    fig_line.update_xaxes(rangeslider_visible=True)
    
    return fig_line
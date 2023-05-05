
import pandas as pd
import plotly.express as px
import dash as dash
from dash import dcc, ctx
from dash import html, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pathlib
from app import app
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from apps.common_items import *
from apps.dataset import *
from apps.dataBag import *

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_ep=pd.read_excel(DATA_PATH.joinpath('El Paso Passengers 2012-2022.xlsx'))

layout=html.Div([
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(['El Paso Passengers Statistics'], style=TITLE),
                    TILE_HR
                ])
            ])
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Year'], style=LABEL),
                    dcc.Dropdown(
                        id='select-year-airep',
                        options=[{'label':x, 'value':x}for x in df_ep['Year'].unique()],
                        value=df_ep['Year'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ])
        ]),
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='bar-air',
                        figure={}
                    )
                ])
            ])
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P(' Units: Individuals', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Last Update: June 2022', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Source: USA Gov', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-air2', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-air2')
            ],  style={'margin-left': '0px', 'margin-right':'1px'})
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ]),
])

@app.callback(
    Output('download-air2','data'),
    Input('download-bttn-air2', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_ep.to_excel, 'El Paso Passengers Statistics.xlsx')

@app.callback(
    Output('bar-air', 'figure'),
    Input('select-year-airep', 'value')
)
def update_data(yearEP):
    dff=df_ep.copy()
    dff=dff[dff['Year']==yearEP]
    fig=px.bar(dff, 'Month', 'Value', color='Type', color_discrete_sequence=get_colors(dff['Type'].unique()))
    
    return fig
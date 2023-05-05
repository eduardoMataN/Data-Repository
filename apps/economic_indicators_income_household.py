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
from apps.dataset import *
from apps.dataBag import *


PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets/Income").resolve() #Once we're on that path, we go into datasets
df_income= pd.read_excel(DATA_PATH.joinpath("Household_Family Income by Zip Code.xlsx"))
df_income_copy=df_income.copy()
#incomeDataset=dataset('Median Household & Personal Income Chart', df_median, 'Income', 'income', 'Indicator', 'Income')
#incomeDataset.modify_percent_change(['County', 'Household Type', 'Industry', 'Indicator'], 'County', 'Income')
df_income_zip=df_income_copy[~df_income_copy['ZIP'].isin(['Texas', 'El Paso County, Texas'])]
df_overall=df_income[df_income['ZIP'].isin(['Texas', 'El Paso County, Texas'])]

layout=html.Div([
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(id='households-title', children=['Household Family Income by Zip Code'], style={'color':'#041E42'})
                ])
            ),
            html.Hr(style=HR)
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label('Zip Code', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-zip',
                    options=[{'label':x, 'value':x} for x in df_income_zip['ZIP'].unique()],
                    multi=False,
                    value=df_income_zip['ZIP'].tolist()[0],
                    style={'width':'100%'},
                    optionHeight=90)
                    
                ])
            ),
            dbc.Col(
                html.Div([
                    html.Label('Year', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-year',
                    options=[{'label':x, 'value':x} for x in df_income_zip['Year'].unique()],
                    multi=False,
                    value=df_income_zip['Year'].tolist()[0],
                    style={'width':'100%'},
                    optionHeight=90)
                    
                ])
            )
            
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='pie-income', figure={})
                ])
            )
            
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='pie-ep', figure={})
                ])
            ),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='pie-tx', figure={})
                ])
            )
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P(' Units: Dollars ($)', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Last Update: 2020', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Source: USA Gov', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                html.Div([
                    dbc.Button('Download Dataset', id='download-bttn-income2', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ]),
                dcc.Download(id='download-income2')
            ],  style={'margin-left': '0px', 'margin-right':'1px'}, width=2)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ])
])
@app.callback(
    Output('download-income2','data'),
    Input('download-bttn-income2', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB):

    return dcc.send_data_frame(df_income.to_excel, 'Household Family Income by Zip Code.xlsx')

@app.callback(
    [Output(component_id='pie-income', component_property='figure'),
    Output(component_id='pie-ep', component_property='figure'), Output(component_id='pie-tx', component_property='figure')],
    [Input(component_id='select-zip', component_property='value'), 
    Input(component_id='select-year', component_property='value'),
    ]
)
def update_pie(zip, year):
    dff=df_income.copy()
    df_zip=dff[~dff['ZIP'].isin(['Texas', 'El Paso County, Texas'])]
    df_overall=dff[dff['ZIP'].isin(['Texas', 'El Paso County, Texas'])]
    


    df_zip=df_zip[(df_zip['ZIP']==zip) & (df_zip['Year']==year)]
    
    df_ep=df_overall[(df_overall['ZIP']== 'El Paso County, Texas') & (df_overall['Year']==year)]
    df_tx=df_overall[(df_overall['ZIP']== 'Texas') & (df_overall['Year']==year)]
    fig=px.pie(df_zip, values='Income', names='HouseholdsTypes')
    
    fig_ep=px.pie(df_ep, values='Income', names='HouseholdsTypes', title='El Paso Households Income', color_discrete_sequence=px.colors.sequential.Sunset)
    fig_tx=px.pie(df_tx, values='Income', names='HouseholdsTypes', title='Texas Household Income', color_discrete_sequence=px.colors.sequential.Sunset)
    
    return fig,  fig_ep, fig_tx
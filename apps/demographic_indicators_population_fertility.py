
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
DATA_PATH = PATH.joinpath("../datasets/Population").resolve() #Once we're on that path, we go into datasets. 
df_population= pd.read_excel(DATA_PATH.joinpath("Population by Language Spoken by County.xlsx"))
df_population['Value']=pd.to_numeric(df_population['Value'])
df_total= pd.read_excel(DATA_PATH.joinpath("Total Population.xlsx"))
df_total['Value']=pd.to_numeric(df_total['Value'])
df_pop_race=pd.read_excel(DATA_PATH.joinpath("Population Race.xlsx"))
df_pop_race['Population']=pd.to_numeric(df_pop_race['Population'])
df_fert=pd.read_excel(DATA_PATH.joinpath("Fertility Rates.xlsx"))

layout=html.Div([
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(children=['Fertility Rates'], style={'color':'#041E42'}),
                    TILE_HR
                ])
                
            )
        ]),
        dbc.Row([
            dbc.Col([
                html.Label(['County'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-county-fert',
                    options=[{'label':x, 'value':x} for x in sorted(df_fert.County.unique())],
                    multi=False,
                    value=df_fert['County'].unique()[0],
                    style={'width':'100%'},
                    optionHeight=90)
            ]),
            dbc.Col([
                html.Label(['Year'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-year-fert',
                    options=[{'label':x, 'value':x}for x in sorted(df_fert.Year.unique())],
                    multi=False,
                    value=df_fert.Year.unique()[0],
                    style={'width':'100%'},
                    optionHeight=90)
            ]),
            dbc.Col([
                html.Label(['County'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-county-fert2',
                    options=[{'label':x, 'value':x} for x in sorted(df_fert.County.unique())],
                    multi=False,
                    value=df_fert['County'].unique()[1],
                    style={'width':'100%'},
                    optionHeight=90)
            ])
            
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='pie-fert-1', figure={})
                ])
            ),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='pie-fert-2', figure={})
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
                        dbc.Button('Download Dataset', id='download-bttn-fertility', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-fertility')
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
    Output('download-fertility','data'),
    Input('download-bttn-fertility', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_fert.to_excel, 'Fertility Rates.xlsx')

@app.callback(
    [Output(component_id='pie-fert-1', component_property='figure'),
    Output(component_id='pie-fert-2', component_property='figure')],
    [Input(component_id='select-county-fert', component_property='value'),
    Input(component_id='select-year-fert', component_property='value'),
    Input(component_id='select-county-fert2', component_property='value')]
)
def update_pie_charts(countyF, yearF, countyF2):
    df_pie1=df_fert.copy()
    df_pie1=df_pie1[(df_pie1['County']==countyF) & (df_pie1['Year']==yearF)]
    fig=go.Figure(data=[go.Pie(labels=df_pie1['Age'], values=df_pie1['Percentage'])])

    df_pie2=df_fert.copy()
    df_pie2=df_pie2[(df_pie2['County']==countyF2) & (df_pie2['Year']==yearF)]
    fig2=go.Figure(data=[go.Pie(labels=df_pie2['Age'], values=df_pie2['Percentage'])])
    return fig, fig2
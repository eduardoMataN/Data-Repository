
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
                    ALIGN_LABEL,
                    html.H2(children=['Population By Race'], style={'color':'#041E42'}),
                    TILE_HR
                ]),
                
            ),
            dbc.Col([
                html.Label(['County'], style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-county-race',
                        options=[{'label':x, 'value':x} for x in sorted(df_pop_race.County.unique())],
                        multi=False,
                        value=df_pop_race['County'].unique()[0],
                        style={'width':'100%'},
                        optionHeight=90)
            ]),
            dbc.Col([
                html.Label(['Year'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-year-race',
                options=[{'label':x, 'value':x}for x in sorted(df_pop_race.Year.unique())],
                multi=False,
                value=df_pop_race.Year.unique()[0],
                style={'width':'100%'},
                optionHeight=90)
            ])
        ]),
        dbc.Row([
            dbc.Col(
                html.H4(children=['White Alone'], style={'color':'#FF8200', 'textAlign': 'center'})
            ),
            dbc.Col(
                html.H4(children=['Black or African American Alone'], style={'color':'#FF8200', 'textAlign': 'center'})
            ),
            dbc.Col(
                html.H4(children=['American Indian and Alaska Native Alone'], style={'color':'#FF8200', 'textAlign': 'center'})
            )
        ]),
        dbc.Row([
            dbc.Col(
                daq.Gauge(
                    id='gauge-white',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True,
                    color="#00008B"
                )
            ),
            dbc.Col(
                daq.Gauge(
                    id='gauge-black',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True,
                    color="#00008B"
                )
            ),
            dbc.Col(
                daq.Gauge(
                    id='gauge-indian',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True,
                    color="#00008B"
                )
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.H4(children=['Asian Alone'], style={'color':'#FF8200', 'textAlign': 'center'})
            ),
            dbc.Col(
                html.H4(children=['Native Hawaiian and Other Pacific Islander Alone'], style={'color':'#FF8200', 'textAlign': 'center'})
            ), 
            dbc.Col(
                html.H4(children=['Some other race alone'], style={'color':'#FF8200', 'textAlign': 'center'})
            )
        ]),
        dbc.Row([
            dbc.Col(
                daq.Gauge(
                    id='gauge-asian',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True,
                    color="#00008B"
                )
            ),
            dbc.Col(
                daq.Gauge(
                    id='gauge-hawai',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True,
                    color="#00008B"
                )
            ), 
            dbc.Col(
                daq.Gauge(
                    id='gauge-other',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True,
                    color="#00008B"
                )
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.H4(children=['Two or more races'], style={'color':'#FF8200', 'textAlign': 'center'})
            ),
            dbc.Col(
               html.H4(children=['Two races including some other race'], style={'color':'#FF8200', 'textAlign': 'center'}) 
            ),
            dbc.Col(
                html.H4(children=['Two races excluding some other race, and three or more races'], style={'color':'#FF8200', 'textAlign': 'center'})
            )
        ]),
        dbc.Row([
            dbc.Col(
                daq.Gauge(
                    id='gauge-two',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True,
                    color="#00008B"
                )
            ), 
            dbc.Col(
                daq.Gauge(
                    id='gauge-including',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True,
                    color="#00008B"
                )
            ),
            dbc.Col(
                daq.Gauge(
                    id='gauge-exclude',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True,
                    color="#00008B"
                )
            )
        ]),
        
       
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
                        dbc.Button('Download Dataset', id='download-bttn-race', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-race')
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
    Output('download-race','data'),
    Input('download-bttn-race', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_pop_race.to_excel, 'Population by Race.xlsx')

@app.callback(
    [Output(component_id='gauge-white', component_property='value'), Output(component_id='gauge-white', component_property='max'), Output(component_id='gauge-white', component_property='min'),
    Output(component_id='gauge-black', component_property='value'), Output(component_id='gauge-black', component_property='max'), Output(component_id='gauge-black', component_property='min'),
    Output(component_id='gauge-indian', component_property='value'), Output(component_id='gauge-indian', component_property='max'), Output(component_id='gauge-indian', component_property='min'),
    Output(component_id='gauge-asian', component_property='value'), Output(component_id='gauge-asian', component_property='max'), Output(component_id='gauge-asian', component_property='min'),
    Output(component_id='gauge-hawai', component_property='value'), Output(component_id='gauge-hawai', component_property='max'), Output(component_id='gauge-hawai', component_property='min'),
    Output(component_id='gauge-other', component_property='value'), Output(component_id='gauge-other', component_property='max'), Output(component_id='gauge-other', component_property='min'),
    Output(component_id='gauge-two', component_property='value'), Output(component_id='gauge-two', component_property='max'), Output(component_id='gauge-two', component_property='min'),
    Output(component_id='gauge-including', component_property='value'), Output(component_id='gauge-including', component_property='max'), Output(component_id='gauge-including', component_property='min'),
    Output(component_id='gauge-exclude', component_property='value'), Output(component_id='gauge-exclude', component_property='max'), Output(component_id='gauge-exclude', component_property='min')],
    [Input(component_id='select-county-race', component_property='value'),
    Input(component_id='select-year-race', component_property='value')]
)
def update_gauges(countyR, yearR):
    categDic={'White alone':[], 'Black or African American alone':[], 'American Indian and Alaska Native alone':[], 'Asian alone':[], 'Native Hawaiian and Other Pacific Islander alone':[], 'Some other race alone':[], 'Two or more races:':[], 'Two races including Some other race':[], 'Two races excluding Some other race, and three or more races':[]}
    for category in categDic:
        df_race=df_pop_race.copy()
        df_race=df_race[(df_race['County']==countyR) & (df_race['Year']==yearR)]
        dfcount3=df_total.copy()
        dfcount3=dfcount3[(dfcount3['County']==countyR) & (dfcount3['Year']==yearR)]
        categDic[category].append(max(dfcount3['Value']))
        categDic[category].append(min(df_race['Population']))
        df_race=df_race[df_race['Race']==category]
        categDic[category].append(sum(df_race['Population']))
    return categDic['White alone'][2], categDic['White alone'][0], 0, categDic['Black or African American alone'][2], categDic['Black or African American alone'][0], 0, categDic['American Indian and Alaska Native alone'][2], categDic['American Indian and Alaska Native alone'][0], 0, categDic['Asian alone'][2], categDic['Asian alone'][0], 0, categDic['Native Hawaiian and Other Pacific Islander alone'][2], categDic['Native Hawaiian and Other Pacific Islander alone'][0], 0, categDic['Some other race alone'][2], categDic['Some other race alone'][0],0, categDic['Two or more races:'][2],categDic['Two or more races:'][0], 0, categDic['Two races including Some other race'][2], categDic['Two races including Some other race'][0], 0, categDic['Two races excluding Some other race, and three or more races'][2], categDic['Two races excluding Some other race, and three or more races'][0], 0

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
from apps import demographic_indicators_population_language as language
from apps import demographic_indicators_population_race as race
from apps import demographic_indicators_population_fertility as fertility
subSection={'lang': language.layout, 'race':race.layout, 'fertility':fertility.layout}
# type: ignore

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
    html.Br(),
    dbc.Container(children=[
        dcc.Tabs(id='population-tabs', children=[
            dcc.Tab(label='Population by Language Spoken', value='lang', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Population by Race', value='race', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Fertility Rates', value='fertility', style=tab_style, selected_style=tab_selected_style)
        ], value='lang'),
        html.Br(),
        html.Div(id='subMenu-section-population',children=[])
        
    ])
])

@app.callback(
    Output('subMenu-section-population', 'children'),
    Input('population-tabs','value')
)
def update_submenu(tabValue):
    try:
        return subSection[tabValue]
    except:
        return language.layout



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
df_est=pd.read_excel(DATA_PATH.joinpath('Number of Establishments.xlsx'))
stabDataset=dataset('Number of Business Stablishments by Year Chart', df_est, 'Value', 'stablishments', 'County', 'Value', groupMax=True, groupValue=['Year','County'])
toTable=df_est[df_est['Year']==df_est['Year'][0]][['County', 'Period', 'Value']]
df_gdp=pd.read_excel(DATA_PATH.joinpath('GDP by Industry for Border Counties.xlsx'))
gdpDatasetCounty=dataset('GDP by Industry for Border Counties Chart', df_gdp, 'GDP', 'gdpCounty', 'County', 'GDP')
gdpDatasetCounty.modify_percent_change('County','Description', 'GDP')
gdpDatasetIndustry=dataset('GDP by County for Industries Chart', df_gdp, 'GDP', 'gdpDesc', 'County', 'GDP')
gdpDatasetIndustry.modify_percent_change('Description','County', 'GDP')
industryDatabag=dataBag([stabDataset, gdpDatasetIndustry, gdpDatasetCounty])
from apps import economic_indicators_industry_business as business
from apps import economic_indicators_industry_gdp as gdp
subsectionDic={'est':business.layout, 'gdp':gdp.layout}
layout=html.Div(children=[
    html.Br(),
    dbc.Container(children=[
        dcc.Tabs(id='industry-tabs', children=[
            dcc.Tab(label='Number of Establishments by Year', value='est', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='GDP by Industry for Border Counties', value='gdp', style=tab_style, selected_style=tab_selected_style)
        ], value='est'),
        html.Br(),
        html.Div(id='subMenu-section-industry',children=[])
        
    ]),
])

@app.callback(
    Output('subMenu-section-industry', 'children'),
    Input('industry-tabs','value')
)
def update_submenu(tabValue):
    try:
        return subsectionDic[tabValue]
    except:
        return business.layout
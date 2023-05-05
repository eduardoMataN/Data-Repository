
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

from apps import transportation_airport_activity_dom as dom_int
from apps import transportation_airport_activity_ep as ep_pass
from apps import transportation_airport_activity_maps as aiport_maps
PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_domes_int=pd.read_excel(DATA_PATH.joinpath('Jurez & Chihuahua.xlsx'))
df_ep=pd.read_excel(DATA_PATH.joinpath('El Paso Passengers 2012-2022.xlsx'))
subsectionDic={'dom-int':dom_int.layout, 'ep-pass':ep_pass.layout, 'airport_maps':aiport_maps.layout}

layout=html.Div(children=[
    html.Br(),
    dbc.Container(children=[
        dcc.Tabs(id='transportation-tabs', children=[
            dcc.Tab(label='Domestic and International Air Passengers', value='dom-int', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='El Paso Passenger Statistics', value='ep-pass', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Maps', value='airport_maps', style=tab_style, selected_style=tab_selected_style)
        ], value='dom-int'),
        html.Br(),
        html.Div(id='subMenu-section-transportation',children=[])
        
    ])
])

@app.callback(
    Output('subMenu-section-transportation', 'children'),
    Input('transportation-tabs','value')
)
def update_submenu(tabValue):
    try:
        return subsectionDic[tabValue]
    except:
        return dom_int.layout
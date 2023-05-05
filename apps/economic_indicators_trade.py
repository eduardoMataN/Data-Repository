
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
import dash_draggable



PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets/Trade").resolve() #Once we're on that path, we go into datasets. 
df_trade_hs= pd.read_excel(DATA_PATH.joinpath("Imports & Exports by HS Commodities, yearly.xlsx"))
hsImportsDataset=dataset('Imports by HS Commodities Imports Chart', df_trade_hs,'Imports', 'hsImports', 'Port', 'Imports')
hsImportsDataset.modify_percent_change(['Measures', 'Commodity'], 'Port', 'Imports')
hsExportsDataset=dataset('Exports by HS Commodities Imports Chart', df_trade_hs,'Exports', 'hsExports', 'Port', 'Exports')
hsExportsDataset.modify_percent_change(['Measures', 'Commodity'], 'Port', 'Exports')
df_trade_naics=pd.read_excel(DATA_PATH.joinpath("Exports & Imports by NAICS Commodities, yearly.xlsx"))
naicsDataset=dataset('Imports & Exports by NAICS Commodities Chart', df_trade_naics, 'Value', 'naics', 'Commodity', 'Value')
naicsDataset.modify_percent_change(['Commodity', 'Measures'], 'District', 'Value')
#-------------------------------------------------------------------------------------
df_ep=pd.read_excel(DATA_PATH.joinpath("Total Flows to El Paso.xlsx"))
epDataset=dataset('Total Flows to El Paso Chart', df_ep, 'Total', 'totalFlows', 'Commodity', 'Total')
epDataset.modify_percent_change('Mode', 'Commodity', 'Total')
tradeDatabag=dataBag([naicsDataset, hsExportsDataset, hsImportsDataset, epDataset])
from apps import economic_indicators_trade_imports_exports as impExp
from apps import economic_indicators_trade_flows  as epFlows
subsectionDic={'imp-exp':impExp.layout, 'ep-flows':epFlows.layout}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "0rem",
    "margin-right": "0rem",
    "padding": "0rem 0rem",
}

layout=html.Div(children=[
    html.Br(),
    dbc.Container(children=[
        dcc.Tabs(id='trade-tabs', children=[
            dcc.Tab(label='Imports & Exports by HS/NAICS Commodities', value='imp-exp', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Total Flows to El Paso', value='ep-flows', style=tab_style, selected_style=tab_selected_style)
        ], value='imp-exp'),
        html.Br(),
        html.Div(id='subMenu-section-trade',children=[])
        
    ])
])

@app.callback(
    Output('subMenu-section-trade', 'children'),
    Input('trade-tabs','value')
)
def update_submenu(tabValue):
    try:
        return subsectionDic[tabValue]
    except:
        return impExp.layout







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
from dash.exceptions import PreventUpdate
DATA_PATH = PATH.joinpath("../datasets/Apprehensions").resolve()

df_cit=pd.read_excel(DATA_PATH.joinpath('Apprehensions by Citizenship.xlsx'))
df_cit_per=df_cit.copy()
df_cit_per['Apprehensions']=df_cit_per['Apprehensions'].pct_change()
citDataset=dataset('Yearly Apprehensions by Citizenship Chart', df_cit, 'Apprehensions','tab-cit', 'Citizenship', 'Apprehensions', 'Citizenship')
citDataset.modify_percent_change('Sector', 'Citizenship', 'Apprehensions')

df_country=pd.read_excel(DATA_PATH.joinpath('Apprehensions by Country.xlsx'))
df_country_per=df_country.copy()
df_country_per['Illegal Alien Apprehensions']=df_country_per['Illegal Alien Apprehensions'].pct_change()
countryDataset=dataset('Yearly Apprehensions by Country Chart', df_country, 'Illegal Alien Apprehensions', 'tab-country', 'Country', 'Illegal Alien Apprehensions')
countryDataset.modify_percent_change('Sector', 'Country', 'Illegal Alien Apprehensions')



df_uac=pd.read_excel(DATA_PATH.joinpath('Monthly UAC Apprehensions by Sector.xlsx'))
aucDataset=dataset('AUC Monthly Apprehensions Chart', df_uac, 'Unaccompanied Alien Children Apprehended', 'auc-app', 'Sector', 'Unaccompanied Alien Children Apprehended')

df_family=pd.read_excel(DATA_PATH.joinpath('Monthly Family Unit Apprehensions.xlsx'))
familyDataset=dataset('Family Unit Monthly Apprehensions by Sector Chart', df_family, 'Total','family-unit', 'Sector', 'Total')

df_southwesta=pd.read_excel(DATA_PATH.joinpath('Southwest Border Apprehensions.xlsx'))
southwestAppDataset=dataset('Southwest Border Apprehensions Chart',df_southwesta, 'Total', 'apps', 'Sector', 'Total')

df_southwestb=pd.read_excel(DATA_PATH.joinpath('Southwest Border Deaths.xlsx'))
southwestDeathDataset=dataset('Southwest Border Deaths Chart',df_southwestb, 'Deaths', 'deaths', 'Sector', 'Deaths')



show_sidebar=True
from apps import border_security_yApprehensions as yearly
from apps import border_security_mApprehensions  as monthly
from apps import border_security_SWapprehensions as southwest
subsectionDic={'yearly':yearly.layout, 'monthly':monthly.layout, 'southwest':southwest.layout}



layout=html.Div([
    html.Br(),
    dbc.Container(children=[
        dcc.Tabs(id='border-tabs', children=[
            dcc.Tab(label='Yearly Apprehensions by Sector', value='yearly', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Monthly Apprehensions by Sector', value='monthly', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Southwest Border', value='southwest', style=tab_style, selected_style=tab_selected_style)
        ], value='yearly'),
        html.Br(),
        html.Div(id='subMenu-section-app',children=[])
        
    ])
])

@app.callback(
    Output('subMenu-section-app', 'children'),
    Input('border-tabs','value')
)
def update_submenu(tabValue):
    try:
        return subsectionDic[tabValue]
    except:
        return yearly.layout








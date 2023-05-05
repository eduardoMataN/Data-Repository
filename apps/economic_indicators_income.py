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
DATA_PATH = PATH.joinpath("../datasets/Income").resolve() #Once we're on that path, we go into datasets. 
df_income= pd.read_excel(DATA_PATH.joinpath("Household_Family Income by Zip Code.xlsx"))
df_median=pd.read_excel(DATA_PATH.joinpath("Median Household income.xlsx")) #Might have to divide this. 
df_median_personal=df_median[df_median['Indicator']=='Personal Per Capita Income']
df_personal=df_median_personal.copy()
df_median_industry=df_median[df_median['Indicator']=='Earnings by Industry']
df_industry=df_median_industry.copy()
df_median_median=df_median[df_median['Indicator']=='Median Household Income']
df_median_final=df_median_median.copy()
personalDataset=dataset('Personal Per Capita Income Chart', df_personal, 'Income', 'Personal Per Capita Income', 'County', 'Income')
industryDataset=dataset('Earnings by Industry Chart', df_industry, 'Income', 'Earnings by Industry', 'County', 'Income')
industryDataset.modify_percent_change('Industry', 'County', 'Income')
medianDataset=dataset('Median Household Income Chart', df_median_final, 'Income', 'Median Household Income', 'County', 'Income')
medianDataset.modify_percent_change('Household Type', 'County', 'Income')


df_income_copy=df_income.copy()
#incomeDataset=dataset('Median Household & Personal Income Chart', df_median, 'Income', 'income', 'Indicator', 'Income')
#incomeDataset.modify_percent_change(['County', 'Household Type', 'Industry', 'Indicator'], 'County', 'Income')
df_income_zip=df_income_copy[~df_income_copy['ZIP'].isin(['Texas', 'El Paso County, Texas'])]
df_overall=df_income[df_income['ZIP'].isin(['Texas', 'El Paso County, Texas'])]
df_revenues=pd.read_excel(DATA_PATH.joinpath('Revenues by Workers Remittances, Distribution by municipality, Chihuahua, Juárez.xlsx'))
revenuesDataset=dataset('Revenues by Workers Remittances Chart', df_revenues, 'Dollars in Millions', name='revenues')
maxYear=df_income['Year'].max()
incomeDatabag=dataBag([personalDataset, medianDataset, industryDataset, revenuesDataset])
df_median=pd.read_excel(DATA_PATH.joinpath("Median Household income.xlsx"))

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
from apps import economic_indicators_income_median as median
from apps import economic_indicators_income_household  as household
subsectionDic={'median':median.layout, 'household':household.layout}

layout=html.Div(children=[
    html.Br(),
    dbc.Container(children=[
        dcc.Tabs(id='income-tabs', children=[
            dcc.Tab(label='Median Household & Personal Income', value='median', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Household Family Income by Zip Code', value='household', style=tab_style, selected_style=tab_selected_style)
        ], value='median'),
        html.Br(),
        html.Div(id='subMenu-section-income',children=[])
        
    ])
])

@app.callback(
    Output('subMenu-section-income', 'children'),
    Input('income-tabs','value')
)
def update_submenu(tabValue):
    try:
        return subsectionDic[tabValue]
    except:
        return median.layout










        







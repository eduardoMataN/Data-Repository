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
#Dataframe is created from excel data file. An object of the dataset class is created.
df_uac=pd.read_excel(DATA_PATH.joinpath('Monthly UAC Apprehensions by Sector.xlsx'))
aucDataset=dataset('AUC Monthly Apprehensions Chart', df_uac, 'Unaccompanied Alien Children Apprehended', 'auc-app', 'Sector', 'Unaccompanied Alien Children Apprehended')

df_family=pd.read_excel(DATA_PATH.joinpath('Monthly Family Unit Apprehensions.xlsx'))
familyDataset=dataset('Family Unit Monthly Apprehensions by Sector Chart', df_family, 'Total','family-unit', 'Sector', 'Total')
monthlyBag=dataBag([aucDataset, familyDataset])

layout=html.Div([
    html.Div(id='sidebar-space-mApp',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-mApp',children='Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-mApp',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        dcc.Input(id='max_input_mApp', type='number', min=10, max=1000, value=150),
        html.Label('Min Y Value:', style=LABEL),
        dcc.Input(id='min_input_mApp', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-mApp', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)
    ],
    style=SIDEBAR_STYLE,
    )
    ], hidden=True),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(id='mApp-title',children=['Monthly Apprehensions by Sector'], style=TITLE)
                ])
            ])
        ]),
        html.Hr(style={'color':blue, 'borderWidth': "0.3vh", 'borderColor':blue, 'opacity':'unset', 'width':'100%'})
    ]),
    dbc.Container([
        dcc.Tabs(id='monthly-tabs', value='family-unit', children=[
            dcc.Tab(label='Family Unit Apprehensions', value='family-unit', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='AUC Apprehensions', value='auc-app', style=tab_style, selected_style=tab_selected_style)
        ])
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Sector'], style=LABEL),
                    dcc.Dropdown(
                        id='sector-monthly',
                        options=get_options(df_family,'Sector'),
                        value=df_family['Sector'].unique()[0],
                        multi=False,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-monthly', outline=True, color="primary", className="me-1", value='monthly')
                ])
            ], width=2),
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='monthly-graph',
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
                        html.P('Last Update: 2019', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Source: USA Gov', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-app-2', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-app-2')
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
    Output('download-app-2','data'),
    [Input('download-bttn-app-2', 'n_clicks'),
    Input('monthly-tabs', 'value')],
    prevent_initial_call=True
)
def download_median(downloadB, tab): 
    trigger_id=ctx.triggered_id 
    if(trigger_id=='monthly-tabs'):
        raise PreventUpdate
    else:
        if(tab=='family-unit'):
            return dcc.send_data_frame(df_family.to_excel, 'Monthly Family Unit Apprehensions by Sector.xlsx')
        else:
            return dcc.send_data_frame(df_uac.to_excel, 'Monthly UUC Apprehensions by Sector.xlsx')

@app.callback(
    [Output('sidebar-space-mApp','hidden'),
    Output('sidebar-title-mApp','children'),
    Output('max_input_mApp', 'max'),
    Output('max_input_mApp', 'min'),
    Output('min_input_mApp', 'max'),
    Output('min_input_mApp','min'),
    Output('max_input_mApp','value'),
    Output('min_input_mApp','value')],
    [
    Input('edit-monthly','n_clicks'),
    Input('monthly-tabs', 'value'),
    Input('sidebar-space-mApp','hidden'),
    Input('sidebar-title-mApp', 'children'),
    Input('reset-mApp','n_clicks'),
    Input('sector-monthly','value'),
    Input('max_input_mApp','value'),
    Input('min_input_mApp','value')]
)
def get_sidebar(monthlyButton, monthlyTab, sideBarShow, title, reset, filterValue, max, min):
    trigger_id=ctx.triggered_id 
    monthlyBag.getByName(monthlyTab).adjustMinMax('Sector', filterValue)   
    if(trigger_id=='select-sector'):
        monthlyBag.getByName(monthlyButton).adjustMinMax('Sector', filterValue)
        
            
    if(trigger_id=='edit-monthly'):
        currentDataset=monthlyBag.getByName(monthlyTab)
        newTitle=currentDataset.title
        if(sideBarShow):
            sideBarShow=False
        elif(title==newTitle):
            sideBarShow=True
        
        title=newTitle
        
    
        
    if(trigger_id=='monthly-tabs'):
        currentDataset=monthlyBag.getByName(monthlyTab)
        title=currentDataset.title
    currentDataset=monthlyBag.getDataframe(title)
    currMin=currentDataset.min
    currMax=currentDataset.max
    if(currentDataset.isTrimmed()):
        currentValueMax=currentDataset.trimMax
        currentValueMin=currentDataset.trimMin
        minMax=currentDataset.trimMax-1
        maxMin=currentDataset.trimMin+1
    else:
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        minMax=currentDataset.max-1
        maxMin=currentDataset.min+1
    if(trigger_id=='reset-mApp'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        sideBarShow=False
    if(trigger_id=='max_input_mApp' or trigger_id=='min_input_mApp'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        sideBarShow=False
    
    
    
        
    
    

         
    return sideBarShow, title, currMax, maxMin, minMax, currMin, currentValueMax, currentValueMin

@app.callback(
    Output('mApp-title','children'),
    [Input('mApp-title','children'),
    Input('chart-options-mApp','value'),
    Input('sidebar-title-mApp','children'),
    Input('reset-mApp','n_clicks'),
    Input('max_input_mApp','value'),
    Input('min_input_mApp','value')]
)
def change_chart(title, chartMode, sideBarTitle, reset, max, min):
    trigger_id=ctx.triggered_id
    monthlyBag.getDataframe(sideBarTitle).activateDataframe(chartMode)
    if(trigger_id=='max_input_mApp' or trigger_id=='min_input_mApp'):
        monthlyBag.getDataframe(sideBarTitle).trim(max, min)
    if(trigger_id=='reset-mApp'):
        monthlyBag.getDataframe(sideBarTitle).reset()
    return title
@app.callback(
    [
    Output('sector-monthly','options'),
    Output('sector-monthly','value'),
    Output('monthly-graph','figure')
    ],
    [
    Input('monthly-tabs', 'value'),
    Input('sector-monthly', 'options'),
    Input('sector-monthly','value'),
    Input('chart-options-mApp','value'),
    Input('max_input_mApp','value'),
    Input('min_input_mApp','value'),
    Input('reset-mApp','n_clicks')]
)
def update_data(monthlyTab, monthlyOptions, monthlyValue,  chartType, dummyMax, dummyMin, dummyReset):
    trigger_id=ctx.triggered_id
    #Chunk for section 2:
    if(monthlyTab=='family-unit'):
        dff2=monthlyBag.getByName(monthlyTab).getActive().copy()
        if(trigger_id=='monthly-tabs'):
            monthlyOptions=get_options(dff2, 'Sector')
            monthlyValue=dff2['Sector'].unique()[0]
        fig2=px.line(filter_df(dff2, 'Sector',monthlyValue), x='Date', y='Total')
        fig2.update_traces(line_color='#FF8200')
    if(monthlyTab=='auc-app'):
        dff2=monthlyBag.getByName(monthlyTab).getActive().copy()
        if(trigger_id=='monthly-tabs'):
            monthlyOptions=get_options(dff2, 'Sector')
            monthlyValue=dff2['Sector'].unique()[0]
        fig2=px.line(filter_df(dff2, 'Sector', monthlyValue), x='Date', y='Unaccompanied Alien Children Apprehended')
        fig2.update_traces(line_color='#FF8200')
    if(monthlyBag.getByName(monthlyTab).get_active_mode()=='Original'):
        nothing='nothing'
    else:
        fig2.update_yaxes(ticksuffix='%')
    fig2.update_xaxes(rangeslider_visible=True)
    
    
    fig2.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig2.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>", tickangle=45)
    return  monthlyOptions, monthlyValue, fig2

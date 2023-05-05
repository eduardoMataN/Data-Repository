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

df_southwesta=pd.read_excel(DATA_PATH.joinpath('Southwest Border Apprehensions.xlsx'))
southwestAppDataset=dataset('Southwest Border Apprehensions Chart',df_southwesta, 'Total', 'apps', 'Sector', 'Total')

df_southwestb=pd.read_excel(DATA_PATH.joinpath('Southwest Border Deaths.xlsx'))
southwestDeathDataset=dataset('Southwest Border Deaths Chart',df_southwestb, 'Deaths', 'deaths', 'Sector', 'Deaths')

southBag=dataBag([southwestAppDataset, southwestDeathDataset])

layout=html.Div([
    html.Div(id='sidebar-space-sApp',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-sApp',children='Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-sApp',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        dcc.Input(id='max_input_sApp', type='number', min=10, max=1000, value=150),
        html.Label('Min Y Value:', style=LABEL),
        dcc.Input(id='min_input_sApp', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-sApp', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)
    ],
    style=SIDEBAR_STYLE,
    )
    ], hidden=True),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(id='sApp-title',children=['Southwest Border'], style=TITLE)
                ])
            ])
        ]),
        html.Hr(style={'color':blue, 'borderWidth': "0.3vh", 'borderColor':blue, 'opacity':'unset', 'width':'100%'})
    ]),
    dbc.Container([
        dcc.Tabs(id='south-tabs', value='apps', children=[
            dcc.Tab(label='Apprehensions', value='apps', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Deaths', value='deaths', style=tab_style, selected_style=tab_selected_style)
        ])
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Sector'], style=LABEL),
                    dcc.Dropdown(
                        id='south-sector',
                        options=get_options(df_southwesta, 'Sector'),
                        value=df_southwesta['Sector'].unique()[0],
                        multi=False,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-southwest', outline=True, color="primary", className="me-1", value='southwest')
                ])
            ], width=2),
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='south-graph',
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
                        html.P('Last Update: 2018', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Source: USA Gov', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-app-3', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-app-3')
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
    Output('download-app-3','data'),
    [Input('download-bttn-app-3', 'n_clicks'),
    Input('south-tabs', 'value')],
    prevent_initial_call=True
)
def download_median(downloadB, tab): 
    trigger_id=ctx.triggered_id 
    if(trigger_id=='south-tabs'):
        raise PreventUpdate
    else:
        if(tab=='apps'):
            return dcc.send_data_frame(df_southwesta.to_excel, 'Southwest Border Apprehensions by Sector.xlsx')
        else:
            return dcc.send_data_frame(df_southwestb.to_excel, 'Southwest Border Deaths by Sector.xlsx')
@app.callback(
    [Output('sidebar-space-sApp','hidden'),
    Output('sidebar-title-sApp','children'),
    Output('max_input_sApp', 'max'),
    Output('max_input_sApp', 'min'),
    Output('min_input_sApp', 'max'),
    Output('min_input_sApp','min'),
    Output('max_input_sApp','value'),
    Output('min_input_sApp','value')],
    [
    Input('sidebar-space-sApp','hidden'),
    Input('edit-southwest','n_clicks'),
    Input('south-tabs','value'),
    Input('sidebar-title-sApp', 'children'),
    Input('reset-sApp','n_clicks'),
    Input('south-sector','value'),
    Input('max_input_sApp','value'),
    Input('min_input_sApp','value')]
)
def get_sidebar(sideBarShow, southButton, southTabs, title, reset, filterValue, max, min):
    trigger_id=ctx.triggered_id    
    if(trigger_id=='south-sector'):
        southBag.getByName(southTabs).adjustMinMax('Sector', filterValue)
        
    if(trigger_id=='edit-southwest'):
        currentDataset=southBag.getByName(southTabs)
        newTitle=currentDataset.title
        if(sideBarShow):
            sideBarShow=False
        elif(title==newTitle):
            sideBarShow=True
        title=newTitle
        
    if(trigger_id=='south-tabs'):
        currentDataset=southBag.getByName(southTabs)
        title=currentDataset.title
    currentDataset=southBag.getDataframe(title)
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
    if(trigger_id=='reset-sApp'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        sideBarShow=False
    if(trigger_id=='max_input_app' or trigger_id=='min_input_app'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        sideBarShow=False
    if(trigger_id=='reset-sApp'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        sideBarShow=False
    if(trigger_id=='max_input_app' or trigger_id=='min_input_app'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        sideBarShow=False
         
    return sideBarShow, title, currMax, maxMin, minMax, currMin, currentValueMax, currentValueMin
@app.callback(
    Output('sApp-title','children'),
    [Input('sApp-title','children'),
    Input('chart-options-sApp','value'),
    Input('sidebar-title-sApp','children'),
    Input('reset-sApp','n_clicks'),
    Input('max_input_sApp','value'),
    Input('min_input_sApp','value')]
)
def change_chart(title, chartMode, sideBarTitle, reset, max, min):
    trigger_id=ctx.triggered_id
    southBag.getDataframe(sideBarTitle).activateDataframe(chartMode)
    if(trigger_id=='max_input_app' or trigger_id=='min_input_app'):
        southBag.getDataframe(sideBarTitle).trim(max, min)
    if(trigger_id=='reset-sApp'):
        southBag.getDataframe(sideBarTitle).reset()
    return title

@app.callback(
    [
    Output('south-sector','options'),
    Output('south-sector','value'),
    Output('south-graph','figure'),
    ],
    [
    Input('south-tabs','value'),
    Input('south-sector','options'),
    Input('south-sector','value'),
    Input('chart-options-sApp','value'),
    Input('max_input_sApp','value'),
    Input('min_input_sApp','value'),
    Input('reset-sApp','n_clicks')]
)
def update_data(southTab, southOptions, southValue, chartType, dummyMax, dummyMin, dummyReset):
    trigger_id=ctx.triggered_id
    
    #Chunk for section 3:
    if(southTab=='apps'):
        dff3=southBag.getByName(southTab).getActive().copy()
        if(trigger_id=='south-tabs'):
            southOptions=get_options(dff3, 'Sector')
            southValue=dff3['Sector'].unique()[0]
        fig3=px.line(filter_df(dff3,'Sector',southValue), x='Fiscal Year', y='Total')
        fig3.update_traces(line_color='#FF8200')
    if(southTab=='deaths'):
        dff3=southBag.getByName(southTab).getActive().copy()
        if(trigger_id=='south-tabs'):
            southOptions=get_options(dff3, 'Sector')
            southValue=dff3['Sector'].unique()[0]
        fig3=px.line(filter_df(dff3, 'Sector', southValue), x='Year', y='Deaths')
        fig3.update_traces(line_color='#FF8200')
    fig3.update_xaxes(rangeslider_visible=True)
    if(southBag.getByName(southTab).get_active_mode()=='Original'):
        nothing='nothing'
    else:
        fig3.update_yaxes(ticksuffix='%')
    
    fig3.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return southOptions, southValue, fig3
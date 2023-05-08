
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
DATA_PATH = PATH.joinpath("../datasets/Crime").resolve() #Once we're on that path, we go into datasets. 
df_crime=pd.read_excel(DATA_PATH.joinpath('Crime 2006 - 2019.xlsx'))
crimeDataset=dataset('Crime by County Chart', df_crime, 'Number', 'crime', 'County', 'Number')
crimeDataset.modify_percent_change('Crime Desctiption', 'County', 'Number')
crimeDatabag=dataBag([crimeDataset])


layout=html.Div(children=[
    html.Div(id='sidebar-space-crime',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-crime',children='Crime By County'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-crime',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        


        
    ],
    style=SIDEBAR_STYLE,
    )
    ], hidden=True, style={'z-index':'999'}),
    dbc.Container(children=[
    html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(children=['Crime by County'], style={'color':'#041E42'})
                ])
            ]),
            html.Hr(style=HR)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Type of Crime'], style={'font-weight':'bold', 'color':'#041E42'}),
                    dcc.Dropdown(
                        id='select-type-cr',
                        options=[{'label':x, 'value':x}for x in df_crime['Crime Desctiption'].unique()],
                        value=df_crime['Crime Desctiption'].unique()[0],
                        style={'width':'100%'},
                        optionHeight=90
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label(['County'], style=LABEL),
                    dcc.Dropdown(
                        id='select-county1-cr',
                        options=[{'label':x, 'value':x}for x in df_crime['County'].unique()],
                        value=df_crime['County'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=True
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    COMPARE_LABEL,
                    daq.PowerButton(
                        id='sbs-cr',
                        on=False,
                        labelPosition='top',
                        style=LABEL,
                        color='#FF5E5E'
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    html.Label(['County'], style=LABEL),
                    dcc.Dropdown(
                        id='select-county2-cr',
                        options=[{'label':x, 'value':x}for x in df_crime['County'].unique()],
                        value=df_crime['County'].unique()[-1],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=True
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    ALIGN_LABEL,
                    html.Br(),
                    dbc.Button('Edit Graph', id='edit-crime', outline=True, color="primary", className="me-1", value='edit')
                ])
            ])
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='cr-graph',
                        figure={}
                    )
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
                        html.P(' Units: Crimes', style={'color':blue})
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
                        dbc.Button('Download Dataset', id='download-bttn-crime', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-crime')
            ],  style={'margin-left': '0px', 'margin-right':'1px'}, width=2)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ]),
])
@app.callback(
    Output('download-crime','data'),
    Input('download-bttn-crime', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_crime.to_excel, 'Crime Data.xlsx') 

@app.callback(
    
    Output('sidebar-space-crime', 'hidden'),
    [Input('edit-crime', 'n_clicks'),
    Input('sidebar-space-crime', 'hidden'),
    Input('chart-options-crime', 'value')]
)
def get_sidebar(button, showSideBar, chartMode):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-crime'):
        if(showSideBar):
            showSideBar=False
        else:
            showSideBar=True
    crimeDatabag.getDataframe().activateDataframe(chartMode)
    return showSideBar

@app.callback(
    [
        Output('cr-graph', 'figure'),
        Output('select-county1-cr','disabled'),
        Output('select-county2-cr','disabled')
    ],
    [
        Input('select-type-cr','value'),
        Input('select-county1-cr','value'),
        Input('select-county2-cr', 'value'),
        Input('sbs-cr', 'on'),
        Input('chart-options-crime', 'value')
    ] 
)
def update_data(type, county1, county2, on, dummyValue):
    dff=crimeDatabag.getDataframe().getActive().copy()
    dff=dff[dff['Crime Desctiption']==type]
    d1_dis=True
    d2_dis=True
    if(on==True):
        fig=make_subplots(rows=1, cols=2)
        dff1=dff[dff['County']==county1]
        dff2=dff[dff['County']==county2]
        fig=create_subplot(fig,1,1,dff1,'Year','Number','County')
        fig=create_subplot(fig,1,2,dff2,'Year','Number','County')
        fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=1)
        fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=2)
        
        d1_dis=False
        d2_dis=False
    else:
        fig=px.line(dff,'Year','Number', color='County', color_discrete_sequence=get_colors(dff['County'].unique()))
        fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return fig, d1_dis, d2_dis
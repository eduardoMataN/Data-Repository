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
DATA_PATH = PATH.joinpath("../datasets/Industry").resolve() #Once we're on that path, we go into datasets. 
df_est=pd.read_excel(DATA_PATH.joinpath('Number of Establishments.xlsx'))
df_est_yearly=pd.read_excel(DATA_PATH.joinpath('Number of Establishments by Year.xlsx'))
stabDataset=dataset('Number of Business Stablishments by Year Chart', df_est, 'Value', 'stablishments', 'County', 'Value', groupMax=True, groupValue=['Year','County'])
stabYearly=dataset('Number of Business Stablishments by Year Chart', df_est_yearly, 'Value', 'stablishments', 'County', 'Value')
toTable=df_est[df_est['Year']==df_est['Year'][0]][['County', 'Period', 'Value']]
layout=dbc.Container([
    html.Div(id='sidebar-space-ind-business',children=[
        html.Div([
        html.H6(id='sidebar-title-ind-business',children='Number of Business Stablishments by Year Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-ind-business',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='max_input-ind-business', type='number', min=df_est_yearly['Value'].min()+1, max=df_est_yearly['Value'].max(), value=df_est_yearly['Value'].max()),
        html.Br(),
        html.Label('Min Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='min_input-ind-business', type='number', min=df_est_yearly['Value'].min(), max=df_est_yearly['Value'].max()-1, value=df_est_yearly['Value'].min()),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-ind-business', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)

        ], style=SIDEBAR_STYLE)
        
    
    ], hidden=True),
    dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(id='title-business',children=['Number of Business Stablishments by Year'], style={'color':blue}),
                    html.Hr(style=HR)
                ])
            ),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-stablishments', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            ], width=2),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='line-1', figure={})
            )
            
        ]),
    dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label(['County'], style=LABEL),
                    dcc.Dropdown(
                        id='select-county-ind',
                        options=[{'label':x, 'value':x} for x in df_est['County'].unique()],
                        multi=False,
                        value=df_est['County'].unique()[0],
                        style={'width':'100%'},
                        optionHeight=90            
                    )
            ])
            ),
            dbc.Col([
                html.Div([
                    html.Label(['Year'], style=LABEL),
                    dcc.Dropdown(
                        id='select-year-ind',
                        options=[{'label':x, 'value':x} for x in df_est['Year'].unique()],
                        value=df_est['Year'].unique()[0],
                        style={'width':'100%'},
                        optionHeight=90
                    )
                ])
                    ]),
            
        ]),
        html.Br(),
        dbc.Row(
            dbc.Col([
                html.Div(id='table-loc',children=[
                    dash_table.DataTable(
                        id='industry-table',
                        columns=[{'name':i, 'id':i} for i in toTable.columns],
                        data=toTable.to_dict('records'),
                        editable=True,
                        filter_action='none',
                        sort_action='native',
                        sort_mode='multi',
                        row_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_size=10,
                        style_cell={'font-family':'Arial', 'textAlign':'center'},
                        style_header={'font-family':'Arial'}
                    )
                ])
            ])
        ),
        html.Br(),
        html.Br(),
        dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P(' Units: Dollars ($)', style=INFO_BOX_STYLE)
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P(id='chartmode',children='Last Update: June 2022', style=INFO_BOX_STYLE)
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P(id='experiment',children='Source: USA Gov',style=INFO_BOX_STYLE)
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-ind', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-ind')
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
    Output('download-ind','data'),
    Input('download-bttn-ind', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_est.to_excel, 'Number of Business Stablishments by Year Data.xlsx')
@app.callback(
        Output('sidebar-space-ind-business','hidden'),
        [Input('edit-stablishments', 'n_clicks'),
         Input('sidebar-space-ind-business','hidden')],
         prevent_initial_call=True
)
def display_sidebar(editButton, hideBar):
    if(hideBar):
        return False
    return True
@app.callback(
        [Output('title-business','children'),
        Output('max_input-ind-business','value'),
        Output('min_input-ind-business','value')],
        [Input('chart-options-ind-business','value'),
        Input('max_input-ind-business','value'),
        Input('min_input-ind-business','value'),
        Input('reset-ind-business','n_clicks')]
)
def update_dataset(chartMode, max, min, reset):
    trigger_id=ctx.triggered_id
    stabYearly.activateDataframe(chartMode)
    if(trigger_id=='max_input-ind-business' or trigger_id=='min_input-ind-business'):
        stabYearly.trim(max, min)
    if(trigger_id=='reset-ind-business'):
        stabYearly.reset()
        max=stabYearly.max
        min=stabYearly.min
    return stabYearly.title, max, min
    
@app.callback(
    [Output(component_id='line-1', component_property='figure'),
    Output('industry-table', 'data'), Output('industry-table', 'columns')],
    [Input('select-county-ind', 'value'),
    Input('select-year-ind', 'value'),
    Input('chart-options-ind-business', 'value'),
    Input('max_input-ind-business','value'),
    Input('min_input-ind-business','value'),
    Input('reset-ind-business','n_clicks')]
)
def create_chart(countyValue, yearValue, chartOptions, maxInput, minInput, resetButton):
    trigger_id=ctx.triggered_id
    
    dff=stabDataset.getActive().copy()
    dff1=stabYearly.getActive().copy()
    dff.groupby('Year')
    finalFig=px.line(dff1, x='Year', y='Value', color='County', color_discrete_sequence=get_colors(dff['County'].unique()))
    finalFig.update_xaxes(nticks=len(pd.unique(dff['Year'])))
    finalFig.update_xaxes( rangeslider_visible=True)
    toTable=dff[(dff['Year']==yearValue) & (dff['County']==countyValue)][['County', 'Period', 'Value']]
    finalFig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    finalFig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return finalFig, toTable.to_dict('records'), [{'name':i, 'id':i} for i in toTable.columns]


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
DATA_PATH = PATH.joinpath("../datasets/Migration Indicators").resolve()

df_migration=pd.read_excel(DATA_PATH.joinpath('County to County Migration Flows 2009-2018.xlsx'))
migrationDataset=dataset('Migration Indicators by State Chart', df_migration, 'Value', 'migrationState', 'Migration', 'Value')
migrationDataset.modify_percent_change('State', 'Migration', 'Value')
migrationDatasetCounty=dataset('Migration Indicators by County Chart', df_migration, 'Value', 'migrationCounty', 'Migration', 'Value')
migrationDatasetCounty.modify_percent_change('County', 'Migration', 'Value')
migrationDatabag=dataBag([migrationDataset, migrationDatasetCounty])

layout=html.Div([
    html.Div(id='sidebar-space-migration',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-migration',children='Border Patrol Agent Staffing'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-migration',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        dcc.Input(id='max_input_migration', type='number', min=10, max=1000, value=150),
        html.Label('Min Y Value:', style=LABEL),
        dcc.Input(id='min_input_migration', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-migration', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)


        
    ],
    style=SIDEBAR_STYLE,
    )
    ], hidden=True),
    dbc.Container([
    html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(['Migration Indicators'], style=TITLE)
                ])
            ]),
            html.Hr(style=HR)
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Migration Flow'], style=LABEL),
                    dcc.Dropdown(
                        id='select-flow',
                        options=get_options(df_migration, 'Migration'),
                        value=df_migration['Migration'].unique()[0],
                        multi=False,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    daq.BooleanSwitch(
                        id='state-county',
                        on=False,
                        label='By State/By County',
                        style=LABEL,
                        color=orange
                    )
                ])
            ], width=2),
            dbc.Col([
                html.Div([
                    ALIGN_LABEL,
                    html.Br(),
                    dbc.Button('Edit Graph', id='edit-migration', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            ], width=2)
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='migration-graph',
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
                        html.P(' Units: Dollars in Thousands ($)', style={'color':blue})
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
                        dbc.Button('Download Dataset', id='download-bttn-mig', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-mig')
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
    Output('download-mig','data'),
    Input('download-bttn-mig', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_migration.to_excel, 'Revenues by Workers Remittances Data.xlsx')

@app.callback(
    [Output('sidebar-space-migration','hidden'),
    Output('sidebar-title-migration', 'children')],
    [Input('edit-migration', 'n_clicks'),
    Input('state-county','on'),
    Input('sidebar-space-migration', 'hidden'),
    Input('chart-options-migration', 'value')]
)
def get_sidebar(button, filter, hideSideBar, graphMode):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-migration'):
        if(hideSideBar):
            hideSideBar=False
        else:
            hideSideBar=True
    if(filter):
        title=migrationDatabag.getByName('migrationCounty').title
        migrationDatabag.getByName('migrationCounty').activateDataframe(graphMode)
    else:
        title=migrationDatabag.getByName('migrationState').title
        migrationDatabag.getByName('migrationState').activateDataframe(graphMode)

    
    return hideSideBar, title

@app.callback(
    Output('migration-graph','figure'),
    [Input('select-flow','value'),
    Input('state-county','on'),
    Input('chart-options-migration','value')]
)
def update_data(migrationFlow, view, dummyValue):
    
    if(view):
        dff=migrationDatabag.getByName('migrationCounty').getActive().copy()
        dff=filter_df(dff, 'Migration', migrationFlow)
        fig=px.line(dff, x='Year', y='Value', color='County', color_discrete_sequence=get_colors(dff['County'].unique()))
    else:
        dff=migrationDatabag.getByName('migrationState').getActive().copy()
        dff=filter_df(dff, 'Migration', migrationFlow)
        fig=px.line(sum_df(dff, 'State', 'Year', 'Value'), x='Year', y='Value', color='State', color_discrete_sequence=get_colors(dff['State'].unique()))
    fig.update_xaxes(rangeslider_visible=True)
    if(dummyValue=='Original'):
        fig.update_yaxes(tickprefix='$')
    else:
        fig.update_yaxes(ticksuffix='%', tickformat='000')
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return fig
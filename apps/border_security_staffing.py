
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
DATA_PATH = PATH.joinpath("../datasets/Border Patrol Agent Staffing").resolve()

df_region=pd.read_excel(DATA_PATH.joinpath('Staffing by region.xlsx'))
df_sector=pd.read_excel(DATA_PATH.joinpath('Staffing by Sector.xlsx'))
regionDataset=dataset('Border Patrol Agent Staffing by Region', df_region, 'Staffing ', 'region', 'Border Patrol Region', 'Staffing ')
sectorDataset=dataset('Border Patrol Agent Staffing by Sector', df_sector, 'Staff', 'sector', 'Sector', 'Staff')
staffDatabag=dataBag([regionDataset, sectorDataset])



layout=html.Div([
    html.Div(id='sidebar-space-staff',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-staff',children='Border Patrol Agent Staffing'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-staff',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        dcc.Input(id='max_input_staff', type='number', min=10, max=1000, value=150),
        html.Label('Min Y Value:', style=LABEL),
        dcc.Input(id='min_input_staff', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-staff', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)


        
    ],
    style=SIDEBAR_STYLE,
    )
    ], hidden=True),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2(id='staff-title',children=['Border Patrol Agent Staffing'], style=TITLE),
                html.Hr(style=HR)
            ]),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-staff', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            ], width=2)
        ])
    ]),
    dbc.Container([
        dbc.Col([
            dcc.Tabs(id='select-indicator', value='region', children=[
                dcc.Tab(label='By Region', value='region', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='By Sector', value='sector', style=tab_style, selected_style=tab_selected_style)
            ])
        ])
        
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='staffing-graph',
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
                        dbc.Button('Download Dataset', id='download-bttn-staff', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-staff')
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
    Output('download-staff','data'),
    [Input('download-bttn-staff', 'n_clicks'),
    Input('select-indicator', 'value')],
    prevent_initial_call=True
)
def download_median(downloadB, tab): 
    trigger_id=ctx.triggered_id 
    if(trigger_id=='select-indicator'):
        raise PreventUpdate
    else:
        if(tab=='region'):
            return dcc.send_data_frame(df_region.to_excel, 'Border Patrol Agent Staffing by Region.xlsx')
        else:
            return dcc.send_data_frame(df_sector.to_excel, 'Border Patrol Agent Staffing by Sector.xlsx')

@app.callback(
    [Output('sidebar-space-staff','hidden'),
    Output('sidebar-title-staff', 'children'),
    Output('max_input_staff', 'max'),
    Output('max_input_staff', 'min'),
    Output('min_input_staff', 'max'),
    Output('min_input_staff','min'),
    Output('max_input_staff','value'),
    Output('min_input_staff','value')],
    [Input('edit-staff', 'n_clicks'),
    Input('select-indicator','value'),
    Input('sidebar-space-staff', 'hidden'),
    Input('reset-staff','n_clicks'),
    Input('chart-options-staff','value')]
)
def get_sidebar(button, graphName, hideSideBar, reset, dummyChartOptions):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-staff'):
        if(hideSideBar):
            hideSideBar=False
        else:
            hideSideBar=True
    staffDatabag.getByName(graphName).activateDataframe(dummyChartOptions)
    currentDataset=staffDatabag.getByName(graphName)
    title=currentDataset.title
    
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
    if(trigger_id=='reset-staff'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        hideSideBar=False
    if(trigger_id=='max_input_staff' or trigger_id=='min_input_staff'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        hideSideBar=False
    
    return hideSideBar, title, currMax, maxMin, minMax, currMin, currentValueMax, currentValueMin
@app.callback(
    Output('staff-title','children'),
    [Input('staff-title','children'),
    Input('chart-options-staff','value'),
    Input('sidebar-title-staff','children'),
    Input('reset-staff','n_clicks'),
    Input('max_input_staff','value'),
    Input('min_input_staff','value')]
)
def change_chart(title, chartMode, sideBarTitle, reset, max, min):
    trigger_id=ctx.triggered_id
    #staffDatabag.getDataframe(sideBarTitle).activateDataframe(chartMode)
    if(trigger_id=='max_input_staff' or trigger_id=='min_input_staff'):
        staffDatabag.getDataframe(sideBarTitle).trim(max, min)
    if(trigger_id=='reset-staff'):
        staffDatabag.getDataframe(sideBarTitle).reset()
    return title

@app.callback(
    Output('staffing-graph', 'figure'),
    [Input('select-indicator','value'),
    Input('chart-options-staff', 'value'),
    Input('max_input_staff','value'),
    Input('min_input_staff','value'),
    Input('reset-staff','n_clicks')]
)
def update_data(indicator, dummyValue, dummyMax, dummyMin, dummyReset):
    dff=staffDatabag.getByName(indicator).getActive().copy()
    if(indicator=='region'):
        fig=px.line(dff, x='Fiscal Year', y='Staffing ', color='Border Patrol Region', color_discrete_sequence=get_colors(dff['Border Patrol Region'].unique()))
    if(indicator=='sector'):
        fig=px.line(dff, x='Year', y='Staff', color='Sector', color_discrete_sequence=get_colors(dff['Sector'].unique()))
    fig.update_xaxes(rangeslider_visible=True)
    if(dummyValue=='PercentChange'):
        fig.update_yaxes(ticksuffix='%')
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return fig
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
df_ep=pd.read_excel(DATA_PATH.joinpath("Total Flows to El Paso.xlsx"))
epDataset=dataset('Total Flows to El Paso Chart', df_ep, 'Total', 'totalFlows', 'Commodity', 'Total')
epDataset.modify_percent_change('Mode', 'Commodity', 'Total')

layout=html.Div(children=[
    html.Div(id='sidebar-space-trade-epFlows',children=[
        html.Div([
        html.H6(id='sidebar-title-trade-epFlows',children='Total Flows to El Paso by Year'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-trade-epFlows',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='max_input-trade-epFlows', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Label('Min Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='min_input-trade-epFlows', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-trade-epFlows', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)

        ], style=SIDEBAR_STYLE)
        
    
    ], hidden=True),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(id='dummy-trade-epFlows',children=['Total Flows to El Paso'], style=TITLE)
                ])
            ]),
            html.Hr(style=HR)
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='ep-graph',
                        figure={},
                        config={'editable':False}
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Label(['Mode'], style=LABEL),
                            dcc.Dropdown(
                                id='select-mode-int',
                                options=[{'label':x, 'value':x}for x in df_ep['Mode'].unique()],
                                value=df_ep['Mode'].unique()[0],
                                style=DROPDOWN,
                                optionHeight=90,
                                
                            ),
                        ]),
                        dbc.Col([
                            html.Div([
                                html.Label(['Edit'], style={'color':'#ffffff'}),
                                html.Br(),
                                dbc.Button('Edit Graph', id='edit-trade-flows', outline=True, color="primary", className="me-1", value='edit')
                            ])
                        ])
                        ]),
                    html.Br(),
                    daq.LEDDisplay(
                        id='led-ep',
                        value=5,
                        label='Total Flows',
                        color=orange,
                        size=35,
                        style=LABEL
                    )
                
            
                ]),
                html.Br(),
                html.Br(),
                html.Br()
            ], width=4)
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
                        html.P('Last Update: 2020', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Source: USA Gov', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-trade2', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-trade2')
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
    Output('download-trade2','data'),
    Input('download-bttn-trade2', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB):

    return dcc.send_data_frame(df_ep.to_excel, 'Total Flows to El Paso.xlsx')

@app.callback(
    [Output('sidebar-space-trade-epFlows', 'hidden'),
    Output('max_input-trade-epFlows', 'max'),
    Output('max_input-trade-epFlows', 'min'),
    Output('min_input-trade-epFlows', 'max'),
    Output('min_input-trade-epFlows','min'),
    Output('max_input-trade-epFlows','value'),
    Output('min_input-trade-epFlows','value')],
    [Input('edit-trade-flows', 'n_clicks'),
    Input('sidebar-space-trade-epFlows', 'hidden'),
    Input('select-mode-int','value'),
    Input('reset-trade-epFlows', 'n_clicks')]
)
def get_sidebar(editButton,showSideBar, mode, reset):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-trade-flows'):
        name='totalFlows'
        if(showSideBar):
            showSideBar=False
        else:
            showSideBar=True
    epDataset.adjustMinMax('Mode',mode)
    if(trigger_id=='select-mode-int'):
        epDataset.reset()
    currentDataset=epDataset
    currMin=currentDataset.min
    currMax=currentDataset.max
    if(currentDataset.isTrimmed()):
        currentValueMax=currentDataset.trimMax
        currentValueMin=currentDataset.trimMin
        minMax=currentDataset.trimMax-1
        maxMin=currentDataset.trimMin-1
    else:
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        minMax=currentDataset.max-1
        maxMin=currentDataset.min+1
    if(trigger_id=='reset-trade-epFlows'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        showSideBar=False
    if(trigger_id=='max_input-trade-epFlows' or trigger_id=='min_input-trade-epFlows'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        showSideBar=False
    return showSideBar, currMax, maxMin, minMax, currMin, currentValueMax, currentValueMin


@app.callback(
    Output('sidebar-title-trade-epFlows','children'),
    [Input('chart-options-trade-epFlows','value'),
    Input('max_input-trade-epFlows','value'),
    Input('min_input-trade-epFlows','value'),
    Input('reset-trade-epFlows','n_clicks'),
    Input('dummy-trade-epFlows','children')]
)
def update_dataset(chartMode, max, min, reset, mainTitle):
    trigger_id=ctx.triggered_id
    epDataset.activateDataframe(chartMode)
    
    if(trigger_id=='max_input-trade-epFlows' or trigger_id=='min_input-trade-epFlows'):
        epDataset.trim(max, min)
    if(trigger_id=='reset-trade-flows'):
        epDataset.reset()
    return mainTitle

@app.callback(
    [Output('ep-graph','figure'),
    Output('led-ep','value')],
    [Input('select-mode-int','value'),
    Input('chart-options-trade-epFlows', 'value'),
    Input('max_input-trade-epFlows','value'),
    Input('min_input-trade-epFlows','value'),
    Input('reset-trade-epFlows','n_clicks')]
)
def generate_chart(mode, dummyValue, dummyMax, dummyMin, dummyReset):
    dff_ep=epDataset.getActive().copy()
    fig2=epDataset.get_line_chart('Mode', mode, colors='Commodity',tick=1,dt=1)
    total_f=round(sum(dff_ep[dff_ep['Mode']==mode]['Total']),1)
    fig2.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig2.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return fig2, total_f
    
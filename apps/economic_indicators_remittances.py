
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
DATA_PATH = PATH.joinpath("../datasets/Remittances").resolve() #Once we're on that path, we go into datasets. 
df_rem=pd.read_excel(DATA_PATH.joinpath('Worker Remittances Juarez.xlsx'))
remDataset=dataset('Revenues by Workers Remittances Chart', df_rem, 'Value', name='remit', group='City', By='Value')
remDatabag=dataBag([remDataset])

layout=html.Div(children=[
    html.Div(id='sidebar-space-rem',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-rem',children='Revenues by Workers Remittances Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-rem',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        dcc.Input(id='max_input_rem', type='number', min=10, max=1000, value=150),
        html.Label('Min Y Value:', style=LABEL),
        dcc.Input(id='min_input_rem', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-rem', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)
        


        
    ],
    style=SIDEBAR_STYLE,
    )
    ], hidden=True),
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(id='rem-title',children=['Revenues by Workers Remittances. Juarez Unit.'], style={'color':'#041E42'})
                ])
            ),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-rem', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            
            ], width=2)
        ]),
        html.Hr(style=HR),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='rem-graph', figure={})
            )
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
                        html.P('Last Update: Jan 2021', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Source: USA Gov', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-rem', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-rem')
            ],  style={'margin-left': '0px', 'margin-right':'1px'}, width=2)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ]),
    ])
])
@app.callback(
    Output('download-rem','data'),
    Input('download-bttn-rem', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_rem.to_excel, 'Revenues by Workers Remittances Data.xlsx')

@app.callback(
    Output('rem-title','children'),
    [Input('chart-options-rem','value'),
    Input('max_input_rem','value'),
    Input('min_input_rem','value'),
    Input('reset-rem','n_clicks'),
    Input('rem-title','children')
    ]
)
def change_chart(chartMode, max, min, reset, mainTitle):
    trigger_id=ctx.triggered_id
    if(trigger_id=='chart-options-rem'):
        remDatabag.getDataframe().activateDataframe(chartMode)
        remDatabag.getDataframe().reset()
    if(trigger_id=='max_input_rem' or trigger_id=='min_input_rem'):
        remDatabag.getDataframe().trim(max, min)
    if(trigger_id=='reset-rem'):
        remDatabag.getDataframe().reset()
    return mainTitle

@app.callback(
    [Output('sidebar-space-rem','hidden'),
    Output('max_input_rem', 'max'),
    Output('max_input_rem', 'min'),
    Output('min_input_rem', 'max'),
    Output('min_input_rem','min'),
    Output('max_input_rem','value'),
    Output('min_input_rem','value')],
    [Input('edit-rem', 'n_clicks'),
    Input('sidebar-space-rem', 'hidden'),
    Input('max_input_rem','value'),
    Input('min_input_rem','value'),
    Input('reset-rem','n_clicks'),
    Input('rem-title','children')]
)
def get_sidebar(button, hideSideBar, max, min, reset, dummyTitle):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-rem'):
        if(hideSideBar):
            hideSideBar=False
        else:
            hideSideBar=True
    currentDataset=remDatabag.getDataframe()
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
    if(trigger_id=='reset-rem'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        hideSideBar=False
    if(trigger_id=='max_input_rem' or trigger_id=='min_input_rem'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        hideSideBar=False

    
    return hideSideBar, currMax, maxMin, minMax, currMin, currentValueMax, currentValueMin



@app.callback(
    Output('rem-graph', 'figure'),
    [Input('rem-title', 'children'),
    Input('chart-options-rem', 'value'),
    Input('reset-rem','n_clicks')]
    
)
def update_data(title, dummyValue, reset):
    currentDataset=remDatabag.getDataframe()
    dff=currentDataset.getActive().copy()
    if(currentDataset.isTrimmed()):
        max=currentDataset.trimMax
        min=currentDataset.trimMin
        dff=dff[(dff['Value']>=min)&(dff['Value']<=max)]
    fig=px.line(dff, x='Year', y='Value')
    fig.update_xaxes(nticks=len(pd.unique(dff['Year'])), rangeslider_visible=True)
    if(dummyValue=='Original'):
        fig.update_yaxes(tickprefix='$')
    else:
        fig.update_yaxes(ticksuffix='%')
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return fig
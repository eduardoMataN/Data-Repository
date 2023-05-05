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
df_gdp=pd.read_excel(DATA_PATH.joinpath('GDP by Industry for Border Counties.xlsx'))
gdpDatasetCounty=dataset('GDP by Industry for Border Counties Chart', df_gdp, 'GDP', 'gdpCounty', 'County', 'GDP')
gdpDatasetCounty.modify_percent_change('County','Description', 'GDP')
gdpDatasetIndustry=dataset('GDP by County for Industries Chart', df_gdp, 'GDP', 'gdpDesc', 'County', 'GDP')
gdpDatasetIndustry.modify_percent_change('Description','County', 'GDP')
gdpDataBag=dataBag([gdpDatasetCounty, gdpDatasetIndustry])

layout=dbc.Container([
    html.Div(id='sidebar-space-ind-gdp',children=[
        html.Div([
        html.H6(id='sidebar-title-ind-gdp',children='Number of Business Stablishments by Year Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-ind-gdp',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='max_input-ind-gdp', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Label('Min Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='min_input-ind-gdp', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-ind-gdp', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)

        ], style=SIDEBAR_STYLE)
        
    
    ], hidden=True),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1(id='title-gdp',children=['GDP by Industry for Border Counties'], style=TITLE)
                ])
            ]),
            html.Hr(style=HR)
        ])
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    daq.PowerButton(
                        id='county-button',
                        on=True,
                        color=orange
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    html.Label(['County'], style=LABEL),
                    dcc.Dropdown(
                        id='select-county-gdp',
                        options=get_options(df_gdp, 'County'),
                        value=df_gdp['County'].unique()[0],
                        multi=False,
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=False
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    daq.PowerButton(
                        id='industry-button',
                        on=False,
                        color=orange
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    html.Label(['Industry'], style=LABEL),
                    dcc.Dropdown(
                        id='select-industry-gdp',
                        options=get_options(df_gdp, 'Description'),
                        value=df_gdp['Description'].unique()[0],
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
                    dbc.Button('Edit Graph', id='edit-gdp', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            ], width=2),
            
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='gdp-graph',
                        figure={}
                    )
                ])
            ])
        ]),
    ]),
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
                        html.P('Last Update: June 2022',style=INFO_BOX_STYLE)
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Source: USA Gov', style=INFO_BOX_STYLE)
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        ALIGN_LABEL,
                        html.Br(),
                        dbc.Button('Download Dataset', id='download-bttn-ind-2', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-ind-2')
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
    Output('download-ind-2','data'),
    Input('download-bttn-ind-2', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_gdp.to_excel, 'GDP By Industry for Border Counties Data.xlsx')

@app.callback(
        Output('sidebar-space-ind-gdp','hidden'),
        [Input('edit-gdp', 'n_clicks'),
        Input('sidebar-space-ind-gdp','hidden')],
         prevent_initial_call=True
)
def display_sidebar(editButton, hideBar):
    if(hideBar):
        return False
    return True
@app.callback(
        [Output('max_input-ind-gdp', 'max'),
        Output('max_input-ind-gdp', 'min'),
        Output('min_input-ind-gdp', 'max'),
        Output('min_input-ind-gdp','min'),
        Output('max_input-ind-gdp','value'),
        Output('min_input-ind-gdp','value')],
        [Input('industry-button','on'),
        Input('county-button','on'),
        Input('reset-ind-gdp','n_clicks'),
        Input('max_input-ind-gdp','value'),
        Input('min_input-ind-gdp','value'),
        Input('select-county-gdp','value'),
        Input('select-industry-gdp','value')]
)
def adjust_sidebar(industryButton, countyButton, resetButton,max, min, countyValue, industryValue):
    trigger_id=ctx.triggered_id
    print(trigger_id)
    if(industryButton):
        currentDataset=gdpDataBag.getDataframe('GDP by Industry for Border Counties Chart')
        currentDataset.adjustMinMax('Description', industryValue)
    if(countyButton):
        currentDataset=gdpDataBag.getDataframe('GDP by County for Industries Chart')
        currentDataset.adjustMinMax('County', countyValue)
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
    if(trigger_id=='reset-ind-gdp'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
    if(trigger_id=='max_input-ind-gdp' or trigger_id=='min_input-ind-gdp'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        
    
    return currMax, maxMin, minMax, currMin, currentValueMax, currentValueMin

@app.callback(
        Output('title-gdp','children'),
        [Input('chart-options-ind-gdp','value'),
        Input('max_input-ind-gdp','value'),
        Input('min_input-ind-gdp','value'),
        Input('reset-ind-gdp','n_clicks'),
        Input('industry-button','on'),
        Input('county-button','on')]
)
def update_dataset(chartMode, max, min, reset, industryButton, countyButton):
    trigger_id=ctx.triggered_id
    if(industryButton):
        gdpDataBag.set_current('GDP by Industry for Border Counties Chart')
    else:
        gdpDataBag.set_current('GDP by County for Industries Chart')
    currentDataset=gdpDataBag.get_current()
    currentDataset.activateDataframe(chartMode)
    if(trigger_id=='max_input-ind-gdp' or trigger_id=='min_input-ind-gdp'):
        currentDataset.trim(max, min)
    if(trigger_id=='reset-ind-gdp'):
        currentDataset.reset()
    gdpDataBag.replace_current(currentDataset)
    return currentDataset.title
@app.callback(
    [Output('gdp-graph','figure'),
    Output('county-button','on'),
    Output('select-county-gdp','disabled'),
    Output('industry-button','on'),
    Output('select-industry-gdp','disabled')],
    [Input('county-button','on'),
    Input('select-county-gdp','value'),
    Input('industry-button', 'on'),
    Input('select-industry-gdp','value'),
    Input('chart-options-ind-gdp', 'value'),
    Input('max_input-ind-gdp','value'),
    Input('min_input-ind-gdp','value'),
    Input('reset-ind-gdp','n_clicks')]

)
def create_chart(countyOn, countyValue, industryOn, industryValue, chartOptions, max, min, reset):
    trigger_id=ctx.triggered_id
    disableCounty=False
    disableIndustry=True
    dff2=gdpDataBag.get_current()
    if(trigger_id=='industry-button'):
        disableCounty=True
        disableIndustry=False
        countyOn=False
        industryOn=True
        
    if(trigger_id=='county-button'):
        disableCounty=False
        disableIndustry=True
        countyOn=True
        industryOn=False
        
    if(countyOn):
        dff2=gdpDataBag.getByName('gdpCounty').getActive().copy()
        fig=px.line(filter_df(dff2, 'County', countyValue), x='Year', y='GDP', color='Description', color_discrete_sequence=get_colors(dff2['Description'].unique()))
        disableCounty=False
        disableIndustry=True
        countyOn=True
        industryOn=False
    if(industryOn):
        dff2=gdpDataBag.getByName('gdpDesc').getActive().copy()
        fig=px.line(filter_df(dff2, 'Description', industryValue), x='Year', y='GDP', color='County', color_discrete_sequence=get_colors(dff2['County'].unique()))
        disableCounty=True
        disableIndustry=False
        countyOn=False
        industryOn=True
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return fig, countyOn, disableCounty, industryOn, disableIndustry

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

incomeDatabag=dataBag([personalDataset, medianDataset, industryDataset])

layout=html.Div([
    html.Div(id='sidebar-space-income-median',children=[
        html.Div([
        html.H6(id='sidebar-title-income-median',children='Imports by HS Commodities Imports Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-income-median',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='max_input-income-median', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Label('Min Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='min_input-income-median', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-income-median', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)

        ], style=SIDEBAR_STYLE)
        
    
    ], hidden=True),
    dbc.Container(children=[
    html.Br(),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(id='median-income-title', children=['Median Household & Personal Income'], style={'color':'#041E42'})
                ]),
                
            ),
            html.Hr(style=HR)
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label('Indicator', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-indicator',
                    options=[{'label':x, 'value':x} for x in df_median['Indicator'].unique()],
                    multi=False,
                    value=df_median['Indicator'].tolist()[0],
                    style={'width':'100%'},
                    optionHeight=90)
                ])
            ),
            dbc.Col(
                html.Div([
                    html.Label('Household Type', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-household',
                    options=[{'label':x, 'value':x} for x in df_median['Household Type'].dropna().unique()],
                    multi=False,
                    value=df_median['Household Type'].dropna().unique()[0],
                    style={'width':'100%'},
                    optionHeight=90,
                    disabled=True)
                ])
            ),
            dbc.Col(
                html.Div([
                    html.Label('Industry', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-industry',
                    options=[{'label':x, 'value':x} for x in df_median['Industry'].dropna().unique()],
                    multi=False,
                    value=df_median['Industry'].dropna().unique()[4],
                    style={'width':'100%'},
                    optionHeight=90,
                    disabled=True)
                ])
            , width=3),
            dbc.Col([
                html.Div([
                    ALIGN_LABEL,
                    html.Br(),
                    dbc.Button('Edit Graph', id='edit-income-median', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ], style={"padding": "0rem 0rem"})
            ], style={'margin-left': '0px', "padding": "0px 0px"}, width=2)
            
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='median-graph', figure={})
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
                        html.P(' Units: Dollars ($)', style={'color':blue})
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
                    dbc.Button('Download Dataset', id='download-bttn-income', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ]),
                dcc.Download(id='download-income')
            ],  style={'margin-left': '0px', 'margin-right':'0px'}, width=2)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ])
])

@app.callback(
    Output('download-income','data'),
    Input('download-bttn-income', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB):
    

    return dcc.send_data_frame(df_median.to_excel, 'Median Household & Personal Income.xlsx')

@app.callback(
    [Output('sidebar-space-income-median','hidden'),
    Output('sidebar-title-income-median', 'children'),
    Output('max_input-income-median', 'max'),
    Output('max_input-income-median', 'min'),
    Output('min_input-income-median', 'max'),
    Output('min_input-income-median','min'),
    Output('max_input-income-median','value'),
    Output('min_input-income-median','value')],
    [Input('edit-income-median', 'n_clicks'),
    Input('select-indicator','value'),
    Input('sidebar-space-income-median', 'hidden'),
    Input('sidebar-title-income-median', 'children'),
    Input('select-household','value'),
    Input('select-industry','value'),
    Input('max_input-income-median','value'),
    Input('min_input-income-median', 'value'),
    Input('reset-income-median', 'n_clicks')]
)
def get_sidebar(button, indicatorValue, hideSideBar, title, householdValue, industryValue, max, min, reset):
    trigger_id=ctx.triggered_id
    
    if(trigger_id=='edit-income-median'):
        if(hideSideBar):
            hideSideBar=False
        else:
            hideSideBar=True
        title=incomeDatabag.getByName(indicatorValue).title
    
    currentDataset=incomeDatabag.getByName(indicatorValue)
    if(indicatorValue=='Earnings by Industry'):
        currentDataset.adjustMinMax('Industry', industryValue)
    if(indicatorValue=='Median Household Income'):
        currentDataset.adjustMinMax('Household Type', householdValue)
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
    if(trigger_id=='reset-income-median'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        hideSideBar=False
    if(trigger_id=='max_input-income-median' or trigger_id=='min_input-income-median'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        hideSideBar=False


    
    return hideSideBar, title, currMax, maxMin, minMax, currMin, currentValueMax, currentValueMin
@app.callback(
    Output('median-income-title','children'),
    [Input('chart-options-income-median','value'),
    Input('max_input-income-median','value'),
    Input('min_input-income-median','value'),
    Input('reset-income-median','n_clicks'),
    Input('median-income-title','children'),
    Input('select-indicator','value')
    ]
)
def change_chart(chartMode, max, min, reset, mainTitle, indicatorValue):
    trigger_id=ctx.triggered_id
    if(trigger_id=='chart-options-income-median'):
        incomeDatabag.getByName(indicatorValue).activateDataframe(chartMode)
        #incomeDatabag.getDataframe('Employment by Industry Chart').reset()
    if(trigger_id=='max_input-income-median' or trigger_id=='min_input-income-median'):
        incomeDatabag.getByName(indicatorValue).trim(max, min)
    if(trigger_id=='reset-income-median'):
        incomeDatabag.getByName(indicatorValue).reset()
    return mainTitle

@app.callback(
    [Output(component_id='median-graph', component_property='figure'), Output(component_id='select-household', component_property='disabled'),
    Output(component_id='select-industry', component_property='disabled')],
    [Input(component_id='select-indicator', component_property='value'), Input(component_id='select-household', component_property='value'),
    Input(component_id='select-industry', component_property='value'), Input('chart-options-income-median', 'value'),
    Input('max_input-income-median','value'),
    Input('min_input-income-median','value'),
    Input('reset-income-median','n_clicks')]
)
def update_median(ind, household, industry, chartType, dummyMax, dummyMin, dummyReset):
    drop1=True
    
    drop3=True
    
    dff=incomeDatabag.getByName(ind).getActive().copy()
    
    fig=make_subplots(rows=1, cols=1)
    if(ind=='Personal Per Capita Income'):
        drop1=True
        df_temp=dff[dff['Indicator']==ind]
        counties=df_temp['County'].unique()
        fig=create_subplot(fig, 1, 1, df_temp, 'Year', 'Income', 'County')
        fig.update_xaxes(rangeslider_visible=True)
        if(chartType=='PercentChange'):
            fig.update_yaxes(ticksuffix='%')
    
    if (ind=='Median Household Income'):
        drop1=False
        df_temp=dff[dff['Indicator']==ind]
        counties=df_temp['County'].unique()
        fig=create_subplot(fig, 1, 1, df_temp[df_temp['Household Type']==household], 'Year', 'Income', 'County')
        fig.update_xaxes(rangeslider_visible=True)
        if(chartType=='PercentChange'):
            fig.update_yaxes(ticksuffix='%')
    
    if (ind=='Earnings by Industry'):
        drop3=False
        df_temp=dff[dff['Indicator']==ind]
        df_temp=dff[dff['Industry']==industry]
        counties=df_temp['County'].unique()
        fig=create_subplot(fig, 1, 1, df_temp[df_temp['Industry']==industry], 'Year', 'Income', 'County')
        fig.update_xaxes(rangeslider_visible=True)
        if(chartType=='PercentChange'):
            fig.update_yaxes(ticksuffix='%')
        else:
            fig.update_yaxes(ticksuffix='M')
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.', xaxis_title='Year')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return fig, drop1, drop3
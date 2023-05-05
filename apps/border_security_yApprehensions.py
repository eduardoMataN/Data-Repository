
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

df_cit=pd.read_excel(DATA_PATH.joinpath('Apprehensions by Citizenship.xlsx'))
df_cit_per=df_cit.copy()
df_cit_per['Apprehensions']=df_cit_per['Apprehensions'].pct_change()
citDataset=dataset('Yearly Apprehensions by Citizenship Chart', df_cit, 'Apprehensions','tab-cit', 'Citizenship', 'Apprehensions', 'Citizenship')
citDataset.modify_percent_change('Sector', 'Citizenship', 'Apprehensions')

df_country=pd.read_excel(DATA_PATH.joinpath('Apprehensions by Country.xlsx'))
df_country_per=df_country.copy()
df_country_per['Illegal Alien Apprehensions']=df_country_per['Illegal Alien Apprehensions'].pct_change()
countryDataset=dataset('Yearly Apprehensions by Country Chart', df_country, 'Illegal Alien Apprehensions', 'tab-country', 'Country', 'Illegal Alien Apprehensions')
countryDataset.modify_percent_change('Sector', 'Country', 'Illegal Alien Apprehensions')
borderSecurityBag=dataBag([citDataset, countryDataset])

layout=html.Div([
     html.H6(id='dummy1', children='', hidden=True),
    html.Div(id='dummy',children=[], hidden=True),
    html.Div(dcc.Location(id='sidebar-location',refresh=False)),
    html.Div(id='sidebar-space-yApp',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-yApp',children='Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-yApp',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        dcc.Input(id='max_input_yApp', type='number', min=10, max=1000, value=150),
        html.Label('Min Y Value:', style=LABEL),
        dcc.Input(id='min_input_yApp', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-yApp', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)
    ],
    style=SIDEBAR_STYLE,
    )
    ], hidden=True),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(id='app-title',children=['Yearly Apprehensions by Sector'], style=TITLE)
                ])
            ]),
            html.Hr(style={'color':blue, 'borderWidth': "0.3vh", 'borderColor':blue, 'opacity':'unset', 'width':'100%'})
        ])
    ]),
    dbc.Container([
        dcc.Tabs(id='app-tabs', value='tab-cit', children=[
            dcc.Tab(label='By Citizenship', value='tab-cit', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='By Country',value='tab-country', style=tab_style, selected_style=tab_selected_style)
        ]),
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(id='sector-label', children=['Sector'], style=LABEL),
                    dcc.Dropdown(
                        id='select-sector',
                        options=[{'label':x, 'value':x}for x in df_cit['Sector'].unique()],
                        value=df_cit['Sector'].unique()[0],
                        multi=False,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label(['Edit'], style={'color':'#ffffff'}),
                    html.Br(),
                    dbc.Button('Edit Graph', id='edit-yearly', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            ], width=2),
        ]),
       
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='apprehensions-graph',
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
                        dbc.Button('Download Dataset', id='download-bttn-app', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-app')
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
    Output('download-app','data'),
    [Input('download-bttn-app', 'n_clicks'),
    Input('app-tabs', 'value')],
    prevent_initial_call=True
)
def download_median(downloadB, tab): 
    trigger_id=ctx.triggered_id 
    if(trigger_id=='app-tabs'):
        raise PreventUpdate
    else:
        if(tab=='tab-cit'):
            return dcc.send_data_frame(df_cit.to_excel, 'Yearly Apprehensions by Sector and Citizenship.xlsx')
        else:
            return dcc.send_data_frame(df_country.to_excel, 'Yearly Apprehensions by Sector and Country.xlsx')
@app.callback(
    [Output('sidebar-space-yApp','hidden'),
    Output('sidebar-title-yApp','children'),
    Output('max_input_yApp', 'max'),
    Output('max_input_yApp', 'min'),
    Output('min_input_yApp', 'max'),
    Output('min_input_yApp','min'),
    Output('max_input_yApp','value'),
    Output('min_input_yApp','value')],
    [Input('edit-yearly','n_clicks'),
    Input('sidebar-space-yApp','children'),
    Input('app-tabs','value'),
    Input('sidebar-space-yApp','hidden'),
    Input('sidebar-title-yApp', 'children'),
    Input('reset-yApp','n_clicks'),
    Input('app-title','children'),
    Input('select-sector','value'),
    Input('max_input_yApp','value'),
    Input('min_input_yApp','value')]
)
def get_sidebar(button, sidebarSpace, currentTabApp, sideBarShow, title, reset, dummyTitle, filterValue, max, min):
    trigger_id=ctx.triggered_id    
    if(trigger_id=='select-sector'):
        borderSecurityBag.getByName(currentTabApp).adjustMinMax('Sector', filterValue)
    if(trigger_id=='edit-yearly'):
        borderSecurityBag.getByName(currentTabApp).adjustMinMax('Sector', filterValue)
        currentDataset=borderSecurityBag.getByName(currentTabApp)
        newTitle=currentDataset.title
        if(sideBarShow):
            sideBarShow=False
        else:
            sideBarShow=True
        if(title!=newTitle):
            sideBarShow=False
        title=newTitle
        
            
    
        
    if(trigger_id=='app-tabs'):
        currentDataset=borderSecurityBag.getByName(currentTabApp)
        title=currentDataset.title
    currentDataset=borderSecurityBag.getDataframe(title)
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
    if(trigger_id=='reset-yApp'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        sideBarShow=False
    if(trigger_id=='max_input_yApp' or trigger_id=='min_input_yApp'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        sideBarShow=False
    return sideBarShow, title, currMax, maxMin, minMax, currMin, currentValueMax, currentValueMin
@app.callback(
    Output('app-title','children'),
    [Input('app-title','children'),
    Input('chart-options-yApp','value'),
    Input('sidebar-title-yApp','children'),
    Input('reset-yApp','n_clicks'),
    Input('max_input_yApp','value'),
    Input('min_input_yApp','value')]
)
def change_chart(title, chartMode, sideBarTitle, reset, max, min):
    trigger_id=ctx.triggered_id
    borderSecurityBag.getDataframe(sideBarTitle).activateDataframe(chartMode)
    if(trigger_id=='max_input_yApp' or trigger_id=='min_input_app'):
        borderSecurityBag.getDataframe(sideBarTitle).trim(max, min)
    if(trigger_id=='reset-yApp'):
        borderSecurityBag.getDataframe(sideBarTitle).reset()
    return title
@app.callback(
    [Output('apprehensions-graph', 'figure'),
    Output('select-sector','options'),
    Output('select-sector','value'),
    ],
    [Input('select-sector','value'),
    Input('select-sector','options'),
    Input('app-tabs','value'),
    Input('chart-options-yApp','value'),
    Input('max_input_yApp','value'),
    Input('min_input_yApp','value'),
    Input('reset-yApp','n_clicks')]
)
def update_data(sectorValue, sectorOptions, currentTab,  chartType, dummyMax, dummyMin, dummyReset):
    #Chunk for section 1:
    trigger_id=ctx.triggered_id
    if(currentTab=='tab-cit'):
        dff=borderSecurityBag.getByName(currentTab).getActive().copy()
        if(trigger_id=='app-tabs'):
            sectorOptions=get_options(dff, 'Sector')
            sectorValue=dff['Sector'].unique()[0]
        fig=px.line(dff[dff['Sector']==sectorValue], x='Year', y='Apprehensions', color='Citizenship', color_discrete_sequence=borderSecurityBag.getByName(currentTab).colors)
        fig.update_xaxes(rangeslider_visible=True)
    if(currentTab=='tab-country'):
        dff=borderSecurityBag.getByName(currentTab).getActive().copy()
        if(trigger_id=='app-tabs'):
            sectorOptions=get_options(dff, 'Sector')
            sectorValue=dff['Sector'].unique()[0]
        fig=px.line(dff[dff['Sector']==sectorValue], x='Year', y='Illegal Alien Apprehensions', color='Country', color_discrete_sequence=borderSecurityBag.getByName(currentTab).colors)
        fig.update_xaxes(rangeslider_visible=True)   
    if(borderSecurityBag.getByName(currentTab).get_active_mode()=='Original'):
        nothing='nothing'
    else:
        fig.update_yaxes(ticksuffix='%')
        #fig.update_layout(xaxis=dict(range=[x[0],x[-1]],rangeslider=dict(range=[x[0],x[-1]])))
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return fig, sectorOptions, sectorValue
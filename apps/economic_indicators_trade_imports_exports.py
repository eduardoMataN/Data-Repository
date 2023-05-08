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
df_trade_hs= pd.read_excel(DATA_PATH.joinpath("Imports & Exports by HS Commodities, yearly.xlsx"))
hsImportsDataset=dataset('Imports by HS Commodities Imports Chart', df_trade_hs,'Imports', 'hsImports', 'Port', 'Imports')
hsImportsDataset.modify_percent_change(['Measures', 'Commodity'], 'Port', 'Imports')
hsExportsDataset=dataset('Exports by HS Commodities Imports Chart', df_trade_hs,'Exports', 'hsExports', 'Port', 'Exports')
hsExportsDataset.modify_percent_change(['Measures', 'Commodity'], 'Port', 'Exports')
df_trade_naics=pd.read_excel(DATA_PATH.joinpath("Exports & Imports by NAICS Commodities, yearly.xlsx"))
naicsDataset=dataset('Imports & Exports by NAICS Commodities Chart', df_trade_naics, 'Value', 'naics', 'Commodity', 'Value')
naicsDataset.modify_percent_change(['Commodity', 'Measures'], 'District', 'Value')
tradeDatabag=dataBag([naicsDataset, hsExportsDataset, hsImportsDataset])
layout=html.Div(children=[
    html.Div(id='sidebar-space-trade-impExp',children=[
        html.Div([
        html.H6(id='sidebar-title-trade-impExp',children='Imports by HS Commodities Imports Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-trade-impExp',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='max_input-trade-impExp', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Label('Min Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='min_input-trade-impExp', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-trade-impExp', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)

        ], style=SIDEBAR_STYLE)
        
    
    ], hidden=True),
    dbc.Container(children=[
    html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(id='dummy_trade',children=['Imports & Exports by HS/NAICS Commodities'], style=TITLE)
                ])
            ]),
            html.Hr(style=HR)
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Measures'], style=LABEL),
                    dcc.Dropdown(
                        id='select-measures-int',
                        options=[{'label':x, 'value':x}for x in df_trade_hs['Measures'].unique()],
                        multi=False,
                        value=df_trade_hs['Measures'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=False,
                        searchable=True
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label(['Commodity'], style=LABEL),
                    dcc.Dropdown(
                        id='select-comm-int',
                        options=[{'label':x, 'value':x}for x in df_trade_hs['Commodity'].unique()],
                        value=df_trade_hs['Commodity'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=False,
                        searchable=True
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    daq.ToggleSwitch(
                        id='toggle-int',
                        label='Imports/Exports',
                        labelPosition='top',
                        value=False,
                        style=LABEL,
                        disabled=False
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    daq.ToggleSwitch(
                        id='toggle-int-2',
                        label='HS/NAICS',
                        labelPosition='top',
                        value=False,
                        style=LABEL
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    ALIGN_LABEL,
                    html.Br(),
                    dcc.Dropdown(
                        id='compare-port1',
                        options=[{'label':x, 'value':x}for x in df_trade_hs['Port'].unique()],
                        value=df_trade_hs['Port'].unique()[0],
                        disabled=True,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    COMPARE_LABEL,
                    daq.PowerButton(
                        id='pwr-int',
                        on=False,
                        color='#FF5E5E',
                        style=LABEL,
                        labelPosition='top'
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    ALIGN_LABEL,
                    html.Br(),
                    dcc.Dropdown(
                        id='compare-port2',
                        options=[{'label':x,'value':x}for x in df_trade_hs['Port'].unique()],
                        value=df_trade_hs['Port'].unique()[0],
                        disabled=True,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    ALIGN_LABEL,
                    html.Br(),
                    dbc.Button('Edit Graph', id='edit-trade-impExp', outline=True, color="primary", className="me-1", value='edit')
                ])
            ], width=2)
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id='hs-naics-graph', figure={}, config={'editable':True, 'edits':{'legendPosition':True,'titleText':False, 'axisTitleText':False}, 'showTips':True})
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
                        html.P(' Units: Dollars in Millions ($)', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Last Update: 2022', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Source: USA Gov', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-trade', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-trade')
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
    Output('download-trade','data'),
    Input('download-bttn-trade', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): #THERE ARE TWO DATA FRAMES. SHOULD WE APPEND THEM. 

    return dcc.send_data_frame(pd.concat([df_trade_naics, df_trade_hs]).to_excel, 'Imports & Exports by HS/NAICS Commodities.xlsx')

@app.callback(
    [Output('sidebar-space-trade-impExp', 'hidden'),
    Output('max_input-trade-impExp', 'max'),
    Output('max_input-trade-impExp', 'min'),
    Output('min_input-trade-impExp', 'max'),
    Output('min_input-trade-impExp','min'),
    Output('max_input-trade-impExp','value'),
    Output('min_input-trade-impExp','value'),
    Output('select-measures-int','options'),
    Output('select-measures-int','value'),
    Output('select-comm-int','options'),
    Output('select-comm-int','value'),
    Output('sidebar-title-trade-impExp','children'),
    Output('compare-port1','options'),
    Output('compare-port1','value'),
    Output('compare-port2','options'),
    Output('compare-port2','value')],
    [Input('edit-trade-impExp', 'n_clicks'),
    Input('sidebar-space-trade-impExp', 'hidden'),
    Input('toggle-int-2', 'value'),
    Input('toggle-int','value'),
    Input('reset-trade-impExp','n_clicks'),
    Input('max_input-trade-impExp','value'),
    Input('min_input-trade-impExp','value'),
    Input('select-measures-int','value'),
    Input('select-comm-int','value'),
    Input('select-measures-int','options'),
    Input('select-comm-int','options'),
    Input('sidebar-title-trade-impExp','children'),
    Input('compare-port1','options'),
    Input('compare-port1','value'),
    Input('compare-port2','options'),
    Input('compare-port2','value')]
)
def adjust_elements(buttonimpEx, showSideBar, hsNaics, impExp, reset, max, min, measureValue, commValue, measuresOp, commOp, sidebarTitle, port1Op, port1Value, port2Op, port2Value):
    #This function is merely intended to show or hide the sidebar, and adjust its values. 
    #The first step when we display the sidebar is to adjust our mins and max to the information on the screen. 
    #To do this, we will access the databag that contains the necessary datasets. 
    trigger_id=ctx.triggered_id #This variable will tell us which input triggered our callback. 
    #Let's set a default name for the dataset we need and update it later. 
    name='hsImports'

    #If the user clicked on the Edit Graph button, then they are trying to show or hide the sidebar.
    if(trigger_id=='edit-trade-impExp'):
        if(showSideBar):
            showSideBar=False
        else:
            showSideBar=True
    #Depending on the rest of the controls, we can update the name of the dataset we are looking for. 
    if(hsNaics==True):
        name='naics'
        sidebarTitle=tradeDatabag.getByName(name).get_title()

    else:
        if(impExp==True):
            name='hsExports'
            sidebarTitle=tradeDatabag.getByName(name).get_title()
        else:
            name='hsImports'
            sidebarTitle=tradeDatabag.getByName(name).get_title()
    if(trigger_id=='toggle-int' or trigger_id=='toggle-int-2'):
        if(hsNaics==True):
            name='naics'
            sidebarTitle=tradeDatabag.getByName(name).get_title()
            port1Op, port1Value=tradeDatabag.getDataframe(sidebarTitle).get_options('District')
            port2Op, port2Value=tradeDatabag.getDataframe(sidebarTitle).get_options('District')
        else:
            if(impExp==True):
                name='hsExports'
                sidebarTitle=tradeDatabag.getByName(name).get_title()
                port1Op, port1Value=tradeDatabag.getDataframe(sidebarTitle).get_options('Port')
                port2Op, port2Value=tradeDatabag.getDataframe(sidebarTitle).get_options('Port')
            else:
                name='hsImports'
                sidebarTitle=tradeDatabag.getByName(name).get_title()
                port1Op, port1Value=tradeDatabag.getDataframe(sidebarTitle).get_options('Port')
                port2Op, port2Value=tradeDatabag.getDataframe(sidebarTitle).get_options('Port')
        measuresOp, measureValue=tradeDatabag.getDataframe(sidebarTitle).get_options('Measures')
        commOp, commValue=tradeDatabag.getDataframe(sidebarTitle).get_options('Commodity')
    #Once we have checked the rest of our filters, we can decide which dataset we're currently using. 
    tradeDatabag.getDataframe(sidebarTitle).adjustMinMax(['Measures','Commodity'], [measureValue, commValue])
    #Set current dataset to the one with this title. 
    tradeDatabag.set_current(sidebarTitle)
    currentDataset=tradeDatabag.get_current()
    currMin=currentDataset.min
    currMax=currentDataset.max
    #If the dataset is currently trimmed, then the values of our Max and Min will correspond to these trim values. 
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
    if(trigger_id=='reset-trade-impExp'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        showSideBar=False
    if(trigger_id=='max_input-trade-impExp' or trigger_id=='min_input-trade-impExp'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        showSideBar=False
    return showSideBar, currMax, maxMin, minMax, currMin, currentValueMax, currentValueMin, measuresOp, measureValue, commOp, commValue, sidebarTitle, port1Op, port1Value, port2Op, port2Value

@app.callback(
    Output('dummy_trade','children'),
    [Input('chart-options-trade-impExp','value'),
    Input('max_input-trade-impExp','value'),
    Input('min_input-trade-impExp','value'),
    Input('reset-trade-impExp','n_clicks'),
    Input('dummy_trade','children')
    ]
) 
def update_datasets(chartMode, max, min, reset, mainTitle):
    #This function will update the dataset if needed using the sidebar controls.  
    trigger_id=ctx.triggered_id
    #Activates the current charmode (percent, or original)
    tradeDatabag.get_current().activateDataframe(chartMode)
    #Trims if min or max are updated.
    if(trigger_id=='max_input-trade-impExp' or trigger_id=='min_input'):
        tradeDatabag.get_current().trim(max, min)
    #Resets if reset button is clicked on. 
    if(trigger_id=='reset-trade-impExp'):
        tradeDatabag.get_current().reset()
    return mainTitle

@app.callback(
        [Output('hs-naics-graph','figure'),
        Output('compare-port1','disabled'),
        Output('compare-port2', 'disabled'),
        Output('toggle-int','disabled')],
        [Input('select-measures-int', 'value'),
        Input('select-comm-int','value'),
        Input('select-measures-int','options'),
        Input('pwr-int','on'),
        Input('toggle-int','value'),
        Input('toggle-int-2','value'),
        Input('compare-port1','value'),
        Input('compare-port2','value'),
        Input('select-comm-int', 'options'),
        Input('chart-options-trade-impExp', 'value'),
        Input('max_input-trade-impExp','value'),
        Input('min_input-trade-impExp','value'),
        Input('reset-trade-impExp','n_clicks')]
)
def generate_chart(measureValue, commodityValue, measureOptions, compareOn, toggleImEx,toggleHsNaics, portValue1, portValue2, commodityOptions, dummyValue, dummyMax, dummyMin, dummyReset):
    comparePort1=True
    comparePort2=True
    importsToggle=False
    naicsDropdown=True
    trigger_id=ctx.triggered_id
    #print("Resetting graph "+trigger_id)
    
    if(toggleHsNaics==True):
        currentDataset=tradeDatabag.getByName('naics')
        print(currentDataset.title)
        dff=currentDataset.getActive().copy()
        naicsDropdown=False
        importsToggle=True
        if(trigger_id=='toggle-int-2'):
            measureOptions=[{'label':x,'value':x}for x in dff['Measures'].unique()]
            #measureValue=dff['Measures'].unique()[0]
            commodityOptions=[{'label':x,'value':x}for x in dff['Commodity'].unique()]
            #commodityValue=dff['Commodity'].unique()[0]
        if(compareOn==True):
            comparePort1=False
            comparePort2=False
            dff_compare=dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)&(dff['District']==portValue1)]
            dff_compare2=dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)&(dff['District']==portValue2)]
            fig=make_subplots(1,2)
            fig=create_subplot(fig, 1, 1, dff_compare, 'Year', 'Value', 'District')
            fig=create_subplot(fig, 1, 2, dff_compare2, 'Year', 'Value', 'District')
            fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=1)
            fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=2)
            
        else:
            fig=px.line(dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], x='Year', y='Value', color='District', color_discrete_sequence=get_colors(dff['District'].unique()))
            
    else:
        if(toggleImEx):
            currentDataset=tradeDatabag.getByName('hsExports')
            dff=currentDataset.getActive().copy()
        else:
            currentDataset=tradeDatabag.getByName('hsImports')
            dff=currentDataset.getActive().copy()
        if(trigger_id=='toggle-int-2'):
            
            measureOptions=[{'label':x,'value':x}for x in dff['Measures'].unique()]
            #measureValue=dff['Measures'].unique()[0]
            commodityOptions=[{'label':x,'value':x}for x in dff['Commodity'].unique()]
            #commodityValue=dff['Commodity'].unique()[0]
        if(compareOn):
            comparePort1=False
            comparePort2=False
            fig=make_subplots(1,2)
            if(toggleImEx):
                fig=create_subplot(fig, 1, 1, dff[(dff['Port']==portValue1)&(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], 'Year', 'Exports','Port')
                fig=create_subplot(fig, 1, 2, dff[(dff['Port']==portValue2)&(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], 'Year', 'Exports','Port')
                fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=1)
                fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=2)
            else:
                fig=create_subplot(fig, 1, 1, dff[(dff['Port']==portValue1)&(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], 'Year', 'Imports','Port')
                fig=create_subplot(fig, 1, 2, dff[(dff['Port']==portValue2)&(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], 'Year', 'Imports','Port')
                fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=1)
                fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=2)
        else:
            if(toggleImEx):
                currentDataset=tradeDatabag.getByName('hsExports')
                dff=currentDataset.getActive().copy()
                fig=px.line(dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], x='Year', y='Exports', color='Port', color_discrete_sequence=get_colors(dff['Port'].unique()))
                fig.update_xaxes(rangeslider_visible=True)
            else:
                currentDataset=tradeDatabag.getByName('hsImports')
                dff=currentDataset.getActive().copy()
                fig=px.line(dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], x='Year', y='Imports', color='Port', color_discrete_sequence=get_colors(dff['Port'].unique()))
                fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return fig, comparePort1, comparePort2, importsToggle
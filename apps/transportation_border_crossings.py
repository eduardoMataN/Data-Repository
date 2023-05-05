import pandas as pd
import plotly.express as px
import dash as dash
from dash import dcc, ctx
from dash import html, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pathlib
import plotly.graph_objects as go
from app import app
from apps.common_items import *
from apps.dataset import *
from apps.dataBag import *

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df= pd.read_excel(DATA_PATH.joinpath("Border Crossings.xlsx"))
borderCDataSet=dataset('Border Crossings', df, 'Value', 'graph', 'Port', 'Value')
borderCDataSet.modify_percent_change('Measure', 'Port', 'Value')
boderDataBag=dataBag([borderCDataSet])
df['Value']=pd.to_numeric(df['Value'])
df_copy=df.copy()
maxYear=df['Year'].max()
df_copy=df[df['Measure']=='Truck Containers Empty']
initialValue=sum(df_copy.loc[df_copy.Year==maxYear, 'Value'].tolist())
df_current=df[df['Year']==df['Year'].max()]
df_profiler=df_current[df_current['Port']==sorted(df['Port'].unique())[0]]

toTable=df_profiler[['Measure', 'Month', 'Value']]
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "0rem",
    "margin-right": "0rem",
    "padding": "0rem 0rem",
}

layout=html.Div(children=[
    html.Div(id='sidebar-space-bc',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-bc',children='Border Crossings Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-bc',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        


        
    ],
    style=SIDEBAR_STYLE,
    )
    ], hidden=True),
    dbc.Container([
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.H1(id='section-title', children=['Border Crossings'], style={'color':'#041E42'}),
            ], width=3),
            dbc.Col(
                width=5
            ),
            dbc.Col(),
            
            dbc.Col([
                dbc.Col(
                html.Div([
                    #html.Label(['Current'], style=LABEL),
                    daq.LEDDisplay(id='Number1', value=initialValue, color='#FF8200',labelPosition='bottom',),
                    html.Br(),
                ]),width=5
                
            ),
            ]),
            TILE_HR
        ],className="g-0")
    ]),
    
    
    
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label(['Indicator'], style={'font-weight':'bold', 'color':'#041E42'}),
                    dcc.Dropdown(id='select-indicator',
                                options=[{'label':x, 'value':x} for x in sorted(df.Measure.unique())],
                                multi=False,
                                value=df['Measure'].tolist()[0],
                                style={'width':'100%'},
                                optionHeight=90)
                ])
                
            , style={'margin-right': '3px', 'margin-left': '5px'},),
            dbc.Col([
                html.Div([
                    html.Br(),
                    ALIGN_LABEL,
                    dbc.Button('Edit Graph', id='edit-bc', outline=True, color="primary", className="me-1", value='monthly')
                ], )
            ], style={'margin-right': '1px', 'margin-left': '1px'},width=2)
            
            
        ]),

    ]),
    
    dbc.Container(children=[
        dbc.Row([
            
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph', figure={})
                ]),
                
                ]),
            
            
        ])
    ]),
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('Port', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='county-prof-selector', 
                    options=[{'label':x, 'value':x} for x in sorted(df['Port'].unique())],
                    multi=False,
                    value=sorted(df['Port'].unique())[0])
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label('Year', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='Year-selector',
                    options=[{'label':i, 'value':i} for i in sorted(df['Year'].unique())],
                    multi=False,
                    value=sorted(df['Year'].unique())[0])
                ])
            ]),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div(id='table-loc',children=[
                    dash_table.DataTable(
                        id='profiler-table',
                        columns=[{'name':i, 'id':i} for i in toTable.columns],
                        data=toTable.to_dict('records'),
                        editable=True,
                        filter_action='native',
                        sort_action='native',
                        sort_mode='multi',
                        row_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_size=10,
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    dcc.Graph(id='bar-chart', figure={})
                ])
            ])
        ]),
        html.Br(),
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
                        dbc.Button('Download Dataset', id='download-bttn-bc', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-bc')
            ],  style={'margin-left': '0px', 'margin-right':'1px'}, width=2)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ]),
    ])
    
    
    
    
    
    
]
)
@app.callback(
    Output('download-bc','data'),
    Input('download-bttn-bc', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df.to_excel, 'Border Crossings.xlsx') 

@app.callback(
    Output('sidebar-space-bc','hidden'),
    [Input('edit-bc','n_clicks'),
    Input('sidebar-space-bc','hidden'),
    Input('chart-options-bc','value')]
)
def show_sidebar(button, showSidebar, graphMode):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-bc'):
        if(showSidebar):
            showSidebar=False
        else:
            showSidebar=True
    boderDataBag.getDataframe().activateDataframe(graphMode)
    return showSidebar
    

@app.callback(
    [Output(component_id='graph', component_property='figure'), 
    Output(component_id='Number1', component_property='value'),  
    ],
    (Input(component_id='select-indicator', component_property='value'),
    Input('chart-options-bc','value'))
    
    
)
def update_indicator(indicator, dummyValue):
    dff=boderDataBag.getDataframe().getActive().copy()
    dff['Date'] = pd.to_datetime(dff['Date'], format='%y%m')
    dff=dff[dff['Measure']==indicator]
    trigger_id=ctx.triggered_id
    
    

    #dff=dff[(dff['Value']>=start1) & (dff['Value']<=end1)]
    
    fig=px.line(dff, x='Date', y='Value', title=indicator+' by Port ', color='Port')
    fig.update_xaxes(nticks=len(pd.unique(dff['Year'])), rangeslider_visible=True)
    if(dummyValue=='PercentChange'):
        fig.update_yaxes(tickformat='000',ticksuffix='%')
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.', xaxis_title='Year')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    

    
    
    
    
    #dff2=dff2[(dff2['Value']>=start2) & (dff2['Value']<=end2)]
    
    dff2=boderDataBag.getDataframe().get_original().copy()
    dff2['Date'] = pd.to_datetime(df['Date'], format='%y%m')
    dff2=dff2[dff2['Measure']==indicator]
    dff2=dff2[dff2['Year']==dff2['Year'].max()]
    
    return fig, sum(dff2['Value'])



@app.callback(
    [Output(component_id='profiler-table', component_property='data'), Output(component_id='profiler-table', component_property='columns'),
    Output(component_id='bar-chart', component_property='figure')],
    [Input(component_id='county-prof-selector', component_property='value'), Input(component_id='Year-selector', component_property='value')]
    
)
def update_profiler(county, Year):
    df_profiler=df[df['Port']==county]
    df_profiler=df_profiler[df_profiler['Year']==Year]

    toTable=df_profiler[['Measure', 'Month', 'Value']]

    df_bar=df.copy()
    df_bar=df_bar[df_bar['Year']==Year]
    fig=px.bar(df_bar, x='Measure', y='Value', color='Port')
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return toTable.to_dict('records'), [{'name':i, 'id':i} for i in toTable.columns], fig

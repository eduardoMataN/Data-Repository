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

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df= pd.read_excel(DATA_PATH.joinpath("Border Crossings.xlsx"))
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
    
    dbc.Container([
        html.Br(),
        dbc.Row([
            dbc.Col(
                width=5
            ),
            dbc.Col(
                html.Div([
                    html.H1(id='section-title', children=['Border Security'], style={'color':'#041E42'})
                ]),
                width=4
            ),
            dbc.Col([
                html.Div([
                    dbc.Button(
                        "?",
                        id="click-target-1",
                        className="me-1",
                        n_clicks=0,
                        style={'color':'##FF8200'},
                        size='sm'
                    ),
                    dbc.Popover(
                        children='This first section displays information throughout the Years for each indicator by County. Use the sliders at the bottom to dicrease the Year range. You might also change the range of the Y axis using the input boxes. ',
                        target='click-target-1',
                        body=True,
                        trigger='click'
                    )
                ])
            ]),
            dbc.Col()
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.H1(id='County-title-apprehensions', children=df['Measure'].tolist()[0], style={'color':'#041E42'})
                    
                ]),
            ),
            dbc.Col(
                
                
            ),
            
            dbc.Col(
                html.Div([
                    html.H1(id='County-title-apprehensions2', children=df['Measure'].tolist()[0], style={'color':'#041E42'})
                ])
            )
            
        ])
    ]),
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                width=1
            ),
            dbc.Col(
                html.Div([
                    daq.LEDDisplay(id='Number1-apprehensions', value=initialValue, color='#FF8200')
                ]),
                
            ),
            dbc.Col(

            ),
            dbc.Col(
                html.Div([
                    daq.LEDDisplay(id='Number2-apprehensions', value=initialValue, color='#FF8200')
                ]),

            )
        ]),
        dbc.Row([
            dbc.Col(
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.H3(id='Indic-Title-apprehensions', children='Current '+ df['Measure'].tolist()[0], style={'color':'#FF8200'})
                ]),
                
            ),
            dbc.Col(
                width=4
            ),
            dbc.Col(
                html.Div([
                    html.H3(id='Indic-Title-apprehensions2', children='Current '+df['Measure'].tolist()[0], style={'color':'#FF8200'})
                ])
            )
        ])
    ]),
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.Label(['Indicator'], style={'font-weight':'bold', 'color':'#041E42'}),
                    dcc.Dropdown(id='select-indicator-apprehensions',
                                options=[{'label':x, 'value':x} for x in sorted(df.Measure.unique())],
                                multi=False,
                                value=df['Measure'].tolist()[0],
                                style={'width':'100%'},
                                optionHeight=90)
                ]),
                width=2
            ),
            dbc.Col(
                html.Div([
                    html.Label(['Initial Value'], style={'font-weight':'bold', 'width':'100%', 'color':'#041E42'}),
                      daq.NumericInput(
                        id='Y-Axes1-Start-apprehensions', min=0, max=df_copy['Value'].max(), value=0, size=80
                      )
                ], style={'width':'110%'}),
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.Label(['End Value'], style={'font-weight':'bold', 'color':'#041E42'}),
                      daq.NumericInput(
                        id='Y-Axes1-End-apprehensions', min=1, max=df_copy['Value'].max(), value=df_copy['Value'].max(), size=80
                      )
                ])
            ),
            dbc.Col(
                html.Div([
                    html.Button('Reset', id='reset-button-apprehensions', n_clicks=0)
                ]),
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.Button('Reset', id='reset-button-apprehensions2', n_clicks=0)
                ]),
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.Label(['Indicator'], style={'font-weight':'bold','color':'#041E42'}),
                    dcc.Dropdown(id='select-indicator-apprehensions2',
                        options=[{'label':x, 'value':x} for x in sorted(df.Measure.unique())],
                        multi=False,
                        value=df['Measure'].tolist()[0],
                        style={'width':'100%'},
                        optionHeight=90)
                ]), width=2
            ),
            dbc.Col(
                html.Div([
                    html.Label(['Initial Value'], style={'font-weight':'bold', 'color':'#041E42'}),
                      daq.NumericInput(
                        id='Y-Axes2-Start-apprehensions', min=0, max=df_copy['Measure'].max(), value=0, size=80
                      )
                ], style={'width':'110%'}),
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.Label(['End Value'], style={'font-weight':'bold', 'color':'#041E42'}),
                      daq.NumericInput(
                        id='Y-Axes2-End-apprehensions', min=1, max=df_copy['Value'].max(), value=df_copy['Value'].max(), size=80
                      )
                ])
            )
            
        ]),

    ]),
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph-apprehensions', figure={}, style={'height':'65vh', 'width':'60vh'})
                ]),
                
                ], width=6),
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph-apprehensions2-apprehensions', figure={}, style={'height':'65vh', 'width':'60vh'})
                ]),
                
        ]),
            
        ])
    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1(id='profiler-title',children=[('Port Analyzer')], style={'color':'#041E42'}),
                ])
            ], width=3),
            dbc.Col([
                html.Div([
                    dbc.Button(
                        "?",
                        id="click-target",
                        className="me-1",
                        n_clicks=0,
                        style={'color':'##FF8200'},
                        size='sm'
                    ),
                    dbc.Popover(
                        children='In this section, you can see information for every individual county at any given specific Year, as well as the distribution for every indicator at that given Year. Use the dropdowns to switch between counties and Years. You may also use the second row of the table to look for any specific value.',
                        target='click-target',
                        body=True,
                        trigger='click'
                    )
                ])
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('Port', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='county-prof-selector-apprehensions', 
                    options=[{'label':x, 'value':x} for x in sorted(df['Port'].unique())],
                    multi=False,
                    value=sorted(df['Port'].unique())[0])
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label('Year', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='Year-selector-apprehensions',
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
                        id='profiler-table-apprehensions',
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
                    dcc.Graph(id='bar-chart-apprehensions', figure={})
                ])
            ])
        ]),
        html.Br()
    ])
    
    
    
    
    
    
]
)

@app.callback(
    [Output(component_id='graph-apprehensions', component_property='figure'), Output(component_id='graph-apprehensions2-apprehensions', component_property='figure'), 
    Output(component_id='County-title-apprehensions', component_property='children'), Output(component_id='County-title-apprehensions2', component_property='children'),
    Output(component_id='Number1-apprehensions', component_property='value'), Output(component_id='Number2-apprehensions', component_property='value'),
    Output(component_id='Indic-Title-apprehensions', component_property='children'), Output(component_id='Indic-Title-apprehensions2', component_property='children'),
    Output(component_id='Y-Axes1-Start-apprehensions', component_property='max'), Output(component_id='Y-Axes1-End-apprehensions', component_property='min'),
    Output(component_id='Y-Axes2-Start-apprehensions', component_property='max'), Output(component_id='Y-Axes2-End-apprehensions', component_property='min'),
    Output(component_id='reset-button-apprehensions', component_property='n_clicks'),
    Output(component_id='Y-Axes1-Start-apprehensions', component_property='value'), Output(component_id='Y-Axes1-End-apprehensions', component_property='value'),
    Output(component_id='Y-Axes2-Start-apprehensions', component_property='value'), Output(component_id='Y-Axes2-End-apprehensions', component_property='value'),
    Output(component_id='reset-button-apprehensions2', component_property='n_clicks')],
    [Input(component_id='select-indicator-apprehensions', component_property='value'),
    Input(component_id='select-indicator-apprehensions2', component_property='value'),
    Input(component_id='Y-Axes1-Start-apprehensions', component_property='value'), Input(component_id='Y-Axes1-End-apprehensions', component_property='value'),
    Input(component_id='Y-Axes2-Start-apprehensions', component_property='value'), Input(component_id='Y-Axes2-End-apprehensions', component_property='value'),
    Input(component_id='reset-button-apprehensions', component_property='n_clicks'), Input(component_id='reset-button-apprehensions2', component_property='n_clicks')]
)
def update_indicator(indicator,  indicator2, start1, end1, start2, end2, resetB, resetB2):
    dff=df.copy()
    dff['Date'] = pd.to_datetime(df['Date'], format='%y%m')
    dff=dff[dff['Measure']==indicator]
    trigger_id=ctx.triggered_id
    if(trigger_id=='select-indicator-apprehensions'):
        resetB+=1
    if(resetB>0):
        start1= 0 #dff['Value'].min()
        end1=dff['Value'].max()
        resetB=0

    #dff=dff[(dff['Value']>=start1) & (dff['Value']<=end1)]
    
    fig=px.line(dff, x='Date', y='Value', title=indicator+' by Port ', color='Port',  width=750, height=720)
    fig.update_xaxes(nticks=len(pd.unique(dff['Year'])), rangeslider_visible=True)
    fig.update_layout(yaxis_range=[start1,end1])
    fig.update_layout(legend=dict(
    orientation="v",
    yanchor="top",
    y=1,
    xanchor="left",
    x=-0.3
    ))
    fig.update_layout(title_y=1, title_x=0.5, margin=dict(l=0, r=0, t=0, b=0))
    fig.update_yaxes(visible=False)
    

    dff2=df.copy()
    dff['Date'] = pd.to_datetime(df['Date'], format='%y%m')
    dff2=dff2[dff2['Measure']==indicator2]
    if(trigger_id=='select-indicator-apprehensions2'):
        resetB2+=1
    if(resetB2>0):
        start2=0  #dff2['Value'].min()
        end2=dff2['Value'].max()
        resetB2=0
    
    #dff2=dff2[(dff2['Value']>=start2) & (dff2['Value']<=end2)]
    fig2=px.line(dff2,x='Date', y='Value', title=indicator2+' by County ', color='Port',  width=750, height=720)
    fig2.update_xaxes(nticks=len(pd.unique(dff2['Year'])), rangeslider_visible=True)
    fig2.update_layout(yaxis_range=[start2,end2])
    
    fig2.update_layout(title_y=1, title_x=0.5, margin=dict(l=0, r=0, t=0, b=0))
    dff=dff[dff['Year']==dff['Year'].max()]
    dff2=dff2[dff2['Year']==dff2['Year'].max()] 
    return fig, fig2, indicator, indicator2, sum(dff['Value']), sum(dff2['Value']), 'Current '+indicator, 'Current '+indicator2, end1-1, start1+1, end2-1, start2+1, resetB, start1, end1, start2, end2, resetB2



@app.callback(
    [Output(component_id='profiler-table-apprehensions', component_property='data'), Output(component_id='profiler-table-apprehensions', component_property='columns'),
    Output(component_id='bar-chart-apprehensions', component_property='figure')],
    [Input(component_id='county-prof-selector-apprehensions', component_property='value'), Input(component_id='Year-selector-apprehensions', component_property='value')]
    
)
def update_profiler(county, Year):
    df_profiler=df[df['Port']==county]
    df_profiler=df_profiler[df_profiler['Year']==Year]

    toTable=df_profiler[['Measure', 'Month', 'Value']]

    df_bar=df.copy()
    df_bar=df_bar[df_bar['Year']==Year]
    fig=px.bar(df_bar, x='Measure', y='Value', color='Port')

    return toTable.to_dict('records'), [{'name':i, 'id':i} for i in toTable.columns], fig

    


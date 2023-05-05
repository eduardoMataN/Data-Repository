
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
from dash.dash_table import FormatTemplate

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_edu=pd.read_excel(DATA_PATH.joinpath('Educational Attainment and Rate.xlsx'))
educDataset=dataset('Educational Attainment Rate by County', df_edu, 'Value', 'line-edu', 'County','Value')
educDataset.modify_percent_change(['County', 'Age'], 'Educational Attainment', 'Value')
educDatabag=dataBag([educDataset])
percentage=FormatTemplate.percentage(2)

layout=html.Div(children=[
    html.Div(id='sidebar-space-educ',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-educ',children='Educational Attainment Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-educ',
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
    dbc.Container(children=[
    html.Br(),
        dbc.Row([
            dbc.Col([
                html.H2(['Educational Attainment Rate by County'], style=TITLE)
            ]),
            html.Hr(style=HR)
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Label(['County'], style=LABEL),
                dcc.Dropdown(
                    id='select-county-edu',
                    options=[{'label':x,'value':x}for x in df_edu['County'].unique()],
                    value=df_edu['County'].unique()[0],
                    style=DROPDOWN,
                    optionHeight=90
                )
            ]),
            dbc.Col([
                html.Label(['Age'], style=LABEL),
                dcc.Dropdown(
                    id='select-age-edu',
                    options=[{'label':x,'value':x}for x in df_edu['Age'].unique()],
                    value=df_edu['Age'].unique()[0],
                    style=DROPDOWN,
                    optionHeight=90
                )
            ]),
            dbc.Col([
                html.Div([
                    ALIGN_LABEL,
                    html.Br(),
                    dbc.Button('Edit Graph', id='edit-educ', outline=True, color="primary", className="me-1", value='edit')
                ])
            ], width=2),
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='line-edu',
                        figure={}
                    )
                ])
                
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                html.Label(['Year'], style=LABEL),
                    dcc.Dropdown(
                        id='select-year-educ',
                        options=[{'label':x,'value':x}for x in df_edu['Year'].unique()],
                        value=df_edu['Year'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90
                    ),
                    html.Br(),
                    dash_table.DataTable(
                        id='educ-table',
                        columns=[{'name':i, 'id':i, 'type':'numeric', 'format':percentage } for i in df_edu[(df_edu['County']==df_edu['County'].unique()[0]) &(df_edu['Age']==df_edu['Age'].unique()[0])&(df_edu['Year']==df_edu['Year'].unique()[0])][['Educational Attainment', 'Percentage']].columns],
                        data=df_edu[(df_edu['County']==df_edu['County'].unique()[0]) &(df_edu['Age']==df_edu['Age'].unique()[0])&(df_edu['Year']==df_edu['Year'].unique()[0])][['Educational Attainment', 'Percentage']].to_dict('records'),
                        editable=True,
                        sort_action='native',
                        sort_mode='multi',
                        row_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_size=10,
                        style_cell={'font-family':'Arial', 'textAlign':'center'},
                        style_header={'font-family':'Arial'}
                    )
                ])
            ])
        ]),
        html.Br(),
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
                        html.P('Last Update: 2020', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Source: USA Gov', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-educ', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-educ')
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
    Output('download-educ','data'),
    Input('download-bttn-educ', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_edu.to_excel, 'Educational Attainment Data.xlsx')

@app.callback(
    
    Output('sidebar-space-educ', 'hidden'),
    [Input('edit-educ', 'n_clicks'),
    Input('sidebar-space-educ', 'hidden'),
    Input('chart-options-educ', 'value')]
)
def get_sidebar(button, showSideBar, chartMode):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-educ'):
        if(showSideBar):
            showSideBar=False
        else:
            showSideBar=True
    educDatabag.getDataframe().activateDataframe(chartMode)
    return showSideBar
    

@app.callback(
    [Output('line-edu', 'figure'),
    Output('educ-table','data'),
    Output('educ-table', 'columns')],
    [Input('select-county-edu','value'),
    Input('select-age-edu','value'),
    Input('select-year-educ','value'),
    Input('chart-options-educ','value')]
    
)
def update_data(county, age,year, dummyValue):
    dff=educDatabag.getDataframe().getActive().copy()
    fig=px.line(dff[(dff['County']==county)&(dff['Age']==age)], x='Year', y='Value', color='Educational Attainment', color_discrete_sequence=get_colors(dff['Educational Attainment'].unique()))
    fig.update_xaxes( rangeslider_visible=True)
    if(dummyValue=='PercentChange'):
        fig.update_yaxes(ticksuffix='%')
    toTable=df_edu[(df_edu['County']==county) &(df_edu['Age']==age)&(df_edu['Year']==year)][['Educational Attainment', 'Percentage']]
    columns=[{'name':i, 'id':i} for i in toTable.columns]
    data=toTable.to_dict('records')
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return fig, data, columns
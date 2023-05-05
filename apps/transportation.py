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

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df= pd.read_excel(DATA_PATH.joinpath("Border Crossings.xlsx"))
df_copy=df.copy()
maxYear=df['Year'].max()
df_copy=df[df['Measure']=='Personal Vehicle Passengers']
initialValue=sum(df_copy.loc[df_copy.Year==maxYear, 'Value'].tolist())
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
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H1(id='Port-Title-transp', children=df['Measure'].tolist()[0], style={'color':'#041E42', 'text-align':'center'})
                    
                ]),
            ),
            dbc.Col(
                html.Div([
                    html.H1(id='section-title-transp', children=['Transportation'], style={'color':'#041E42', 'text-align':'Center'})
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H1(id='Port-Title2-transp', children=df['Measure'].tolist()[0], style={'color':'#041E42'})
                ])
            )
            
        ])
    ]),
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    daq.LEDDisplay(id='Number1-transp', value=initialValue, color='#FF8200')
                ])
                
            ),
            dbc.Col(

            ),
            dbc.Col(
                html.Div([
                    daq.LEDDisplay(id='Number2-transp', value=initialValue, color='#FF8200')
                ]),

            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H3(id='Indic-Title-transp', children='Current '+ df['Measure'].tolist()[0], style={'color':'#FF8200'})
                ])
            ),
            dbc.Col(

            ),
            dbc.Col(
                html.Div([
                    html.H3(id='Indic-Title2-transp', children='Current '+df['Measure'].tolist()[0], style={'color':'#FF8200'})
                ])
            )
        ])
    ]),
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label(['Measure'], style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-Measure',
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
                    html.Label(['Initial Value'], style={'font-weight':'bold', 'width':'100%'}),
                      daq.NumericInput(
                        id='Y-Axes1-Start-transp', min=0, max=df_copy['Value'].max(), value=0, size=80
                      )
                ], style={'width':'110%'}),
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.Label(['End Value'], style={'font-weight':'bold'}),
                      daq.NumericInput(
                        id='Y-Axes1-End-transp', min=1, max=df_copy['Value'].max(), value=df_copy['Value'].max(), size=80
                      )
                ])
            ),
            dbc.Col(
                html.Div([
                    html.Button('Reset', id='reset-button-transp', n_clicks=0)
                ]),
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.Button('Reset', id='reset-button2-transp', n_clicks=0)
                ]),
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.Label(['Measure'], style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-Measure2-transp',
                        options=[{'label':x, 'value':x} for x in sorted(df.Measure.unique())],
                        multi=False,
                        value=df['Measure'].tolist()[0],
                        style={'width':'100%'},
                        optionHeight=90)
                ]), width=2
            ),
            dbc.Col(
                html.Div([
                    html.Label(['Initial Value'], style={'font-weight':'bold'}),
                      daq.NumericInput(
                        id='Y-Axes2-Start-transp', min=0, max=df_copy['Value'].max(), value=0, size=80
                      )
                ], style={'width':'110%'}),
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.Label(['End Value'], style={'font-weight':'bold'}),
                      daq.NumericInput(
                        id='Y-Axes2-End-transp', min=1, max=df_copy['Value'].max(), value=df_copy['Value'].max(), size=80
                      )
                ])
            )
            
        ]),

    ]),
    dbc.Container(children=[
        dbc.Row([
            
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph-transp', figure={}, style={'height':'65vh', 'width':'60vh'})
                ]),
                
                ]),
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph2-transp', figure={}, style={'height':'65vh', 'width':'60vh'})
                ]),
                
        ]),
            
        ])
    ])
    
    
    
    
    
    
]
)

@app.callback(
    [Output(component_id='graph-transp', component_property='figure'), Output(component_id='graph2-transp', component_property='figure'), 
    Output(component_id='Port-Title-transp', component_property='children'), Output(component_id='Port-Title2-transp', component_property='children'),
    Output(component_id='Number1-transp', component_property='value'), Output(component_id='Number2-transp', component_property='value'),
    Output(component_id='Indic-Title-transp', component_property='children'), Output(component_id='Indic-Title2-transp', component_property='children'),
    Output(component_id='Y-Axes1-Start-transp', component_property='max'), Output(component_id='Y-Axes1-End-transp', component_property='min'),
    Output(component_id='Y-Axes2-Start-transp', component_property='max'), Output(component_id='Y-Axes2-End-transp', component_property='min'),
    Output(component_id='reset-button-transp', component_property='n_clicks'),
    Output(component_id='Y-Axes1-Start-transp', component_property='value'), Output(component_id='Y-Axes1-End-transp', component_property='value'),
    Output(component_id='Y-Axes2-Start-transp', component_property='value'), Output(component_id='Y-Axes2-End-transp', component_property='value'),
    Output(component_id='reset-button2-transp', component_property='n_clicks')],
    [Input(component_id='select-Measure', component_property='value'),
    Input(component_id='select-Measure2-transp', component_property='value'),
    Input(component_id='Y-Axes1-Start-transp', component_property='value'), Input(component_id='Y-Axes1-End-transp', component_property='value'),
    Input(component_id='Y-Axes2-Start-transp', component_property='value'), Input(component_id='Y-Axes2-End-transp', component_property='value'),
    Input(component_id='reset-button-transp', component_property='n_clicks'), Input(component_id='reset-button2-transp', component_property='n_clicks')]
)
def update_Measure(Measure,  Measure2, start1, end1, start2, end2, resetB, resetB2):
    dff=df.copy()
    dff=dff[dff['Measure']==Measure]
    trigger_id=ctx.triggered_id
    if(trigger_id=='select-Measure'):
        resetB+=1
    if(resetB>0):
        start1= 0 #dff['Value'].min()
        end1=dff['Value'].max()
        resetB=0

    #dff=dff[(dff['Value']>=start1) & (dff['Value']<=end1)]
    
    fig=px.line(dff, x='Year', y='Value', title=Measure+' by Port ', color='Port',  width=700, height=650)
    fig.update_xaxes(nticks=len(pd.unique(dff['Year'])), rangeslider_visible=True)
    fig.update_layout(yaxis_range=[start1,end1])


    dff2=df.copy()
    dff2=dff2[dff2['Measure']==Measure2]
    if(trigger_id=='select-Measure2'):
        resetB2+=1
    if(resetB2>0):
        start2=0  #dff2['Value'].min()
        end2=dff2['Value'].max()
        resetB2=0
    
    #dff2=dff2[(dff2['Value']>=start2) & (dff2['Value']<=end2)]
    fig2=px.line(dff2,x='Year', y='Value', title=Measure2+' by Port ', color='Port',  width=700, height=650)
    fig2.update_xaxes(nticks=len(pd.unique(dff2['Year'])), rangeslider_visible=True)
    fig2.update_layout(yaxis_range=[start2,end2])
    dff3=df.copy()
    dff=dff[dff['Year']==dff['Year'].max()]
    dff2=dff2[dff2['Year']==dff2['Year'].max()]


    
    return fig, fig2, Measure, Measure2, sum(dff['Value']), sum(dff2['Value']), 'Current '+Measure, 'Current '+Measure2, end1-1, start1+1, end2-1, start2+1, resetB, start1, end1, start2, end2, resetB2

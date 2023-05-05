
import pandas as pd
import plotly.express as px
import dash as dash
from dash import dcc, ctx
from dash import html, dash_table, no_update
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

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_age=pd.read_excel(DATA_PATH.joinpath('Poverty by Age.xlsx'))
ageDataset=dataset('Poverty by Age Chart', df_age, name='tab-age')
#ageDataset.modify_percent_change('County', 'Age', 'Percentage')
df_sex=pd.read_excel(DATA_PATH.joinpath('Poverty by Sex.xlsx'))
sexDataset=dataset('Poverty by Sex Chart', df_sex, name='tab-sex')
#sexDataset.modify_percent_change('County', 'Sex', 'Percentage')
df_educ=pd.read_excel(DATA_PATH.joinpath('Poverty by Educational Attainment.xlsx'))
educDataset=dataset('Povery by Educational Attaintment Chart', df_educ, name='tab-educ')
#educDataset.modify_percent_change('County', 'Educational Attainment', 'Percentage')
df_race=pd.read_excel(DATA_PATH.joinpath('Poverty by Race.xlsx'))
raceDataset=dataset('Poverty by Race Chart', df_race, name='tab-race')
#raceDataset.modify_percent_change('County', 'Race', 'Percentage')
povertyDatabag=dataBag([ageDataset, sexDataset, raceDataset, educDataset])


layout=html.Div([
    
    dbc.Container([
    html.Br(),
    dcc.Tabs(id='poverty-tabs', value='tab-age', children=[
        dcc.Tab(label='By Age', value='tab-age', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='By Race', value='tab-race', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='By Sex', value='tab-sex', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='By Educational Attainment', value='tab-educ', style=tab_style, selected_style=tab_selected_style)
    ])]),
    html.Br(),
    html.Div(id='content-div', children=[
        dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(id='section-title',children=['Poverty By Age'], style=TITLE)
                ])
            ]),
            html.Hr(style=HR)
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(id='county-dropdown-label', children=['County'], style=LABEL),
                    dcc.Dropdown(
                        id='select-county',
                        options=[{'label':x, 'value':x}for x in df_age['County'].unique()],
                        value=df_age['County'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=False
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label(id='category-dropdown-label',children=['Age'], style=LABEL),
                    dcc.Dropdown(
                        id='select-category',
                        options=[{'label':x,'value':x}for x in df_age['Age'].unique()],
                        value=df_age['Age'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=True
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    daq.ToggleSwitch(
                        id='toggle-poverty',
                        label='By County/By Age',
                        labelPosition='top',
                        value=False,
                        style=LABEL,
                        disabled=False
                    )
                ])
            ], width=2),
            
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='poverty-graph',
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
                        html.P('Last Update: 2020', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        ALIGN_LABEL,
                        html.P('Source: USA Gov', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-pov', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-pov')
            ],  style={'margin-left': '0px', 'margin-right':'1px'})
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
    Output('download-pov','data'),
    [Input('download-bttn-pov', 'n_clicks'),
    Input('poverty-tabs','value')],
    prevent_initial_call=True
)
def download_median(downloadB, currentTab):
    trigger_id=ctx.triggered_id
    if(trigger_id=='poverty-tabs'):
        return no_update
    if(currentTab=='tab-age'):
        return dcc.send_data_frame(df_age.to_excel, 'Povery by Age Data.xlsx')
    if(currentTab=='tab-race'):
        return dcc.send_data_frame(df_race.to_excel, 'Povery by Age Data.xlsx')
    if(currentTab=='tab-sex'):
        return dcc.send_data_frame(df_sex.to_excel, 'Povery by Age Data.xlsx')
    if(currentTab=='tab-educ'):
        return dcc.send_data_frame(df_educ.to_excel, 'Povery by Age Data.xlsx')

@app.callback(
    [Output('section-title', 'children'),
    Output('select-county','options'), Output('select-county','value'), Output('select-county','disabled'),
    Output('category-dropdown-label','children'), Output('select-category','options'), Output('select-category','value'), Output('select-category','disabled'),
    Output('toggle-poverty','label'),
    Output('poverty-graph','figure')],
    [Input('poverty-tabs', 'value'),
    Input('select-county','options'), Input('select-county','value'),
    Input('select-category','options'), Input('select-category','value'),
    Input('toggle-poverty','value'), Input('toggle-poverty','label'),
    Input('category-dropdown-label', 'children')]
)
def update_content(tab, countyOptions, countyValue, categoryOptions, categoryValue, toggleValue, toggleLabel, categoryLabel):
    trigger_id=ctx.triggered_id
    dff=povertyDatabag.getByName(tab).getActive().copy()
    disableCounty=False
    disableCategory=False
    if(tab=='tab-age'):
        #dff=df_age.copy()
        title=['Poverty By Age']
        if(trigger_id=='poverty-tabs'):
            countyOptions=[{'label':x,'value':x}for x in dff['County'].unique()]
            countyValue=dff['County'].unique()[0]
            categoryOptions=[{'label':x,'value':x}for x in dff['Age'].unique()]
            categoryValue=dff['Age'].unique()[0]
            categoryLabel=['Age']
            toggleLabel='By County/By Age'
        if(toggleValue):
            dff=dff[dff['County']==countyValue]
            fig=px.line(dff, x='Year',y='Percentage', color='Age', color_discrete_sequence=get_colors(dff['Age'].unique()))
            disableCategory=True
        else:
            dff=dff[dff['Age']==categoryValue]
            fig=px.line(dff,x='Year',y='Percentage',color='County', color_discrete_sequence=get_colors(dff['County'].unique()))
            disableCounty=True
            
        
    elif(tab=='tab-race'):
        #dff=df_race.copy()
        title=['Poverty By Race']
        if(trigger_id=='poverty-tabs'):
            countyOptions=[{'label':x,'value':x}for x in dff['County'].unique()]
            countyValue=dff['County'].unique()[0]
            categoryOptions=[{'label':x,'value':x}for x in dff['Race'].unique()]
            categoryValue=dff['Race'].unique()[0]
            categoryLabel=['Race']
            toggleLabel='By County/By Race'
        if(toggleValue):
            dff=dff[dff['County']==countyValue]
            fig=px.line(dff, x='Year',y='Percentage', color='Race', color_discrete_sequence=get_colors(dff['Race'].unique()))
            disableCategory=True
        else:
            dff=dff[dff['Race']==categoryValue]
            fig=px.line(dff,x='Year',y='Percentage',color='County', color_discrete_sequence=get_colors(dff['County'].unique()))
            disableCounty=True
        
    elif(tab=='tab-sex'):
        #dff=df_sex.copy()
        title=['Poverty By Sex']
        if(trigger_id=='poverty-tabs'):
            countyOptions=[{'label':x,'value':x}for x in dff['County'].unique()]
            countyValue=dff['County'].unique()[0]
            categoryOptions=[{'label':x,'value':x}for x in dff['Sex'].unique()]
            categoryValue=dff['Sex'].unique()[0]
            categoryLabel=['Sex']
            toggleLabel='By County/By Sex'
        if(toggleValue):
            dff=dff[dff['County']==countyValue]
            fig=px.line(dff, x='Year',y='Percentage', color='Sex', color_discrete_sequence=get_colors(dff['Sex'].unique()))
            disableCategory=True
        else:
            dff=dff[dff['Sex']==categoryValue]
            fig=px.line(dff,x='Year',y='Percentage',color='County', color_discrete_sequence=get_colors(dff['County'].unique()))
            disableCounty=True
        
    elif(tab=='tab-educ'):
        #dff=df_educ.copy()
        title=['Poverty By Educational Attainment']
        if(trigger_id=='poverty-tabs'):
            countyOptions=[{'label':x,'value':x}for x in dff['County'].unique()]
            countyValue=dff['County'].unique()[0]
            categoryOptions=[{'label':x,'value':x}for x in dff['Educational Attainment'].unique()]
            categoryValue=dff['Educational Attainment'].unique()[0]
            categoryLabel=['Educational Attainment']
            toggleLabel='By County/By Educational Attainment'
        if(toggleValue):
            dff=dff[dff['County']==countyValue]
            fig=px.line(dff, x='Year',y='Percentage', color='Educational Attainment', color_discrete_sequence=get_colors(dff['Educational Attainment'].unique()))
            disableCategory=True
        else:
            dff=dff[dff['Educational Attainment']==categoryValue]
            fig=px.line(dff,x='Year',y='Percentage',color='County', color_discrete_sequence=get_colors(dff['County'].unique()))
            disableCounty=True
        
    else:
        title=['Poverty By Age']
        #dff=df_age.copy()
        title=['Poverty By Age']
        if(trigger_id=='poverty-tabs'):
            countyOptions=[{'label':x,'value':x}for x in dff['County'].unique()]
            countyValue=dff['County'].unique()[0]
            categoryOptions=[{'label':x,'value':x}for x in dff['Age'].unique()]
            categoryValue=dff['Age'].unique()[0]
            categoryLabel=['Age']
            toggleLabel='By County/By Age'
        if(toggleValue):
            dff=dff[dff['Age']==categoryValue]
            fig=px.line(dff,x='Year',y='Percentage',color='County', color_discrete_sequence=get_colors(dff['County'].unique()))
            disableCounty=True
        else:
            dff=dff[dff['County']==countyValue]
            fig=px.line(dff, x='Year',y='Percentage', color='Age', color_discrete_sequence=get_colors(dff['Age'].unique()))
            disableCategory=True
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(legend_title_text=f'Click to hide.<br>Double click to isolate.')
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    return title, countyOptions, countyValue, disableCounty, categoryLabel,categoryOptions, categoryValue, disableCategory,toggleLabel, fig

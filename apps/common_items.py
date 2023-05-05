import random
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


legend_colors={0:'#041E42',
            1:'#FF8200', 
            2:'#fff100', 
            3:'#19C824', 
            4:'#AEF6C1', 
            5:'#F98FD9', 
            6:'#C7AFDD', 
            7:'#93F9F6', 
            8:'#FF8200',
            9:'#A4C350',
            10:'#37EDCF',
            11:'#FF3185',
            12:'#D399FD',
            13:'#46C1FB',
            14:'#B1B3B3',
            15:'#F05A28',
            16:'#D8E877',
            17:'#16E487',
            18:'#F039EE',
            19:'#8D73D5',
            20:'#2011B3',
            21:'#D6A00B',
            22:'#EB1427',
            23:'#69A166',
            24:'#3A7538',
            25:'#6905F6',
            26:'#652D90',
            27:'#2D447C',
            28:'#8A6C63',
            29:'#990000',
            30:'#065624',
            31:'#93D8C2',
            32:'#921559',
            33:'#45394F',
            34:'#041E42',
            35:'#FB4E2D'
}
OPTION_BUTTONS=dbc.RadioItems(
            id='chart-options',
            options=[
                {'label':'Percent Change','value':'percent-change'},
                {'label': 'Original Chart','value':'original'}
            ],
            value='original'
        )
blue='#041E42'
orange='#FF8200'
white='#FFFFFF'
black='#000000'
INFO_BOX_STYLE={'color':blue}
LABEL={'font-weight':'bold', 'color':'#041E42'}
TITLE={'color':'#041E42'}
DROPDOWN={'width':'100%'}
ALIGN_LABEL=html.Label(['Edit'], style={'color':'#ffffff'})
HR={'color':blue, 'borderWidth': "0.3vh", 'borderColor':blue, 'opacity':'unset', 'width':'100%'}
TILE_HR=html.Hr(style={'color':blue, 'borderWidth': "0.3vh", 'borderColor':blue, 'opacity':'unset', 'width':'100%'})
COMPARE_LABEL=html.Label('Click to Compare', style={ 'textAlign': 'center', 'font-weight':'bold', 'color':'#041E42'})
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#FF8200',
    'color': 'white',
    'padding': '6px'
}

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
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
 #Once we're on that path, we go into datasets. 
def get_colors(legend):
    final_color_list=[]
    for i in range(0, len(legend)):
        if(i>len(legend_colors)-1):
            r = lambda: random.randint(0,255)
            final_color_list.append('#%02X%02X%02X' % (r(),r(),r()))
        else:
            final_color_list.append(legend_colors[i])
    return final_color_list
def create_subplot(fig,row, col, df, xaxes, yaxes, names):
    df_sub=df.copy()
    legend=df_sub[names].unique()
    colors=get_colors(legend)
    for index, name in enumerate(legend):
        df_ind=df_sub[df_sub[names]==name]
        x=df_ind[xaxes]
        y=df_ind[yaxes]
        fig.add_trace(go.Scatter(x=x, y=y, name=name, marker=dict(color=colors[index])), row=row, col=col)
    
    
        
    return fig
def get_options(df, col):
    return [{'label':x,'value':x}for x in df[col].unique()]
def filter_df(df, col, value):
    return df[df[col]==value]
def sum_df(df, sumCol, sumBy, target):
    newDf={sumBy:[], sumCol:[], target:[]}
    colValues=df[sumCol].unique()
    sumByValues=df[sumBy].unique()
    for sumValue in sumByValues:
        for value in colValues:
            df_temp=filter_df(df, sumBy, sumValue)
            df_temp=filter_df(df_temp, sumCol, value)
            newDf[sumBy].append(sumValue)
            newDf[sumCol].append(value)
            newDf[target].append(sum(df_temp[target]))
   
    return pd.DataFrame.from_dict(newDf)


def generate_sidebar(title, buttons):
    sidebar=html.Div(
    [
        html.H6(id='sidebar-title',children=title),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        buttons,
        
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        


        dbc.Button('Hide', id='hide-button', outline=True, color="primary", className="me-1", value='hide', n_clicks=0 )
    ],
    style=SIDEBAR_STYLE,
    )
    return sidebar







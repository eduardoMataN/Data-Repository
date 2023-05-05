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

layout=html.Div([
    html.Iframe(
    src='https://arcg.is/18zvmX',
    width=1500,
    height=1500
    )
])
import pathlib
import pandas as pd
import plotly.express as px
import dash as dash
from dash import dcc, ctx
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State

# Connect to main app.py file
from app import app
from app import server

from apps import border_security, common_items, demographic_indicators, economic_indicators_trade, education, social_indicators, transportation, transportation_border_crossings, economic_indicators_income, demographic_indicators_population, economic_indicators_employment, economic_indicators_industry, economic_indicators_remittances, social_indicators_crime, transportation_airport_activity, education_educational_attaintment_rate, social_indicators_poverty, border_security_apprehensions, border_security_staffing, border_security_migration
app.layout=html.Div(children=[dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(children=[
    dbc.DropdownMenu(
        [
             
            dbc.DropdownMenuItem('Population', href='/apps/demographic_indicators_population') 
        ],
        label='Demographic Indicators',
        toggle_style={
            'background':'#041E42',
            'border':'#041E42'
        }
    ),
    dbc.DropdownMenu([
        dbc.DropdownMenuItem('International Trade Flows',href='/apps/economic_indicators_trade'),
        dbc.DropdownMenuItem('Income', href='/apps/economic_indicators_income'),
        dbc.DropdownMenuItem('Employment', href='/apps/economic_indicators_employment'),
        dbc.DropdownMenuItem('Industry', href='/apps/economic_indicators_industry'),
        dbc.DropdownMenuItem('Remittances', href='/apps/economic_indicators_remittances')
    ],
    label='Economic Indicators',
    toggle_style={
            'background':'#041E42',
            'border':'#041E42'
        }),
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem('Apprehensions', href='/apps/border_security_apprehensions'),
            dbc.DropdownMenuItem('Border Patrol Agent Staffing', href='/apps/border_security_staffing'),
            dbc.DropdownMenuItem('Migration Indicators', href='/apps/border_security_migration')
            
        ],
        label='Border Security',
        toggle_style={
            'background':'#041E42',
            'border':'#041E42'
        }
    ),
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem('Educational Attaintment', href='/apps/education_educational_attaintment_rate')
        ],
        label='Education', 
        toggle_style={
            'background':'#041E42',
            'border':'#041E42'
        }
    ),
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem('Crime', href='/apps/social_indicators_crime'),
            dbc.DropdownMenuItem('Poverty', href='/apps/social_indicators_poverty')
        ],
        label='Social Indicators',
        toggle_style={
            'background':'#041E42',
            'border':'#041E42'
        }

    ),
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem('Border Crossings', href='/apps/transportation_border_crossings'),
            dbc.DropdownMenuItem('Airport Activity', href='/apps/transportation_airport_activity'),
            
        ],
        label='Transportation',
        toggle_style={
            'background':'#041E42',
            'border':'#041E42'
        }
    )
        ],
        brand='HIBRED',
        brand_href='#',
        color='#041E42',
        style={'font-weight':'bold'},
        className='navbar-dark'
        ),
        html.Div(id='page-content', children=[]),
        
])

@app.callback(Output(component_id='page-content', component_property='children'), 
                [Input(component_id='url', component_property='pathname')])
                
def display_page(pathname):
    if pathname == '/apps/border_security':
        return border_security.layout
    if pathname == '/apps/economic_indicators':
        return economic_indicators_trade.layout
    if pathname == '/apps/education':
        return education.layout
    if pathname == '/apps/social_indicators_crime':
        return social_indicators_crime.layout
    if pathname == '/apps/transportation':
        return transportation.layout
    if pathname == '/apps/transportation_border_crossings':
        return transportation_border_crossings.layout
    if pathname == '/apps/economic_indicators_trade':
        return economic_indicators_trade.layout
    if pathname == '/apps/economic_indicators_income':
        return economic_indicators_income.layout
    if pathname == '/apps/demographic_indicators_population':
        return demographic_indicators_population.layout
    if pathname == '/apps/economic_indicators_employment':
        return economic_indicators_employment.layout
    if pathname == '/apps/economic_indicators_industry':
        return economic_indicators_industry.layout
    if pathname == '/apps/economic_indicators_remittances':
        return economic_indicators_remittances.layout
    if pathname == '/apps/transportation_airport_activity':
        return transportation_airport_activity.layout
    if pathname == '/apps/education_educational_attaintment_rate':
        return education_educational_attaintment_rate.layout
    if pathname == '/apps/social_indicators_poverty':
        return social_indicators_poverty.layout
    if pathname == '/apps/border_security_apprehensions':
        return border_security_apprehensions.layout
    if pathname == '/apps/border_security_staffing':
        return border_security_staffing.layout
    if pathname == '/apps/border_security_migration':
        return border_security_migration.layout
    else:
        return economic_indicators_income.layout



if __name__ == '__main__':
    app.run_server(debug=True)




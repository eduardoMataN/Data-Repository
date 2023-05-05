import dash 
import dash_bootstrap_components as dbc

app=dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name':'viewport',
                            'content': 'width=device-width, initial-scale='}], external_stylesheets=[dbc.themes.BOOTSTRAP]
                            ) #Creating app object
server=app.server #Creating server object
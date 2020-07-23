import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'Forecasts'
server = app.server

app.layout = html.Div(children=[
    html.H1(myheading),

    ]
)


if __name__ == '__main__':
    app.run_server()

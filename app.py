import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go


# ---------------------------- Set up raw data ---------------------------
# ========================================================================
# 1. F O R  G D P   F O R E C A S T   G R A P H

    # forecast data
fct = pd.read_csv('forecast.csv')


    # Colors from tab10 palette
colors = ['#d62728', '#ff7f0e', '#1f77b4'][::-1] 

          
          
########### Set up the chart


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Forecast'

########### Set up the layout
app.layout = html.Div(children=[
    html.H1('DANIEL'),
    dcc.Graph(
        id='flyingdog',
    ),
    html.A('Code on Github'),
    html.Br(),
    html.A('Data Source'),
    ]
)

if __name__ == '__main__':
    app.run_server()

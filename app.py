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

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "45rem",
    "padding": "2rem 0rem",
    "background-color": "#f3f6fa", ##f8f9fa
    "font-size": "1.5rem",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "45rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(

)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# Make annotations
@app.callback(Output("text", "children"), [Input("slider", "value")])
def make_text(value):
    if value is None:
        value = 0
 
if __name__ == '__main__':
    app.run_server()

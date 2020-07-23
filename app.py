import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

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

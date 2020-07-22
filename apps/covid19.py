import dash_core_components as dcc   
import plotly.graph_objs as go  
from dash.dependencies import Input, Output
import pandas as pd 

from apps import template
from apps.app import dash_app

APPS_NAME = 'covid19 xxx'
df = pd.read_json('https://covid19.mathdro.id/api/daily')
df['reportDate'] = pd.to_datetime(df['reportDate'])

dropdown_menu = dcc.Dropdown(id='data-input-' + APPS_NAME,
                            options=[ {'label': 'Data Harian Dunia', 'value': 'data-harian-dunia'}],
                            value=['data-harian-dunia'],
                            multi=True)

layout = template.template(APPS_NAME, dropdown_menu) 

def covid19(value_name: str):
    data_1 = go.Scatter(x=df['reportDate'], y=df['totalConfirmed'], name="Total Confirmed", mode="lines+markers")
    data = [data_1]
    layout = dict(title='Total Positif Covid 19 di Seluruh Dunia xxx',
                xaxis=dict(title='Hari'),
                yaxis=dict(title='Jumlah Kumulatif'),
    )
    fig = dict(data=data, layout=layout)
    return dcc.Graph(
        id=value_name,
        figure=fig,
    )

@dash_app.callback(
    Output('graphs-' + APPS_NAME, 'children'),
    [Input('data-input-' + APPS_NAME, 'value')],
)
def update_graph(data):
    graphs = []
    for x in data:
        if x == 'data-harian-dunia':
            graphs.append(covid19(x))
 
    return graphs

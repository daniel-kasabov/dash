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


    # historical data
# hist = pd.read_excel('history.xlsx', index_col=None, header=0)
hist = pd.read_csv('history.csv', index_col=None, header=0)
hist.dropna(subset=['datetime', 'GDP'], inplace = True)

    # forecast data
# fct = pd.read_excel('forecast.xlsx', index_col=None, header=0)
fct = pd.read_csv('forecast.csv', index_col=None, header=0)
fct.dropna(subset=['Model'], inplace = True)

    # available models
available_models = list(fct['Model'].unique())
    # dates with available forecast periods
# fct_period = pd.period_range(hist['datetime'].iloc[-1], freq='Q', periods=5)
fct_period = pd.period_range(hist['datetime'].iloc[-2], freq='Q', periods=6)
fct_period = fct_period[1:].asfreq('M', how='E')
fct_period = fct_period.to_timestamp()

    # Colors from tab10 palette
colors = ['#d62728', '#ff7f0e', '#1f77b4'][::-1] 

          
# 2. F O R  N O W C A S T   G R A P H
#colors_ncst = ['#37AB65', '#3DF735', '#AD6D70', '#EC2504', '#8C0B90', '#C0E4FF', '#27B502', '#7C60A8', '#CF95D7', '#145JKH']          
colors_ncst = ['red', 'turquoise', 'gold', 'lime', 'deeppink','mediumblue', 'blanchedalmond', 'lightslategray', 'darkseagreen', 'olive', 'purple']          

# ncst = pd.read_excel('nowcast.xlsx', index_col=0, header=0)
ncst = pd.read_csv('nowcast.csv', index_col=0, header=0)
ncst.dropna(subset=['GDP Nowcast'], inplace = True)


ncst_period = ncst.index

categ = ncst.columns.to_list()

data_ncst = []
trace = go.Scatter(
            x = ncst_period,
            y = ncst['GDP Nowcast'],
            hoverinfo="y",
            line={"color": "black","width": 2.5},
            name = 'GDP Nowcast',
            marker = {'color': "black"})
data_ncst.append(trace)

for idx, model in enumerate(ncst.drop(labels='GDP Nowcast', axis=1)):
    trace = go.Bar(
            x = ncst_period,
            y = ncst[model],
            name = model,
            marker = {'color': colors_ncst[categ.index(model)]}
            )            
    data_ncst.append(trace)
          
          
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

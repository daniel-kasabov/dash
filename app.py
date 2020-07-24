import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

# ---------------------------- Set up raw data ---------------------------
# ========================================================================
# 1. F O R  G D P   F O R E C A S T   G R A P H


    # historical data
#hist = pd.read_excel('history.xlsx', index_col=None, header=0)
hist = pd.read_csv('history.csv', index_col=None, header=0)
hist.dropna(subset=['datetime', 'GDP'], inplace = True)
hist['datetime'] = pd.to_datetime(hist.datetime, format='%d/%m/%Y')

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

#ncst = pd.read_excel('nowcast.xlsx', index_col=0, header=0)
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
          
          
########### Initiate the app


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = 'Forecasts'
server = app.server


######### Set up the layout 

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
    [
        html.Div(
                [
                 html.Div(
                     [
                             html.Img(
                             src=app.get_asset_url("BNB-logo2.png"),
                             className="BNB-logo",
                             style={'padding': '0px','height': '60%','width': '60%','margin': '0px 80px'}
                                          )
                     ]
                        ), 
                 dcc.Markdown(
                         """### Compare Macro Forecasts""".replace("  ", ""),              
                         className="title"),                                                            
                 dcc.Markdown(
                         """This interactive report icludes state-of-the art forecasting models employed by the  
                         [Research team @BNB](http://www.bnb.bg/ResearchAndPublications/PubResearch/PubRForecasting/index.htm):
                             * **ARMA(p,q) model**
                             * **Dynamic Factor Models (DFM)**
                             * **Mixed-data sampling (MIDAS)**
                             * **State Space Model**
                             * **Unobserved Components Model (UCM)** 
                             * **Bayesian Vector Autoregression Model (BVAR)** """.replace("  ", ""),
                         className="subtitle"),
                    ]
                ), 
        html.Hr(),
        dbc.Nav( # see https://dash-bootstrap-components.opensource.faculty.ai/
            [
                dbc.NavLink("GDP", href="/page-gdp", id="page-gdp-link"),
                dbc.NavLink("Inflation", href="/page-inflation", id="page-inflation-link"),
                dbc.NavLink("Methodology", href="/page-methodology", id="page-methodology-link"),
            ],
            vertical=True,
            pills=True,
            
        ),
#        html.Div(
#            [
#                 html.A(
#                        html.Button("Learn More", className="learn-more-button"),
#                        href="/page-methodology",
#                        target="_blank",
#                       )
#            ],
#                 className="info-button",
#        ), 
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])



# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in {'gdp','inflation','methodology'}],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in {'gdp','inflation','methodology'}]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-gdp"]:
        return  html.Div([
                    html.H1(children='GDP forecast using various econometric models',style={'margin-top':'0px', 'text-align':'center'}),
                    html.Div([
                            html.P([
                                    html.Label('Select model ...'),
                                    dcc.Checklist(
                                        id='models-options',
                                        options=[{'label': i, 'value':i} for i in available_models],
                                        value=list(fct['Model'].unique()),
                                        labelStyle={'display': 'inline-block', 'margin': '3px'}
                                        )],
                                style={'width': '250px', 'margin-right': 'auto', 'margin-left': 'auto', 'text-align': 'center', 'padding': '-20px 0px 0px 0px'}
                                    )],
                            className='input-wrapper'),
                    dcc.Graph(id="forecast-graph", 
                              #style={"margin": "20px 20px", "height": "45vh",'width': '75%'},
                              style={'width': '85%', 'height': '60vh', 'margin-right': 'auto', 'margin-left': 'auto'},
                              config={
                                      'modeBarButtonsToRemove': ['autoScale2d', 'select2d', 'zoom2d',
                                                                 'pan2d', 'toggleSpikelines',
                                                                 'hoverCompareCartesian',   
                                                                 'zoomOut2d', 'zoomIn2d',
                                                                 'hoverClosestCartesian',
                                                                 # 'sendDataToCloud',
                                                                 'resetScale2d']}
                                ),
                    html.P([
                            html.Label('Select year ...'),
                            dcc.RangeSlider(
                                    id = 'year-slider',
                                    min = hist['datetime'].dt.year.min(),
                                    #max = fct_period.year.max(),
                                    max = hist['datetime'].dt.year.max(),        
                                    value = [2010, fct_period.year.max()],
                                    marks = {str(year): str(year) for year in range(hist['datetime'].dt.year.min(), hist['datetime'].dt.year.max(),2)}                                   ), 
                                    ],
                            style={'width': '70%', 'margin-right': 'auto', 'margin-left': 'auto', 'padding': '0px 0px 10px 10px'}),
                    html.H1(children='GDP nowcast for Q2 2020',style={'margin-top':'20px', 'text-align':'center'}),    
                    dcc.Graph(id='nowcast-graph',
                              style={'width': '85%', 'height': '60vh', 'margin-right': 'auto', 'margin-left': 'auto'},
                              figure={
                                      "data": data_ncst,
                                      "layout": go.Layout(
                                              barmode="relative",
                                              #title = 'GDP nowcast (qoq, %)',
                                              #legend = {'orientation': 'h', "x": 0.5, 'xanchor': 'center'},
                                              #height = 400,
                                              margin = {'l': 50,'r': 50,'t': 40},
                                              hovermode = 'closest',                                              
                                              xaxis = {'tickangle': -90,
                                                      'showgrid': True,
                                                          #'title': 'Time'
                                                      },
                                              yaxis = {'title': '(qoq, %)',
                                                       'showgrid': True,
                                                       #'range': [-1, 3]
                                                       },         
                                            # font = {
                                                    #"family": "Roboto",
                                                    # "size": 14
                                                    # }
                                                        )
                                      }
                              ),
                     dcc.Markdown(''' 
                                   Notes:                                                     
                                      - The nowcast stands at -3.8% (qoq) for 2020:Q2.                                 
                                      - News from mid-May data releases pointed to a decline of around -6.4% (qoq), driven by negative news from surveys, labour market and turnover statistics.                                             
                                  ''')                 
                                      
  
            ],
            id="page",
            className="ten columns",
        )
    elif pathname == "/page-inflation":
        return html.P("This is the content of page Inflation. Yay!")
    elif pathname == "/page-methodology":
        return html.P("Oh cool, this is page Methodology!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )
    
    
@app.callback(
    dash.dependencies.Output('forecast-graph', 'figure'),
    [dash.dependencies.Input('models-options', 'value'),
     dash.dependencies.Input('year-slider', 'value')])


def update_graph(selected_models, year_value):

    # data for the graph
    data = []
    trace = {
            'x': hist.loc[(hist['datetime'].dt.year >= year_value[0]) & (hist['datetime'].dt.year <= year_value[1]), 'datetime'],
            'y': hist.loc[(hist['datetime'].dt.year >= year_value[0]) & (hist['datetime'].dt.year <= year_value[1]), 'GDP'],
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': 'Historical data',
            'line': {'color': 'rgb(33, 33, 33)'}
            }
    data.append(trace)

    for idx, model in enumerate(selected_models):
        trace = {
                'x': fct_period,
                #'y': fct.loc[(fct['Model'] == model) & (fct['name'] == 'Baseline'),'Q1':'Q4'].mean(),
                'y': hist['GDP'].tail(1).append(fct.loc[(fct['Model'] == model) & (fct['name'] == 'Baseline'),'Q1':'Q4'].mean()),
                'showlegend': False,
                'type': 'scatter',
                'mode': 'lines+markers',
                'name': model,
                'line': {'color': colors[idx]}
                }
        data.append(trace)

    # for idx, band in enumerate(models list):
    for idx, model in enumerate(selected_models):
        trace = {
                'x': fct_period,
                #'y': fct.loc[(fct['Model'] == model) & (fct['name'] == 'Low'),'Q1':'Q4'].min(),
                'y': hist['GDP'].tail(1).append(fct.loc[(fct['Model'] == model) & (fct['name'] == 'Low'),'Q1':'Q4'].min()),
                'showlegend': False,
                'type': 'scatter',
                'mode': 'lines',
                'name': 'min {}'.format(model),
                'line': {'color': colors[idx],
                         'width': 0.5},
                         }
        data.append(trace)

        trace = {
                'x': fct_period,
                #'y': fct.loc[(fct['Model'] == model) & (fct['name'] == 'High'),'Q1':'Q4'].max(),
                'y': hist['GDP'].tail(1).append(fct.loc[(fct['Model'] == model) & (fct['name'] == 'High'),'Q1':'Q4'].max()),
                'type': 'scatter',
                'fill': 'tonexty',
                'mode': 'lines',
                'name': model,
                'line': {'color': colors[idx],
                         'width': 0.5}
                }
        data.append(trace)  

    return {
        'data': data,
        'layout': {
            #'title': 'Observed & Projected GDP Growth (qoq, %)',    
            'legend': {
                'orientation': 'h',
                "x": 0.5,
                'xanchor': 'center'
            },
#            'height': 400,
            'margin': {
                'l': 50,
                'r': 50,
                't': 40
            },
            'hovermode': 'closest',
            'yaxis': {
                'title': '(qoq, %)',
                'showgrid': True,
                'range': [-5, 4]
#                'range': [hist.loc[(hist['datetime'].dt.year >= year_value[0]), 'GDP'].min()-2, hist.loc[(hist['datetime'].dt.year >= year_value[0]), 'GDP'].max()+2]
            },
            'xaxis': {
                'showgrid': True,
            #    'rangeslider': {'visible':True}
            #    'title': 'Time'
            },
            # "font": {
            #     "family": "Roboto",
            #     "size": 14
            # }
        }
    }

# Make annotations
@app.callback(Output("text", "children"), [Input("slider", "value")])
def make_text(value):
    if value is None:
        value = 0
 


if __name__ == "__main__":
    app.run_server()

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go


# ======================================== G D P   F O R E C A S T   G R A P H ==============================
# historical data
hist = pd.read_excel('history.xlsx', index_col=None, header=0)

# forecast data
fct = pd.read_excel('forecast.xlsx', index_col=None, header=0)

# available models
available_models = list(fct['Model'].unique())

# dates with available forecast periods
# fct_period = pd.period_range(hist['datetime'].iloc[-1], freq='Q', periods=5)
fct_period = pd.period_range(hist['datetime'].iloc[-2], freq='Q', periods=6)


fct_period = fct_period[1:].asfreq('M', how='E')
fct_period = fct_period.to_timestamp()

# Colors from tab10 palette
colors = ['#d62728', '#ff7f0e', '#1f77b4'][::-1] 

# ====================================== G D P   N O W C A S T   G R A P H ==================================

#colors_ncst = ['#37AB65', '#3DF735', '#AD6D70', '#EC2504', '#8C0B90', '#C0E4FF', '#27B502', '#7C60A8', '#CF95D7', '#145JKH']          
colors_ncst = ['red', 'turquoise', 'gold', 'lime', 'deeppink','mediumblue', 'blanchedalmond', 'lightslategray', 'darkseagreen', 'olive', 'purple']          

ncst = pd.read_excel('nowcast.xlsx', index_col=0, header=0)
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

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


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




if __name__ == "__main__":
    app.run_server()

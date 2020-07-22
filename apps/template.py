import dash_html_components as html  
import dash_core_components as dcc    


def template(template_name: str, dropdown_menu):
    return html.Div([
        html.H2('An Example Dash App xxx', 
                    style={"display": "inline",
                        'font-size': '3.65em',
                        'margin-left': '7px',
                        'font-weight': 'bolder',
                        'font-family': 'Product Sans',
                        'color': "rgba(117, 117, 117, 0.95)",
                        'margin-top': '20px',
                        'margin-bottom': '0',
                            }),
                    html.Img(src="https://avatars2.githubusercontent.com/u/20743732",
                    style={
                        'height': '100px',
                        'float': 'right',
                        'margin-bottom': '10px',
                    }),
        dropdown_menu,
        html.Div(id='graphs-' + template_name)   
    ], className='container')

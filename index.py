import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import vgames, global_sales, solar

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "19rem",
    "padding": "2rem 1rem",
    "background-color": "#222222",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H3("BankEnergi",style={'fontSize': 25, 'textAlign': 'center', 'color' : '#ffffff'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Carbon Intensity", href="/apps/vgames", active="exact"),
                dbc.NavLink("Elexon Flex Market", href="/apps/global_sales", active="exact"),
                dbc.NavLink("Solar Production", href="/apps/solar", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("Welcome to BankEnergi Data Board!", style={'textAlign': 'center'})
    elif pathname == "/apps/vgames":
        return vgames.layout
    elif pathname == "/apps/global_sales":
        return global_sales.layout
    elif pathname == "/apps/solar":
        return solar.layout    
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == '__main__':
    app.run_server(debug=False)

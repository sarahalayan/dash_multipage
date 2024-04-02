

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

def styled_offcanvas_component(children):
    return dbc.Offcanvas(
        children=children,
        id="offcanvas-sidebar",
        title="Menu",
        is_open=False,
        style={
            "width": "180px",
            "background-color": "#f0f0f0",
            "border-right": "1px solid #ddd",
        },
    )

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
            style={
                "padding": "10px",
                "text-decoration": "none",
                "color": "#333",
                "font-weight": "bold",
                "transition": "0.3s all ease-in-out",
                ":hover": {
                    "background-color": "#eee",
                },
            },
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    className="flex-column",
)


app.layout = html.Div(
    [
        styled_offcanvas_component(sidebar),
        
        dbc.Container(
            fluid=True,
            children=[
                dbc.Row(
                    [
                       
                        dbc.Col(
                            children=[
                                dbc.Button("Menu", id="open-sidebar-button"),
                                dash.page_container
                            ]
                        ),
                    ]
                )
            ],
        ),
    ],
    
    className="app-container",
)


@app.callback(
    Output("offcanvas-sidebar", "is_open"),
    [Input("open-sidebar-button", "n_clicks")],
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks):
    if n_clicks:
        return True
    return False



if __name__ == '__main__':
    app.run(debug=True)

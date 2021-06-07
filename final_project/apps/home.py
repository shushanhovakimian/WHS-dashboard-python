import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to the WHS dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Our Goal: Visualize global health trends and analyse the factors that it is affacted by.'), className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='Audience: Everyone who would like to be informed about public health in all over the world.')
                    , className="mb-5")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(children=[html.H3(children='Get the original datasets used in this dashboard',
                                               className="text-center"),
                                               dbc.Button("World Health Statistics 2020",
                                                  href="https://www.kaggle.com/utkarshxy/who-worldhealth-statistics-2020-complete",
                                                  color="primary",
                                                  className="mt-3"),
                                       ],
                             body=True, color="primary", outline=True)
                    , width=4, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
                                               className="text-center"),
                                       dbc.Button("GitHub",
                                                  href='https://github.com/shushanhovakimian/WHS-Dashboard-Python',
                                                  color="primary",
                                                  className="mt-3"),
                                       ],
                             body=True, color="primary", outline=True)
                    , width=4, className="mb-4")], justify="center")
 ])
    ])

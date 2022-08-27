import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pprint import pprint
import plotly.express as px
import math
import dash_daq as daq
from app import app

color_choices = {
	'light-blue': '#7FAB8',
	'light-grey': '#F7EFED',
	'light-red':  '#F1485B',
	'dark-blue':  '#33546D',
	'middle-blue': '#61D4E2'
}

colors = {
		'full-background':		color_choices['light-grey'],
		'chart-background':		color_choices['light-grey'],
		'histogram-color-1':	color_choices['dark-blue'],
		'histogram-color-2':	color_choices['light-red'],
		'block-borders':		color_choices['dark-blue']
}

# margins = {
# 		'block-margins': '10px 10px 10px 10px',
# 		'block-margins': '4px 4px 4px 4px'
# }

# Data for barplot + linechart
cancer = pd.read_csv('data/30-70cancerChdEtc.csv')
cancer.rename(columns={'First Tooltip': 'prob_dying30_70', 'Dim1': 'gender'},
              inplace=True)  # Probability of dying between the age of 30 and exact age of 70 from any of the cardiovascular disease, cancer, diabetes, or chronic respiratory disease.
cancer = cancer.drop('Indicator', axis=1)
cancer.drop(cancer[cancer['gender'] == 'Both sexes'].index, inplace=True)

years = cancer.Period.unique()
years.sort()
year_dict = {year: str(year) for year in years}

div_5_1_slider = dcc.RangeSlider(
    id='year-slider',
    min=years.min(),
    max=years.max(),
    step=1,
    # marks= {int(year): ({'label':str(year)} if year%4==0 else {'label':str(year), 'style': {'visibility': 'hidden'}})
    #    for year in years},
    value=[years.min(), years.max()]
)

div_5_1_checklist = html.Div(
    children=dcc.Checklist(
        id='summer-winter-checklist',
        options=[
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Female', 'value': 'Female'}

        ],
        value=['Male', 'Female'],
        labelStyle={'display': 'inline-block'}
    ),
    style={'width': '25%'
           }
)

div_5_1_toggle = html.Div(
    children=daq.ToggleSwitch(
        id='summer-winter-toggle-switch',
        value=False,
        color=color_choices['middle-blue']
    ),
    style={'width': '25%'
           }
)

div_5_1_radio = html.Div(
    children=dcc.RadioItems(
        id='bar-line-radioitems',
        options=[
            {'label': 'BarPlot', 'value': 'bar'},
            {'label': 'LinePlot', 'value': 'line'}
        ],
        value='line',
        labelStyle={'display': 'inline-block'}
    )
)

div_5_1_filters = html.Div(children=[div_5_1_checklist,
                                     div_5_1_toggle,
                                     div_5_1_radio],
                           style={
                               'display': 'flex',
                               'flex-flaw': 'row-wrap'
                           }
                           )

div_5_1_graph = dcc.Graph(
    id='probability-of-dying-30-70'
)

div_6_1_radio = html.Div(
    children=dcc.RadioItems(
        id='hover-click-radio',
        options=[
            {'label': 'Hover', 'value': 'hover'},
            {'label': 'Click', 'value': 'click'}
        ],
        value='hover',
        labelStyle={'display': 'inline-block'}
    )
)

div_6_1_graph = dcc.Graph(
    id='country-breakdown-chart'
)

div_row5 = html.Div(children =  [div_5_1_slider,
                div_5_1_filters,
                div_5_1_graph
                ],
          # style ={
          #     'border': '3px {} solid'.format(colors['block-borders']),
          #     'margin': margins['block-margins'],
          #     # 'display': 'flex',
          #     # 'flex-flaw': 'row-wrap'
          #     }
                    )

div_row6 = html.Div(children =  [div_6_1_radio,
                div_6_1_graph
                ],
          # style ={
          #     'border': '3px {} solid'.format(colors['block-borders']),
          #     'margin': margins['block-margins'],
          #     # 'display': 'flex',
          #     # 'flex-flaw': 'row-wrap'
          #     }
                    )

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Non Communicable Diseases'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Probability of dying between the age of 30 and exact age of 70 from any of the cardiovascular disease, cancer, diabetes, or chronic respiratory disease.',
                                 className="text-center text-light bg-primary"), body=True, color="primary")
        , className="mt-4 mb-4")
        ]),
            dbc.Row([
                dbc.Col(div_row5)
            ]),
            dbc.Row([
                dbc.Col(div_row6)
            ])
            ])
        ])


@app.callback(
    Output(component_id='probability-of-dying-30-70', component_property='figure'),
    [Input(component_id='year-slider', component_property='value'),
     Input(component_id='summer-winter-checklist', component_property='value'),
     Input(component_id='summer-winter-toggle-switch', component_property='value'),
     Input(component_id='bar-line-radioitems', component_property='value')
     ]
)
def update_participants_historical_chart(year_range, season_list, toggle_value, chart_type):
    if chart_type == 'line':
        traces = []
        if toggle_value == False:
            df = cancer[(cancer.Period >= year_range[0]) & (cancer.Period <= year_range[1])]
            df = df[df.gender.isin(season_list)]
            df = df.groupby(by='Period').mean().prob_dying30_70
            traces.append(go.Scatter(x=df.index, y=df.values))
        else:
            for season in season_list:
                df = cancer[(cancer.Period >= year_range[0]) & (cancer.Period <= year_range[1])]
                df = df[df.gender == season]
                df = df.groupby(by='Period').mean().prob_dying30_70
                traces.append(go.Scatter(x=df.index, y=df.values))
    else:
        traces = []
        if toggle_value == False:
            df = cancer[(cancer.Period >= year_range[0]) & (cancer.Period <= year_range[1])]
            df = df[df.gender.isin(season_list)]
            df = df.groupby(by='Period').mean().prob_dying30_70
            traces.append(go.Bar(x=df.index, y=df.values))
        else:
            for season in season_list:
                df = cancer[(cancer.Period >= year_range[0]) & (cancer.Period <= year_range[1])]
                df = df[df.gender == season]
                df = df.groupby(by='Period').mean().prob_dying30_70
                traces.append(go.Bar(x=df.index, y=df.values))

    return {
        'data': traces,
        'layout': dict(
            barmode='stack',
            xaxis={'title': 'Year',
                   'showgrid': False
                   },
            yaxis={
                'showgrid': False,
                'showticklabels': True
                },
            # autosize=False,
            # paper_bgcolor=colors['chart-background'],
            # plot_bgcolor=colors['chart-background'],
            # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            # legend={'x': 0, 'y': 1},
            # title='Probability of dying between the age of 30 and exact age of 70 from any of the cardiovascular disease, cancer, diabetes, or chronic respiratory disease.',
            height=550
        )
    }


@app.callback(
    Output(component_id='country-breakdown-chart', component_property='figure'),
    [
        Input(component_id='hover-click-radio', component_property='value'),
        Input(component_id='probability-of-dying-30-70', component_property='hoverData'),
        Input(component_id='probability-of-dying-30-70', component_property='clickData')
    ]
)
def update_country_breakdown_chart(chain_option, hoverinfo, clickinfo):
    if chain_option == 'hover':
        if hoverinfo is None:
            year = 2016
        else:
            year = hoverinfo['points'][0]['x']
    else:
        if clickinfo is None:
            year = 2016
        else:
            year = clickinfo['points'][0]['x']

    df = cancer[cancer.Period == year]
    df = df.groupby(by='Location').mean().prob_dying30_70
    df = df.nlargest(20)
    df = df.sort_values(ascending=True)

    traces = []

    traces.append(go.Bar(x=df.values, y=df.index, orientation='h')
                  )

    return {
        'data': traces,
        'layout': dict(
            barmode='stack',
            xaxis={'title': 'Year',
                   'showgrid': False
                   },
            yaxis={
                # 'title': 'Probability of dying between the age of 30 and exact age of 70 from any of the cardiovascular disease, cancer, diabetes, or chronic respiratory disease.',
                'showgrid': False,
                'showticklabels': True
                },
            # autosize=False,
            # paper_bgcolor=colors['chart-background'],
            # plot_bgcolor=colors['chart-background'],
            # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            # legend={'x': 0, 'y': 1},
            # title='Probability of dying between the age of 30 and exact age of 70 from any of the cardiovascular disease, cancer, diabetes, or chronic respiratory disease.',
            height=700
        )
    }


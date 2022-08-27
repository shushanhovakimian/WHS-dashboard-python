import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go

from app import app

import math

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

margins = {
		'block-margins': '10px 10px 10px 10px',
		'block-margins': '4px 4px 4px 4px'
}

#Data for line chart communicable diseases

hiv = pd.read_csv('data/newHivInfections.csv')
tuber = pd.read_csv('data/incedenceOfTuberculosis.csv')
malaria = pd.read_csv('data/incedenceOfMalaria.csv')
regions=pd.read_csv('data/countryInfo.csv')
hiv = hiv.drop('Indicator', axis = 1)
hiv.rename(columns={'Location':'country','Period':'year', 'Dim1':'Gender', 'First Tooltip':'new_hiv_inf', }, inplace=True)
tuber = tuber.drop('Indicator', axis = 1)
tuber.rename(columns={'Location':'country','Period':'year','First Tooltip':'tb_incidence', }, inplace=True)
malaria = malaria.drop('Indicator', axis = 1)
malaria.rename(columns={'Location':'country','Period':'year','First Tooltip':'malaria_incidence'}, inplace=True)
hiv['new_hiv_inf'] = hiv['new_hiv_inf'].apply(lambda x: x.split(' [')[0])
tuber['tb_incidence'] = tuber['tb_incidence'].apply(lambda x: x.split(' [')[0])
# Join Datasets
joined_df = pd.merge(hiv,tuber,on = ['country', 'year'],how="inner")
joined_df = pd.merge(joined_df, malaria,  on = ['country', 'year'],how="inner")
joined_df= pd.merge(joined_df,regions,on=['country'],how='inner')
# Remove Spaces
joined_df['new_hiv_inf'] = joined_df['new_hiv_inf'].str.strip()
joined_df=joined_df.drop(joined_df[joined_df['new_hiv_inf']=='<0.01'].index)
joined_df=joined_df.drop(joined_df[joined_df['new_hiv_inf']=='No data'].index)
# Change Types
joined_df['new_hiv_inf'] = joined_df['new_hiv_inf'].astype(float)
joined_df['tb_incidence'] = joined_df['tb_incidence'].astype(float)
# Dataframe to use for lineplot
dis_tend =  joined_df.groupby(['region','year']).mean().reset_index('region')[['new_hiv_inf', 'region']]

dis_tend =  joined_df.groupby(['region','year']).mean().reset_index('region')[['new_hiv_inf','tb_incidence', 'malaria_incidence', 'region']]

div_3_1_button = dcc.Checklist(
                            id = 'checklist_regions_function',
                            options=[
                                {'label': 'East Mediterranean', 'value': 'East Mediterranean'},
                                {'label': 'Europe', 'value': 'Europe'},
                                {'label': 'Africa', 'value': 'Africa'},
                                {'label': 'Americas', 'value': 'Americas'},
                                {'label': 'West Pacific', 'value': 'West Pacific'},
                                {'label': 'SE Asia', 'value': 'SE Asia'}
                            ],
                            labelStyle={'display': 'inline-block'},
                value=['Europe']
            )
div_3_1_a_graph = dcc.Graph(
                        id = 'reg_malaria_function',
                        style={'display': 'inline-block'}
            )
div_3_1_b_graph = dcc.Graph(
                        id = 'reg_tub_function',
                        style={'display': 'inline-block'}
            )
div_3_1_c_graph = dcc.Graph(
                        id = 'reg_hiv_function',
                        style={'display': 'inline-block'}
            )



div_3_1 = html.Div(children = [div_3_1_button, div_3_1_a_graph,div_3_1_b_graph,div_3_1_c_graph],
                    style = {
                            #'border': '1px {} solid'.format(colors['block-borders']),
                            'margin': margins['block-margins'],
                            'width': '100%',
                            #'height': sizes['subblock-heights'],
                    }
                )


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Communicable Diseases'), className="mb-2")
        ]),
                html.Div(children = [div_3_1])

            ])
        ])


@app.callback(
     Output('reg_malaria_function', 'figure'),
    [Input('checklist_regions_function', 'value')]
)
def update_graph(region_list):
    traces = []
    if region_list:
        for region in region_list:
            traces.append(go.Scatter(x = dis_tend[dis_tend['region']==region].index,
                y = dis_tend[dis_tend['region'] == region]['malaria_incidence'],
                                        opacity=0.6,
                                        name = region,
                                       # marker = dict(color=drug_colors[region])
                                     # marker_color='lightslategrey'
                            )
                        )
    return {
        'data': traces,
        'layout': dict(
            title='Malaria incidence (per 1 000 population at risk)',
            xaxis={'title': ' ',
                    },
            yaxis={'title': 'Malaria incidence (per 1 000 population at risk)',
                    #'range': [merged_df['Metastatic Sites'].min(), merged_df['Metastatic Sites'].max()],
                    'showgrid': False
                    },
            boxmode = 'group',
            autosize=False,
            # paper_bgcolor = colors['chart-background'],
            # plot_bgcolor = colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
            # legend={'x': 0.99, 'y': 1},
             height=400
        )
        }


@app.callback(
     Output('reg_tub_function', 'figure'),
    [Input('checklist_regions_function', 'value')]
)
def update_graph(region_list):
    traces = []
    if region_list:
        for region in region_list:
            traces.append(go.Scatter(x = dis_tend[dis_tend['region']==region].index,
                y = dis_tend[dis_tend['region'] == region]['tb_incidence'],
                                        opacity=0.6,
                                        name = region,
                                        # marker_color='#9FC5E8'
                            )
                        )
    return {
        'data': traces,
        'layout': dict(
            title = 'Incidence of tuberculosis (per 100 000 population per year)',
            xaxis={'title': ' ',
                    },
            yaxis={'title': 'Incidence of tuberculosis ',
                    #'range': [merged_df['Metastatic Sites'].min(), merged_df['Metastatic Sites'].max()],
                    'showgrid': False
                    },
            boxmode = 'group',
             autosize=False,
            # paper_bgcolor = colors['chart-background'],
            # plot_bgcolor = colors['chart-background'],
             margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
            # legend={'x': 0.99,
            #         'y': 1},
            height=400
        )
    }
@app.callback(
     Output('reg_hiv_function', 'figure'),
    [Input('checklist_regions_function', 'value')]
)
def update_graph(region_list):
    traces = []
    if region_list:
        for region in region_list:
            traces.append(go.Scatter(x = dis_tend[dis_tend['region']==region].index,
                y = dis_tend[dis_tend['region'] == region]['new_hiv_inf'],
                                        opacity=0.6,
                                        name = region,
                                       # marker = dict(color=drug_colors[region])
                            )
                        )
    return {
        'data': traces,
        'layout': dict(
            title = 'New HIV infections (per 1000 uninfected population)',
            xaxis={'title': ' ',
                    },
            yaxis={'title': 'New HIV infections',
                    #'range': [merged_df['Metastatic Sites'].min(), merged_df['Metastatic Sites'].max()],
                    'showgrid': False
                    },
            boxmode = 'group',
            # autosize=False,
            # paper_bgcolor = colors['chart-background'],
            # plot_bgcolor = colors['chart-background'],
             margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
            # legend={'x': 0.99, 'y': 1},
            height=400
        )
    }

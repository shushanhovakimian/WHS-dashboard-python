import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go

from app import app

import math

#Data for map
df_lifeExpectancyAtBirth = pd.read_csv('data/lifeExpectancyAtBirth.csv')
df_lifeExpectancyAtBirth = df_lifeExpectancyAtBirth[df_lifeExpectancyAtBirth['Period'] > 1920]
df_world = df_lifeExpectancyAtBirth[df_lifeExpectancyAtBirth['Dim1'] == 'Both sexes'].sort_values(by=['Period']).reset_index()
df_world.rename(columns={'First Tooltip': 'Life Expectancy'}, inplace=True)
#fig for map
fig1 = px.choropleth(df_world,
                    locations='Location',
                    locationmode = "country names",
                    color='Life Expectancy',
                    color_continuous_scale="Viridis",
                    hover_name='Location',
                    animation_frame='Period'
                   )
fig1.update_layout(
                  title_x = 0.5,
                  geo=dict(
                  showframe = False,
                  showcoastlines = False)
                )

#Data for racing charts
df = pd.read_csv("data/medicalDoctors.csv")
df.rename(columns = {'Location' : 'country',
                     "Period": "year",
                     "First Tooltip": "Medical doctors (per 10,000)"
                     },
           inplace = True)
dict_keys=['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen',
           'fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','twentyone','twentytwo',
           'twentythree','twentyfour','twentyfive','twentysix','twentyseven']

years=[1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,
       2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016]
n_frame={}
for y, d in zip(years, dict_keys):
    dataframe=df[(df['year']==y)]
    dataframe=dataframe.nlargest(n=5,columns=['Medical doctors (per 10,000)'])
    dataframe=dataframe.sort_values(by=['year','Medical doctors (per 10,000)'])
    n_frame[d]=dataframe

# fig for racing
fig2 = go.Figure(
    data=[
        go.Bar(
        x=n_frame['one']['Medical doctors (per 10,000)'], y=n_frame['one']['country'],orientation='h',
        text=n_frame['one']['Medical doctors (per 10,000)'], texttemplate='%{text:.3s}',
        textfont={'size':18}, textposition='inside', insidetextanchor='middle',
        #width=0.9, marker={'color':n_frame['one']['color_code']}
        marker_color = '#9FC5E8'
        )
    ],
    layout=go.Layout(
        xaxis=dict(range=[0, 60], autorange=False, title=dict(text='Medical doctors (per 10,000)',font=dict(size=18))),
        yaxis=dict(range=[-0.5, 5.5], autorange=False,tickfont=dict(size=14)),
        title=dict(text='Year: 1990',font=dict(size=28),x=0.5,xanchor='center'),
        # Add button
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          # https://github.com/plotly/plotly.js/blob/master/src/plots/animation_attributes.js
                          args=[None,
                          {"frame": {"duration": 1000, "redraw": True},
                          "transition": {"duration":250,
                          "easing": "linear"}}]
            )]
        )]
    ),
    frames=[
            go.Frame(
                data=[
                        go.Bar(x=value['Medical doctors (per 10,000)'], y=value['country'],
                        orientation='h',text=value['Medical doctors (per 10,000)'],
                        marker_color = '#9FC5E8'
                        )
                    ],
                layout=go.Layout(
                        xaxis=dict(range=[0, 60], autorange=False),
                        yaxis=dict(range=[-0.5, 5.5], autorange=False,tickfont=dict(size=14)),
                        title=dict(text='Year: '+str(value['year'].values[0]),
                        font=dict(size=28))
                    )
            )
        for key, value in n_frame.items()
    ]
)
#Data for bubble chart
pop = pd.read_csv('data/population.csv')
water = pd.read_csv('data/basicDrinkingWaterServices.csv')
water = water.drop('Indicator', axis = 1)
pop = pop[pop['year'] >= 2000]
pop = pop[pop['year'] <= 2017]
water.rename(columns={'Period':'year', 'First Tooltip':'Drinking', 'Location':'country'}, inplace=True)
unified = pd.merge(pop, water, on = ['country', 'year'])
poison = pd.read_csv('data/mortalityRatePoisoning.csv')
poison = poison.drop('Indicator', axis = 1)
poison.rename(columns={'Dim1':'Gender', 'First Tooltip':'poison_mort', 'Location':'country','Period':'year'}, inplace=True)
df = pd.merge(unified, poison, on = ['country', 'year'])
info = pd.read_csv('data/countryInfo.csv')
info = info.drop(['flag', 'country_alt', 'alpha2', 'numeric'], axis=1)
df = pd.merge(df, info, on = 'country')
df_2016 = df[df['year']==2016]
df_2016 = df_2016.groupby('country').mean()
df_2016 = pd.merge(df_2016, info, on = 'country', how= 'inner')
df_2016.rename(columns={'region':'continent'}, inplace = True)

# fig for bubble

df_2016 = df_2016.sort_values(['continent', 'country'])

hover_text = []
bubble_size = []

for index, row in df_2016.iterrows():
    hover_text.append(('Country: {country}<br>'+
                      'Population: {population}').format(country=row['country'],
                                                        population=row['population']))
        #              'Life Expectancy: {poison_mort}<br>'+
       #               'GDP per capita: {Drinking}<br>'+
      #                'Population: {pop}<br>'+
       #               'Year: {year}').format(country=row['country'],
        #                                    poison_mort=row['poison_mort'],
         #                                   Drinking=row['Drinking'],
          #                                  population=row['population'],
           #                                 year=row['year']))
    bubble_size.append(math.sqrt(row['population']))

df_2016['text'] = hover_text
df_2016['size'] = bubble_size
sizeref = 2.*max(df_2016['size'])/(100**2)

# Dictionary with dataframes for each continent
continent_names = ['Africa', 'Americas', 'East Mediterranean', 'Europe', 'SE Asia','West Pacific']
continent_data = {continent:df_2016.query("continent == '%s'" %continent)
                              for continent in continent_names}

# Create figure
fig = go.Figure()

for continent_name, continent in continent_data.items():
    fig.add_trace(go.Scatter(
        x=continent['Drinking'], y=continent['poison_mort'],
        name=continent_name, text=continent['text'],
        marker_size=continent['size'],
        ))

# Tune marker appearance and layout
fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                              sizeref=sizeref, line_width=2))

fig.update_layout(

    xaxis=dict(
        title='Population using at least basic drinking-water services',
        gridcolor='white',
        type='log',
        gridwidth=2,
    ),
    yaxis=dict(
        title='Mortality rate attributed to unintentional poisoning',
        gridcolor='white',
        gridwidth=2,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
)


#Data for sunburst
df_lifeExpectancyAtBirth = pd.read_csv('data/lifeExpectancyAtBirth.csv')
df_lifeExpectancyAtBirth = df_lifeExpectancyAtBirth[df_lifeExpectancyAtBirth['Period'] > 1920]
sunburst = df_lifeExpectancyAtBirth.drop(['Indicator', 'Dim1'], axis = 1)
sunburst.rename(columns={'First Tooltip': 'Life Expectancy', 'Location':'country', 'Period':'year'}, inplace=True)
info = pd.read_csv('data/countryInfo.csv')
info = info.drop(['flag', 'country_alt', 'alpha2', 'numeric'], axis=1)
sunburst = pd.merge(sunburst, info, on = 'country')
pop = pd.read_csv('data/population.csv')
pop = pop[pop['year']>=2000]
sunburst = pd.merge(sunburst, pop, on = ['country', 'year'])
hale = pd.read_csv('data/HALElifeExpectancyAtBirth.csv')
hale = hale.drop(['Indicator', 'Dim1'], axis =1)
hale.rename(columns={'First Tooltip':'HALE', 'Location':'country', 'Period':'year'}, inplace=True)
hale = hale.groupby(['country', 'year']).mean().reset_index(['country', 'year'])
sunburst = sunburst.groupby(['country', 'year']).mean().reset_index(['country', 'year'])
sunburst = pd.merge(sunburst, hale, on = ['country','year'])
sunburst = pd.merge(sunburst, info, on = 'country')
poisoning = pd.read_csv('data/mortalityRatePoisoning.csv')
poisoning.rename(columns={'Period':'year', 'First Tooltip':'Poisoning_MR', 'Location':'country'}, inplace=True)
poisoning = poisoning.drop(['Indicator', 'Dim1'], axis = 1)
poisoning=poisoning.groupby(['country','year']).mean().reset_index(['country','year'])
sunburst = pd.merge(sunburst, poisoning, on = ['country', 'year'])



layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='WHS indicators at a glance'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Life Expectancy at Birth (years)',
                                 className="text-center text-light bg-primary"), body=True, color="primary")
        , className="mt-4 mb-4")
    ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure = fig1, id = 'map-graph'))
            ]),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Medical doctors per Country',
                                 className="text-center text-light bg-primary"), body=True, color="primary")
        , className="mt-4 mb-4")
    ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig2))
            ]),
            dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Mortality rate due to poisoning vs. Population using basic drinking-water services, 2016',
                                 className="text-center text-light bg-primary"), body=True, color="primary")
        , className="mt-4 mb-4")
    ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig))
            ]),

            dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Population per Indicator',
                                 className="text-center text-light bg-primary"), body=True, color="primary")
        , className="mt-4 mb-4")
    ]),
            dcc.Dropdown(
                id = 'dropdown-sunburst',
                options = [
                {'label':'HALE', 'value': 'HALE'},
                {'label':'Life Expectancy', 'value':'Life Expectancy'},
                {'label':'Poisoning_MR', 'value':'Poisoning_MR'}
                ],
                value = 'Life Expectancy',
                searchable=True,
                multi=False

            ),
            dbc.Row([
                dbc.Col(dcc.Graph(id = 'hale-exp-function'))
            ]),


        ])

    ])

@app.callback(
  Output('hale-exp-function', 'figure'),
  [Input('dropdown-sunburst', 'value')]
  )

def update_sunburst(column_chosen):

  fig4 = px.sunburst(sunburst, path=['region', 'country'], values='population',
                  color=column_chosen,# hover_data=['iso_alpha'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(sunburst[column_chosen], weights=sunburst['population']))

  return fig4

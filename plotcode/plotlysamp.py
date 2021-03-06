#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 17:55:44 2018

@author: shuichi
"""

# Learn about API authentication here: https://plot.ly/pandas/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
import pandas as pd

import plotly.offline as offline
offline.init_notebook_mode()

# The datasets' url. Thanks Jennifer Bryan!
url_csv = 'http://www.stat.ubc.ca/~jenny/notOcto/STAT545A/examples/gapminder/data/gapminderDataFiveYear.txt'

df = pd.read_csv(url_csv, sep='\t')
df.head()

countries = ['China', 'India', 'United States', 'Bangladesh', 'South Africa']
fill_colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854']
gf = df.groupby('country')

data = []

for country, fill_color in zip(countries[::-1], fill_colors):
    group = gf.get_group(country)
    years = group['year'].tolist()
    length = len(years)
    country_coords = [country] * length
    pop = group['pop'].tolist()
    zeros = [0] * length
    
    data.append(dict(
        type='scatter3d',
        mode='markers',
        x=years + years[::-1] + [years[0]],  # year loop: in incr. order then in decr. order then years[0]
        y=country_coords * 2 + [country_coords[0]],
        z=pop + zeros + [pop[0]],
        name='',
        surfaceaxis=1, # add a surface axis ('1' refers to axes[1] i.e. the y-axis)
        surfacecolor=fill_color,
        line=dict(
            color='black',
            width=4
        ),
    ))

layout = dict(
    title='Population from 1957 to 2007 [Gapminder]',
    showlegend=False,
    scene=dict(
        xaxis=dict(title=''),
        yaxis=dict(title=''),
        zaxis=dict(title=''),
        camera=dict(
            eye=dict(x=-1.7, y=-1.7, z=0.5)
        )
    )
)

fig = dict(data=data, layout=layout)
offline.plot(fig, filename='test.html', image_filename='test', image='jpeg')

# IPython notebook
#py.iplot(fig, validate=False, filename='filled-3d-lines')

#url = py.plot(fig, validate=False, filename='filled-3d-lines')

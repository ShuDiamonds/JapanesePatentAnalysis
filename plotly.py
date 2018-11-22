#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 20:35:53 2018

@author: shuichi
"""

import pandas as pd
import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go

import plotly.offline as offline
offline.init_notebook_mode()

import cufflinks as cf
# デフォでPlotlyのオンラインモードとなっているのでオフラインモードへと変更
# 恒久的にデフォルトをオフラインモードとする方法は下に記述
cf.go_offline()
df = pd.DataFrame(np.random.randn(10, 2), columns=["col1", "col2"])
df.iplot()


# データの指定
X = np.random.randint(0,100,100) 
Y = np.random.randint(0,100,100) 
Z = np.random.randint(0,100,100) 

trace0 = go.Histogram(x=X, xbins=dict(start=0, end=101, size=20), name = 'X')
trace1 = go.Histogram(x=Y, xbins=dict(start=0, end=101, size=20), name = 'Y')
trace2 = go.Histogram(x=Z, xbins=dict(start=0, end=101, size=20), name = 'Z')


# レイアウトの指定
layout = go.Layout(
    xaxis = dict(title="value", dtick = 20),
    yaxis = dict(title="count"),
    bargap = 0.2,
    bargroupgap = 0.1,  
    barmode = 'stack') # barmode = 'stack' で積み上げ

fig = dict(data=[trace0, trace1, trace2], layout=layout)
#offline.iplot(fig)

offline.plot(fig, filename='test.html', image_filename='test', image='jpeg')
"""
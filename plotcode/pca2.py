#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 01:10:43 2018

@author: shuichi
"""

import plotly.graph_objs as go
import plotly.offline as offline

import plotly.plotly as py
from plotly import tools

from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


if __name__ == '__main__':
    offline.init_notebook_mode()
    
    iris = datasets.load_iris()
    
    X = iris.data
    y = iris.target
    target_names = iris.target_names
    
    pca = PCA(n_components=2)
    X_r = pca.fit(X).transform(X)
    
    
    
    colors = ['navy', 'turquoise', 'darkorange']
    """
    fig = tools.make_subplots(rows=1, cols=2,
                          subplot_titles=('PCA of IRIS dataset',
                                          'LDA of IRIS dataset')
                         )
    """
    fig=go.Figure()
    for color, i, target_name in zip(colors, [0, 1, 2], target_names):
        pca = go.Scatter(x=X_r[y == i, 0], 
                         y=X_r[y == i, 1], 
                         mode='markers',
                         marker=dict(color=color),
                         name=target_name
                        )
        
        fig.append_trace(pca, 1, 1)
    
        
    for i in map(str, range(1, 3)):
        x = 'xaxis' + i
        y = 'yaxis' + i
        
        fig['layout'][x].update(zeroline=False, showgrid=False)
        fig['layout'][y].update(zeroline=False, showgrid=False)
        
    #fig = go.Figure(data=[trace], layout=layout)
    offline.plot(fig, filename='./pca.html', image_filename='test', image='jpeg')


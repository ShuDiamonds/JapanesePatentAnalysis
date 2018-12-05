#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 21:29:51 2018

@author: shuichi
"""
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

import plotly.graph_objs as go
import plotly.offline as offline

import numpy as np
import matplotlib.pyplot as plt

from sklearn import decomposition
from sklearn import datasets
import re

def Translate2JplatFormat(x):
    return str(x)[-14:-10]+"-"+str(x)[-10:-4]

def selectJplatpatlist_tranlated(x):
    return "".join(Jplatpatlist_tranlated[Jplatpatlist_tranlated["文献番号"].str.contains(x)]["FI_class"].values)
def f_str(x):
    #return str(x).replace('1', 'One').replace('2', 'Two').replace('3', 'Three').replace('4', 'Four')
    return pd.to_datetime(str(x).split("\n")[0], format='%Y/%m/%d')
def selectFIClass(x):
    #return str(x).replace('1', 'One').replace('2', 'Two').replace('3', 'Three').replace('4', 'Four')
    tmp=str(x).replace(' ', '').split("\n")
    resultlist=[x[0:4] for x in tmp]
    resultlist=list(set(resultlist))
    return "\n".join(resultlist)
def selectFISubclass(x):
    #return str(x).replace('1', 'One').replace('2', 'Two').replace('3', 'Three').replace('4', 'Four')
    tmp=str(x).replace(' ', '').split("\n")
    resultlist=[x[0:9] for x in tmp]
    resultlist=list(set(resultlist))
    return "\n".join(resultlist).replace(',', '')

if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    sns.set()
    FIjap=["診断機器","イメージデータ処理","商用特化型データ処理システム",
           "材料の調査","ヘルスケアインフォマティクス","電気的デジタルデータ処理",
           "特定の計算モデルに基づくコンピュータ・システム",
           "光学要素，光学系，または光学装置","酵素 微生物を含む測定 試験方法",
           "エレクトログラフィー"]
    df = pd.read_csv('Jplatpatlist_機械学習_画像_診断.csv',header=0)
    #df = pd.read_csv('Jplatpatlist.csv',header=0)
    # add 出願日 col
    df["出願日"]=0
    df["出願日"]=df["出願日\n公知日\n登録日"].map(f_str)
    df["FI_class"]=df["FI"].map(selectFIClass)
    df["FI_subclass"]=df["FI"].map(selectFISubclass)
    
    df["count"]=1
    #df1=df.set_index("出願日")
    df["month"]=df["出願日"].dt.month
    df["year"]=df["出願日"].dt.year
    ########### FI class aggregation
    tmp=df["FI_class"].value_counts()
    FIvallist=[]
    FIindexlist=[]
    for key,value in tmp.iteritems():
        names=str(key).split("\n")
        for name in names:
            FIvallist.append(value)
            FIindexlist.append(name)
    FIlist=pd.DataFrame(FIvallist,index=FIindexlist)
    FIlist=FIlist.groupby(FIlist.index).sum()
    FIlist=FIlist.sort_values(by=0,ascending=False).drop("他")
    TechElements=FIlist[:10] # select Tech element from top of 10 FI list  
    
    ############# read csv analysis
    Jplatpatlist_tranlated = pd.read_csv('./outputcsv/Jplatpatlist_tranlated.csv',header=0,index_col=0)
    pdfnames = pd.read_csv('./outputcsv/技術課題.csv',header=0,index_col=0)
    pdfnames["key2Jplatpatcsv"]=pdfnames["name"].map(Translate2JplatFormat)
    pdfnames["FI_class"]=pdfnames["key2Jplatpatcsv"].map(selectJplatpatlist_tranlated)
    pdfnames=pdfnames.fillna("")
    ############# パテントマップ
    colnamesa=pdfnames["課題分野"].value_counts().index.values
    TechElementAndObjectmatrix=pd.DataFrame()
    
    for ObjectField in pdfnames["課題分野"].value_counts().index:
        selecteddf=pdfnames[pdfnames["課題分野"].str.contains(ObjectField)]
        colnamestmp=[]
        valuestmp=[]
        for TechElement in TechElements.index:
            TC = selecteddf[selecteddf["FI_class"]==TechElement]
            colnamestmp.append(TechElement)
            valuestmp.append(len(TC))
        TechElementAndObjectmatrix[ObjectField]=pd.Series(valuestmp,index=colnamestmp)
            
    TechElementAndObjectmatrix=TechElementAndObjectmatrix.fillna(value=0)
    TechElementAndObjectmatrix.to_csv("./outputcsv/パテントマップ.csv")
    
    ############ plotly
    X = np.array([[i for i in range(TechElementAndObjectmatrix.shape[1]) ]]*TechElementAndObjectmatrix.shape[0]).flatten()
    Y = np.array([[i]*TechElementAndObjectmatrix.shape[1] for i in range(TechElementAndObjectmatrix.shape[0])]).flatten()
    #LABEL = [chr(i) for i in range(65,65+10)] # ラベル。アルファベットのリスト
    SIZE = TechElementAndObjectmatrix.values.flatten()*10            # サイズのデータ
    
    trace = go.Scatter(x = X, y = Y,mode='markers+text', #text =LABEL, textposition='top',
                      marker = dict(size = SIZE)) # マーカーサイズ
    
    layout = go.Layout(
            autosize=False,
            width=1500,
            height=1000,
            margin=go.layout.Margin(
            l=350,
            r=350,
            b=100,
            t=100,
            pad=4
            ),
        xaxis = dict(
            ticktext = TechElementAndObjectmatrix.columns.values,
            tickvals = np.arange(TechElementAndObjectmatrix.shape[1])  ),
        yaxis = dict(
            #ticktext = TechElementAndObjectmatrix.index.values, # FI code version
            ticktext = FIjap,
            tickvals = np.arange(TechElementAndObjectmatrix.shape[0])  ),
        font = dict(size = 15)) 
    
    fig = dict(data = [trace], layout = layout)
    offline.plot(fig, filename='./bubblechart.html', image_filename='test', image='jpeg')
    
    
    
    
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )
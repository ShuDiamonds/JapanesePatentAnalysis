#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:02:11 2018

@author: shuichi
"""

import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import matplotlib


def not_exist_mkdir( output_path ):
    if( not os.path.exists(output_path) ):
        os.mkdir( output_path )
        
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

def selectFIClassfromdatabase(x):
    #return str(x).replace('1', 'One').replace('2', 'Two').replace('3', 'Three').replace('4', 'Four')
    tmp=str(x).split("\n")
    resultlist=[str(dfs[dfs.index==x]["タイトル"].values) for x in tmp if x!=u"他"]
    return "\n".join(resultlist)


if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    sns.set()
    
    not_exist_mkdir("./outputcsv")
    # dataframe clean up
    df = pd.read_csv('Jplatpatlist_機械学習_画像_診断.csv',header=0)
    #df = pd.read_csv('Jplatpatlist.csv',header=0)
    # add 出願日 col
    df["出願日"]=0
    df["出願日"]=df["出願日\n公知日\n登録日"].map(f_str)
    
    df["count"]=1
    #df1=df.set_index("出願日")
    df["month"]=df["出願日"].dt.month
    df["year"]=df["出願日"].dt.year
    
    
    ############## select FI   
    dfs = pd.read_csv("./FI/FIlist.csv",header=0,index_col=0)
    #tmp=df["FI"][10].replace(' ', '').split("\n")
    df["FI_class"]=df["FI"].map(selectFIClass)
    df["FI_subclass"]=df["FI"].map(selectFISubclass)
    df["FI_classJP"]=df["FI_class"].map(selectFIClassfromdatabase)
    df["FI_subclassJP"]=df["FI_subclass"].map(selectFIClassfromdatabase)
    
    df.to_csv("./outputcsv/Jplatpatlist_tranlated.csv")
    
    ############## print summary
    print(df["出願人"].value_counts())
    print(df["FI_class"].value_counts())
    print(df[df["出願人"]=="ファナック株式会社"]["FI_classJP"].value_counts())
    
    ########### Company aggregation
    Company=df["出願人"].value_counts()[:5] #top 5
    
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
    FIlist["JP"]=FIlist.index.map(selectFIClassfromdatabase)
    FIlist=FIlist.sort_values(by=0,ascending=False).drop("他")
    TechElements=FIlist[:10] # select Tech element from top of 10 FI list  
    
    ########### 出願件数推移：技術要素別
    TechElementTransition=pd.DataFrame()
    for TechElement in TechElements.index:
        selecteddf=df[df["FI_class"].str.contains(TechElement)]
        grouped = selecteddf.groupby(["year"])
        
        TechElementTransition[TechElement]=grouped["count"].sum()
    TechElementTransition=TechElementTransition.fillna(value=0)
    TechElementTransition.to_csv("./outputcsv/出願件数推移：技術要素別.csv")
    ########### 主要出願企業
    from matplotlib import pylab as plt
    # matplotlibのデフォルトフォントをTakaoGothicに設定
    font = {'family' : 'TakaoGothic'}
    matplotlib.rc('font', **font)
    plt.figure(figsize = (15,7))
    Company.plot(kind="barh")    
    #plt.savefig("./submissions2/主要出願企業-hist.png", dpi=400)
    plt.show()
    plt.close('all')
    Company.to_csv("./outputcsv/主要出願企業.csv")
    ########### 出願件数推移：主要出願企業
    CompanyHistgrams=pd.DataFrame()
    for Compa in Company.index:
        grouped = df[df["出願人"]==Compa].groupby(["year"])
        CompanyHistgrams[Compa]=grouped["count"].sum()
    
    plt.figure(figsize = (25,7))
    CompanyHistgrams.plot(kind="bar")
    plt.savefig("./submissions2/出願件数推移：主要出願企業-hist.png", dpi=400)
    plt.show()
    plt.close('all')
    grouped["count"].sum().to_csv("./outputcsv/出願件数推移：主要出願企業.csv")
    ########### 技術区分構造：主要出願企業
    TechStructuresByCompany=pd.DataFrame()
    for TechElement in TechElements.index:
        selecteddf=df[df["FI_class"].str.contains(TechElement)]
        colnamestmp=[]
        valuestmp=[]
        for Compa in Company.index:
            TC = selecteddf[selecteddf["出願人"]==Compa]
            colnamestmp.append(Compa)
            valuestmp.append(len(TC))
        TechStructuresByCompany[TechElement]=pd.Series(valuestmp,index=colnamestmp)
    
    TechStructuresByCompany=TechStructuresByCompany.apply(lambda r: r/r.sum())
    TechStructuresByCompany=TechStructuresByCompany.fillna(value=0)
    
    TechStructuresByCompany=TechStructuresByCompany.T
    plt.figure(figsize = (25,7))
    TechStructuresByCompany.plot(kind="bar",stacked=True)
    plt.savefig("./submissions2/出願件数推移：主要出願企業-hist.png", dpi=400)
    plt.show()
    plt.close('all')
    TechStructuresByCompany.to_csv("./outputcsv/技術区分構造：主要出願企業.csv")
    
    ########### 出願件数推移
    selecteddf=df[df["FI_subclassJP"].str.contains('センサ')]
    #grouped = df[df["出願人"]=="ソニー株式会社"].groupby(["year",'month'])
    grouped = df.groupby(["year"])
    
    plt.figure(figsize = (25,7))
    grouped["count"].sum().plot(kind="bar",color='k')
    plt.savefig("./submissions2/出願件数の推移-hist.png", dpi=400)
    plt.show()
    plt.close('all')
    grouped["count"].sum().to_csv("./outputcsv/出願件数の推移.csv")
    
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )#!/usr/bin/env python3

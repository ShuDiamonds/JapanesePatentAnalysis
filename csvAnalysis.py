#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:02:11 2018

@author: shuichi
"""

import datetime
import time
import pandas as pd

def f_str(x):
    #return str(x).replace('1', 'One').replace('2', 'Two').replace('3', 'Three').replace('4', 'Four')
    return pd.to_datetime(str(x).split("\n")[0], format='%Y/%m/%d')
def selectFIClass(x):
    #return str(x).replace('1', 'One').replace('2', 'Two').replace('3', 'Three').replace('4', 'Four')
    tmp=str(x).replace(' ', '').split("\n")
    resultlist=[]
    for x in tmp:
        resultlist.append(x[0:4])
    return "\n".join(resultlist)
def selectFISubclass(x):
    #return str(x).replace('1', 'One').replace('2', 'Two').replace('3', 'Three').replace('4', 'Four')
    tmp=str(x).replace(' ', '').split("\n")
    resultlist=[]
    for x in tmp:
        resultlist.append(x[0:9])
    return "\n".join(resultlist)

def selectFIClassfromdatabase(x):
    #return str(x).replace('1', 'One').replace('2', 'Two').replace('3', 'Three').replace('4', 'Four')
    tmp=str(x).split("\n")
    resultlist=[]
    for x in tmp:
        resultlist.append(str(dfs[dfs.index==x]["タイトル"].values))
        
    return "\n".join(resultlist)


if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    
    # dataframe clean up
    df = pd.read_csv('Jplatpatlist.csv',header=0)
    #print(df)
    # add 出願日 col
    df["出願日"]=0
    df["出願日"]=df["出願日\n公知日\n登録日"].map(f_str)
    
    df["count"]=1
    #df1=df.set_index("出願日")
    df["month"]=df["出願日"].dt.month
    df["year"]=df["出願日"].dt.year
    #df_m = df.set_index("year","month")
    #df_m.index.names = ["year","month"]
    #df_m.sum(level='month')
    
    
    
    ############## select FI
    dfs = pd.read_csv("./FI/FIlist.csv",header=0,index_col=0)
    #tmp=df["FI"][10].replace(' ', '').split("\n")
    df["FI_class"]=df["FI"].map(selectFIClass)
    df["FI_subclass"]=df["FI"].map(selectFISubclass)
    df["FI_classJP"]=df["FI_class"].map(selectFIClassfromdatabase)
    df["FI_subclassJP"]=df["FI_subclass"].map(selectFIClassfromdatabase)
    
    df.to_csv("Jplatpatlist_tranlated.csv")
    
    ############## 
    print(df["出願人"].value_counts())
    
    grouped = df.groupby(["year",'month'])
    grouped["count"].sum().plot(kind="bar")
    grouped["count"].sum().to_csv("出願件数の推移.csv")
    
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 17:21:21 2018

@author: shuichi
"""



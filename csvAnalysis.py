
import sys
import MeCab
import datetime
import time
import pandas as pd

def f_str(x):
    #return str(x).replace('1', 'One').replace('2', 'Two').replace('3', 'Three').replace('4', 'Four')
    return pd.to_datetime(str(x).split("\n")[0], format='%Y/%m/%d')

if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    

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
    
    #
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



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:02:11 2018

@author: shuichi
"""
import datetime
import time
import pandas as pd
from glob import glob
import re
import os


def f_str(x):
    return str(x).replace(' ', '')

if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    
    
    dfs=pd.DataFrame()
    file_list = glob('./FI/csv/*.csv')
    filenames=os.listdir('./FI/csv/')
    #check the output folder
    for item,filename in zip(file_list,filenames):
        df = pd.read_csv(item,header=0)
        df=df.dropna(subset=[u'記号'])
        df=df.drop(u'インデキシングフラグ', axis=1)
        df=df[df[u'記号'] != u'＜索引＞']
        df=df[df[u'記号'] != u'＜注＞']
        df["記号"]=df["記号"].map(f_str)        
        df=df.set_index(u"記号")
        dfs=pd.concat([dfs,df])
    
    dfs.to_csv("./FI/FIlist.csv")
    
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )#!/usr/bin/env python3


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 12:28:31 2018

@author: shuichi
"""

import sys
import MeCab
import datetime
import time

if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    
    #setup mecab
    m = MeCab.Tagger ("-Owakati")
    #print(m.parse ("すもももももももものうち"))
    result_list=[]
    with open("allpdf.txt", mode='r') as f:
        line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
        while line:
            line = f.readline()
            convertedtext=m.parse (line)
            result_list.append(convertedtext)
        #end while
    
    #saving
    allText = '\n'.join(result_list)
    with open("wakatigaki_allpdf.txt", mode='w') as f:
        f.write(allText)
    
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )
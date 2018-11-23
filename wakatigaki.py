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
import re


def extractNoun(text):
    # パース
    mecab = MeCab.Tagger("-u ./userdic/patentdic.dic")
    parse = mecab.parse(text)
    lines = parse.split('\n')
    items = (re.split('[\t,]', line) for line in lines)
    # 名詞をリストに格納
    return [item[0] for item in items
            if (item[0] not in ('EOS', '', 't', 'ー') and
                 item[1] == '名詞' and item[2] == '一般')]
             

if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    
    #setup mecab
    m = MeCab.Tagger ("-Owakati -u ./userdic/patentdic.dic")
    result_list=[]
    resultNoun_list=[]
    with open("./txt/all【技術分野】.txt", mode='r') as f:
        lines = f.readlines() # 1行を文字列として読み込む(改行文字も含まれる)
        temp="".join(lines)
        lines=temp.split(",\n\n\n")
        
        for line in lines:
            convertedtext=m.parse (line)
            resultNoun_list.append(" ".join(extractNoun(line)))
            result_list.append(convertedtext)
        #end while
    
    #saving
    allText = ',\n'.join(result_list)
    with open("./txt/wakatigaki_allpdf.txt", mode='w') as f:
        f.write(allText)
    # save noun ver
    allText = ',\n'.join(resultNoun_list)
    with open("./txt/wakatigakiNoun_allpdf.txt", mode='w') as f:
        f.write(allText)
    
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )
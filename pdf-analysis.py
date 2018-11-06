#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 18:29:38 2018

@author: shuichi
"""
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LTTextBox, LTTextLine, LTImage,  LTFigure
from pdfminer.converter import PDFPageAggregator

from PIL import Image
from io import StringIO
from glob import glob
import re
import os
import datetime
import time
import pandas as pd



def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    laparams.detect_vertical = True # Trueにすることで綺麗にテキストを抽出できる
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    caching = True
    pagenos=set()
    fstr = ''
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,caching=caching, check_extractable=True):
        interpreter.process_page(page)
        strings = retstr.getvalue()
        fstr = strings

    fp.close()
    device.close()
    retstr.close()
    return fstr

def filteringwords(listdata,word):
    return [x for x in listdata if x!=word]
def REfilteringwords(listdata,pattern):
    return [x for x in listdata if None == re.match(pattern,x)]
def Findwords(listdata,patterns):
    results=[]
    for pattern in patterns:
         results.extend([x for x in listdata if None != re.match(pattern,x)])
    return results
def Findwords2index(listdata,pattern):
    temp= [i for i,x in enumerate(listdata) if None != re.match(pattern,x)]
    if len(temp)==0:
        return 0
    else:   
        return  temp[0]
def not_exist_mkdir( output_path ):
    if( not os.path.exists(output_path) ):
        os.mkdir( output_path )
    
outputpath = "./output/"
if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    
    result_list = []
    PreviousLiteratures=[]
    TechField_list=[]
    BackgroundTech_list=[]
    ProblemSolve_list=[]
    
    file_list = glob('./pdf/*.pdf')
    filenames=os.listdir('./pdf/')
    #check the output folder
    not_exist_mkdir(outputpath)
    pd.DataFrame(filenames).to_csv("pdfnames.csv")
    for item,filename in zip(file_list,filenames):
        #check the output folder
        pdfoutputpath=outputpath+filename.rstrip(".pdf")
        not_exist_mkdir(pdfoutputpath)
        #pdf convert
        result_txt = convert_pdf_to_txt(item)
        
        
        ############## Cleaning the document
        #devide to sentence
        splitted=result_txt.split("\n")
        #strip the items
        splitted=[x.strip() for x in splitted]
        #filtering those words
        filterwords=[""," ","10","20","30","40","50"]
        # if the first item is like "JP 2018-147474 A 2018.9.20",
        if splitted[0].find("JP") != -1:
            filterwords.append(splitted[0])
        for filterword in filterwords:
            splitted=filteringwords(splitted,filterword)
        #merge the splitted data
        mergeddata="".join(splitted)
        #splitted=re.split('【.*】|【】', mergeddata)
        splitted=mergeddata.split("【")
        splitted=["【"+x for x in splitted]
        #Refined well!!!
        
        ############## Extract cleaning start from here
        #Refine "【図.】"
        filterpattern=[u"【図.*】",u"【選択図】"]
        for filterpattern in filterpattern:
            splitted=REfilteringwords(splitted,filterpattern)
        with open(pdfoutputpath+"/cleanedtext.txt", mode='w') as f:
            f.write("\n".join(splitted))
        
        
        result_list.append(",".join(splitted))  
        
        
        #find the purpose section
        ################## Extract "【要約】","【課題】","【解決手段】"
        temp=Findwords(splitted,["【要約】","【課題】","【解決手段】"])
        with open(pdfoutputpath+"/【要約】.txt", mode='w') as f:
            f.write("\n".join(temp))
        
        ################## Extract 【技術分野】
        tempindex=Findwords2index(splitted,"【技術分野】")
        temp=splitted[tempindex:] #skip 2rows
        Findedflag=0 #When it is found, this flag turns 1
        tagetresult=[]
        for sentence in temp:
            if None != re.match("【\d+】",sentence): #check
                Findedflag=1
                tagetresult.append(sentence)
            elif Findedflag==1 and None == re.match("【\d+】",sentence):
                break
        with open(pdfoutputpath+"/【技術分野】.txt", mode='w') as f:
            f.write("\n".join(tagetresult))
        TechField_list.append("\n".join([filename]+tagetresult))
        
        ################## Extract 【背景技術】
        tempindex=Findwords2index(splitted,"【背景技術】")
        temp=splitted[tempindex:] #skip 2rows
        Findedflag=0 #When it is found, this flag turns 1
        tagetresult=[]
        for sentence in temp:
            if None != re.match("【\d+】",sentence): #check
                Findedflag=1
                tagetresult.append(sentence)
            elif Findedflag==1 and None == re.match("【\d+】",sentence):
                break
        with open(pdfoutputpath+"/【背景技術】.txt", mode='w') as f:
            f.write("\n".join(tagetresult))
        BackgroundTech_list.append("\n".join([filename]+tagetresult))
        
        
        ################## Extract 【発明が解決しようとする課題】
        tempindex=Findwords2index(splitted,"【発明が解決しようとする課題】")
        temp=splitted[tempindex:] #skip 2rows
        Findedflag=0 #When it is found, this flag turns 1
        tagetresult=[]
        for sentence in temp:
            if None != re.match("【\d+】",sentence): #check
                Findedflag=1
                tagetresult.append(sentence)
            elif Findedflag==1 and None == re.match("【\d+】",sentence):
                break
        with open(pdfoutputpath+"/【発明が解決しようとする課題】.txt", mode='w') as f:
            f.write("\n".join(tagetresult))
        ProblemSolve_list.append("\n".join([filename]+tagetresult))
        
        
        
        
        ################## Extract 【先行技術文献】の特許
        tempindex=Findwords2index(splitted,"【先行技術文献】")
        temp=splitted[tempindex+2:] #skip 2rows
        Findedflag=0 #When it is found, this flag turns 1
        tagetresult=[]
        for sentence in temp:
            if None != re.match("【特許文献\d+】",sentence): #check
                Findedflag=1
                tagetresult.append(sentence)
            elif Findedflag==1 and None == re.match("【特許文献\d+】",sentence):
                break
        with open(pdfoutputpath+"/【先行技術文献】.txt", mode='w') as f:
            f.write("\n".join(tagetresult))
        PreviousLiteratures.append("\n".join([filename]+tagetresult))
        
        
        
        
    # write all 【技術分野】 text data
    allText = ',\n\n\n'.join(TechField_list)
    allText=allText.strip()
    with open("all【技術分野】.txt", mode='w') as f:
            f.write(allText)
    
    # write all 【背景技術】 text data
    allText = ',\n\n\n'.join(BackgroundTech_list)
    allText=allText.strip()
    with open("all【背景技術】.txt", mode='w') as f:
            f.write(allText)
    
    # write all 【発明が解決しようとする課題】 text data
    allText = ',\n\n\n'.join(ProblemSolve_list)
    allText=allText.strip()
    with open("all【発明が解決しようとする課題】.txt", mode='w') as f:
            f.write(allText)
    
    # write all 【先行技術文献】 text data
    allText = ',\n\n\n'.join(PreviousLiteratures)
    allText=allText.strip()
    with open("all【先行技術文献】.txt", mode='w') as f:
            f.write(allText)
            
    # write all pdf text data
    allText = ',\n\n\n'.join(result_list)
    allText=allText.strip()
    with open("allpdf.txt", mode='w') as f:
            f.write(allText)
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(Duration)：' + str(round(progress_i_time,1)) + "秒" )
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

file_list = glob('./pdf/*.pdf')

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
    

if __name__ == '__main__':
    result_list = []
    for item in file_list:
        result_txt = convert_pdf_to_txt(item)
        result_list.append(result_txt)
    
    
    #Cleaning the document
    result_list2=[]
    for txtdocment in result_list:
        #devide to sentence
        splitted=txtdocment.split("\n")
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
        
        #Extra cleaning start from here
        #Refine "【図.】"
        filterpattern=[u"【図.*】",u"【選択図】"]
        for filterpattern in filterpattern:
            splitted=REfilteringwords(splitted,filterpattern)
            
    
    allText = ','.join(result_list)
    allText=allText.strip()
    file = open('allpdf.txt', 'w')
    file.write(allText)
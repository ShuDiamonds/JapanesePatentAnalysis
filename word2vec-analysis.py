#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 14:57:50 2018

@author: shuichi
"""

from gensim.models import word2vec
"""
sentences = word2vec.Text8Corpus('./wakatigaki_allpdf.txt')

model = word2vec.Word2Vec(sentences, size=200, min_count=20, window=15)
model.save("./patent.model")
"""
vector = model.wv["提供"]
word = model.wv.most_similar( [ vector ], [], 20)
#print(vector)
print(word)
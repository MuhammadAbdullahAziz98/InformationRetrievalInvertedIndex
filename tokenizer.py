# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 21:17:32 2019

@author: abdullah
"""

# -*- coding: utf-8 -*-

#imports
import glob, os
import sys
from bs4 import BeautifulSoup,Comment
import re

#getting arguments:

filename = sys.argv[1]
stopwords = dict()
stopwordsFile = r"C:\Users\lenovo\Downloads\stoplist.txt"   #change  apth for stopwords list
if os.path.exists(stopwordsFile):
    swfp = open(stopwordsFile,'r')
    content = swfp.readlines()
    for x in content:
        stopwords[x.strip()] = x.strip()  
if os.path.exists(filename):
    os.chdir(filename)
    i = 0
    worddict =  dict()
    for file in glob.glob("clueweb12-0000tw-14-17002.txt"):
        #print(file)
        fp = open(file,'r',encoding=" Latin-1 ")
        #print(fp.read())
        soup = BeautifulSoup(fp, 'html.parser')
        el = soup.find('body')
        if el:
            for element in el(text=lambda text: isinstance(text, Comment)):
                element.extract()
            soup.prettify()
            for script in soup(["script", "style"]):                   
                script.decompose()
            docWords = list(el.stripped_strings)
           # print(docWords)
            wordlist = list()
            pattern = '[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+'
            for w in docWords:
                wordlist.append(re.findall(pattern,w))
            vocab = [item for sublist in wordlist for item in sublist]
            for w in stopwords:
                worddict.pop(w, None)
            for w in vocab:
                if w.lower() not in worddict and w.lower() not in stopwords:
                    worddict[w.lower()] = i
                    i = i+1

                #print(re.findall(pattern,w))
            print(worddict)            
            print("FILE ENDS HEREE!!!!!!!!!!!!!!!!!!")
else:
    print("Folder doesn't exist, try entering the complete path")

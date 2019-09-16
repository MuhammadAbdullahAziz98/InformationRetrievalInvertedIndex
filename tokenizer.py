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
from nltk.stem.porter import PorterStemmer

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
    termid = 0
    docid=  0
    worddict =  dict()
    p_stemmer = PorterStemmer()
    for file in glob.glob("*.txt"):
        #print(file)
        fp = open(file,'r',encoding=" Latin-1 ")
        fd = open(r"C:\Users\lenovo\Documents\irAssignment1\docids.txt", "a",encoding=" utf-8 ")
        fd.write(file + "\\t" + str(docid)+"\n")
        fd.close()
        docid = docid+1
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
            pattern = pattern = r'[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|\w+-\w+|\w+.\w+|\w+_\w+'
            for w in docWords:
                wordlist.append(re.findall(pattern,w))
            vocab = [item for sublist in wordlist for item in sublist]
            
            for w in vocab:
                w = w.lower()
                w = p_stemmer.stem(w)
                if w not in worddict and w not in stopwords:
                    worddict[w] = termid
                    termid = termid+1
            #print(worddict)            
            #print("FILE ENDS HEREE!!!!!!!!!!!!!!!!!!")
    f = open(r"C:\Users\lenovo\Documents\irAssignment1\termids.txt", "w",encoding=" utf-8 ")
    for w in worddict:
        f.write(w + "\\t" + str(worddict[w])+"\n")
    f.close()
    
else:
    print("Folder doesn't exist, try entering the complete path")

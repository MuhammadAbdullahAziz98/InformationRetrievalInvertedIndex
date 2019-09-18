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
from operator import itemgetter
class TokenHashmap:
    numberOfOccurences = 0
    totalNoOfDocs = 0
    docs = list()
    pos = list()

    
class TokenWithoutHashmap:
    termid = 0;
    docid = 0
    pos = 0

class Token:
    numberOfOccurences = 0
    totalNoOfDocs = 0
    docs = list()
    pos = list()
    termid = 0

def custom_sort(t):
    return t.termid
#getting arguments:

filename = sys.argv[1]
stopwords = dict()
stopwordsFile = r"C:\Users\lenovo\Downloads\stoplist.txt"   #change  path for stopwords list
if os.path.exists(stopwordsFile):
    swfp = open(stopwordsFile,'r')
    content = swfp.readlines()
    for x in content:
        stopwords[x.strip()] = x.strip()  
if os.path.exists(filename):
    os.chdir(filename)
    termid = 0
    docid=  -1
    worddict =  dict()
    wordinfoHash = dict()
    wordinfoWithoutHash = list()
    p_stemmer = PorterStemmer()
    for file in glob.glob("*.txt"):
        fp = open(file,'r',encoding='utf-8', errors='ignore')
        fd = open(r"C:\Users\lenovo\Documents\irAssignment1\docids.txt", "a",encoding=" utf-8 ")
        fd.write(file + "\\t" + str(docid)+"\n")
        fd.close()
        docid = docid+1
        soup = BeautifulSoup(fp, 'html.parser')
        el = soup.find('body')
        if el:
            for element in el(text=lambda text: isinstance(text, Comment)):
                element.extract()
            for script in soup(["script", "style"]):                   
                script.extract()
            soup.prettify()
            docWords = list(el.stripped_strings)
           # print(docWords)
            vocab = list()
            pattern = pattern = r'[A-Z]+\-[A-Z]+|[a-z]+\-[a-z]+|[A-Z]+\'[A-Z]+|[a-z]+\'[a-z]+|[A-Z][a-z]+|[a-z]+|[A-Z]+|[0-9]+'#[A-Z]+|[A-Z][a-z]+|[a-z]+|[0-9]+|\w+-\w+|\w+.\w+|\w+_\w+'
            for w in docWords:
                vocab.append(re.findall(pattern,w))
            vocab = [item for sublist in vocab for item in sublist]
            for i, w in enumerate(vocab):
                w = w.lower()
                w = p_stemmer.stem(w)
                if w not in worddict and w not in stopwords:
                    worddict[w] = termid
                    print(termid)
                    wordinfoHash[termid] = TokenHashmap()
                    wordinfoHash[termid].docs = list()
                    wordinfoHash[termid].pos = list()
                    wordinfoHash[termid].docs.append(docid)
                    wordinfoHash[termid].pos.append(i)
                    wordinfoHash[termid].numberOfOccurences = wordinfoHash[termid].numberOfOccurences+1
                    wordinfoHash[termid].totalNoOfDocs = wordinfoHash[termid].totalNoOfDocs+1    
                    #without hashmap
                    t = TokenWithoutHashmap()
                    t.docid = docid
                    t.termid = termid
                    t.pos = i
                    wordinfoWithoutHash.append(t)
                    termid = termid+1
                else:
                    ids = worddict.get(w,None)
                    if ids:
                        #print(ids)
                        wordinfoHash[ids].pos.append(i)
                        wordinfoHash[ids].docs.append(docid)
                        wordinfoHash[ids].numberOfOccurences = wordinfoHash[ids].numberOfOccurences+1
                        wordinfoHash[ids].totalNoOfDocs = wordinfoHash[ids].totalNoOfDocs+1
                        t = TokenWithoutHashmap()
                        t.docid = docid
                        t.termid = ids
                        t.pos = i
                        wordinfoWithoutHash.append(t)

    #sorting for hashmap
    idW=0                
    
    #without hashmap:
    #sort on termid:
    wordinfoWithoutHash.sort(key = custom_sort)
    #merging on same term id: 
    wordinfo = list()
    oldtid = 0
    newtid = 0
    olddocid = 0
    newdocid = 0
    t= Token()
    for w in range(0,len(wordinfoWithoutHash)):
        newtid = wordinfoWithoutHash[w].termid
        if newtid == oldtid and newtid!=0:
            t.numberOfOccurences = t.numberOfOccurences+1
            t.docs.append(wordinfoWithoutHash[w].docid)
            t.pos.append(wordinfoWithoutHash[w].pos)
            if olddocid == newdocid:
                t.totalNoOfDocs = t.totalNoOfDocs+1
            else:
                olddocid = newdocid
        else:    
            oldtid = newtid
            t = Token()
            t.termid = newtid
            t.totalNoOfDocs = t.totalNoOfDocs+1
            t.numberOfOccurences = t.numberOfOccurences+1
            t.docs = list()
            t.pos = list()
            t.docs.append(wordinfoWithoutHash[w].docid)
            t.pos.append(wordinfoWithoutHash[w].pos)
            wordinfo.append(t)
    #termids.txt
    f = open(r"C:\Users\lenovo\Documents\irAssignment1\termids.txt", "w",encoding=" utf-8 ")
    for w in worddict:
        f.write(w + "\\t" + str(worddict[w])+"\n")
    f.close()
    
    # delta encoding:
    print("ENCODING STARTS:")
    for w in wordinfoHash:
        for p in range(len(wordinfoHash[w].docs)-1,0,-1):
            wordinfoHash[w].docs[p] = wordinfoHash[w].docs[p] - wordinfoHash[w].docs[p-1]
    for w in wordinfoHash:
        for p in range(len(wordinfoHash[w].pos)-1,0,-1):
            if wordinfoHash[w].pos[p] -wordinfoHash[w].pos[p-1]>=0:
                wordinfoHash[w].pos[p] = wordinfoHash[w].pos[p] - wordinfoHash[w].pos[p-1]
    
    for w in range(0,len(wordinfo)):
        for p in range(len(wordinfo[w].docs)-1,0,-1):
            wordinfo[w].docs[p] = wordinfo[w].docs[p] - wordinfo[w].docs[p-1]
    for w in range(0,len(wordinfo)):
        for p in range(len(wordinfo[w].docs)-1,0,-1):
            if wordinfo[w].pos[p] -wordinfo[w].pos[p-1]>=0:
                wordinfo[w].pos[p] = wordinfo[w].pos[p] - wordinfo[w].pos[p-1]
    
    #inverted index with hashmap 
    f = open(r"C:\Users\lenovo\Documents\irAssignment1\termindex_hashmap.txt", "w",encoding=" utf-8 ")
    for w in wordinfoHash:
        f.write(str(w) + " " + str(wordinfoHash[w].numberOfOccurences) +" "+str(wordinfoHash[w].totalNoOfDocs) +" ")
        for p in range(0,len(wordinfoHash[w].pos)):
            f.write(str(wordinfoHash[w].docs[p]) +","+str(wordinfoHash[w].pos[p]) + " ")
        f.write("\n")            
    f.close()
    #inverted index without hashmap 
    f = open(r"C:\Users\lenovo\Documents\irAssignment1\termindex_withouthashmap.txt", "w",encoding=" utf-8 ")
    for w in range(0,len(wordinfo)):
        f.write(str(wordinfo[w].termid) + " " + str(wordinfo[w].numberOfOccurences) +" "+str(wordinfo[w].totalNoOfDocs) +" ")
        for p in range(0,len(wordinfo[w].pos)):
            f.write(str(wordinfo[w].docs[p]) +","+str(wordinfo[w].pos[p]) + " ")
        f.write("\n")            
    
    f.close()
    
else:
    print("Folder doesn't exist, try entering the complete path")


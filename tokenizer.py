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
    numberOfOccurences = 0
    totalNoOfDocs = 0
    docs = list()
    pos = list()

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
    docid=  -1
    worddict =  dict()
    wordinfoHash = dict()
    wordinfoWithoutHash = list()
    p_stemmer = PorterStemmer()
    for file in glob.glob("*.txt"):
        fp = open(file,'r',encoding=" Latin-1 ")
        fd = open(r"C:\Users\lenovo\Documents\irAssignment1\docids.txt", "a",encoding=" utf-8 ")
        fd.write(file + "\\t" + str(docid)+"\n")
        fd.close()
        docid = docid+1
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
            for i, w in enumerate(vocab):
                w = w.lower()
                w = p_stemmer.stem(w)
                if w not in worddict and w not in stopwords:
                    worddict[w] = termid
                    wordinfoHash[termid] = TokenHashmap()
                    wordinfoHash[termid].docs = list()
                    wordinfoHash[termid].pos = list()
                    wordinfoHash[termid].docs.append(docid)
                    wordinfoHash[termid].pos.append(i)
                    wordinfoHash[termid].numberOfOccurences = wordinfoHash[termid].numberOfOccurences+1
                    wordinfoHash[termid].totalNoOfDocs = wordinfoHash[termid].totalNoOfDocs+1
                    #without hashmap:
                    wordinfoWithoutHash.append(TokenWithoutHashmap())
                    wordinfoWithoutHash[termid].termid = termid
                    wordinfoWithoutHash[termid].docs = list()
                    wordinfoWithoutHash[termid].pos = list()
                    wordinfoWithoutHash[termid].docs.append(docid)
                    wordinfoWithoutHash[termid].pos.append(i)
                    wordinfoWithoutHash[termid].numberOfOccurences = wordinfoWithoutHash[termid].numberOfOccurences+1
                    wordinfoWithoutHash[termid].totalNoOfDocs = wordinfoWithoutHash[termid].totalNoOfDocs+1

                    termid = termid+1
                else:
                    ids = worddict.get(w,None)
                    if ids:
                        print(ids)
                        wordinfoHash[ids].pos.append(i)
                        wordinfoHash[ids].docs.append(docid)
                        wordinfoHash[ids].numberOfOccurences = wordinfoHash[ids].numberOfOccurences+1
                        wordinfoHash[ids].totalNoOfDocs = wordinfoHash[ids].totalNoOfDocs+1
                    #without hashmap
                    idW = None
                    for ind in range(0,len(wordinfoWithoutHash)):
                        if wordinfoWithoutHash[ind].termid == ids:
                            idW = ind
                    if idW:
                        wordinfoWithoutHash[idW].docs.append(docid)
                        wordinfoWithoutHash[idW].pos.append(i)
                        wordinfoWithoutHash[idW].numberOfOccurences = wordinfoWithoutHash[idW].numberOfOccurences+1
                        wordinfoWithoutHash[idW].totalNoOfDocs = wordinfoWithoutHash[idW].totalNoOfDocs+1
    #sorting
    idW=0                
    for idW in range(0,len(wordinfoWithoutHash)):
        [list(x) for x in zip(*sorted(zip(wordinfoWithoutHash[idW].docs, wordinfoWithoutHash[idW].pos), key=itemgetter(0)))]
    ids=0                
    for idW in range(0,len(wordinfoWithoutHash)):
        [list(x) for x in zip(*sorted(zip(wordinfoHash[ids].docs, wordinfoHash[ids].pos), key=itemgetter(0)))]
    #termids.txt
    f = open(r"C:\Users\lenovo\Documents\irAssignment1\termids.txt", "w",encoding=" utf-8 ")
    for w in worddict:
        f.write(w + "\\t" + str(worddict[w])+"\n")
    f.close()
    
    # delta encoding:
    print("ENCODING STARTS:")
    for w in wordinfoHash:
        for p in range(len(wordinfoHash[w].docs)-1,0,-1):
            wordinfoHash[w].docs[p] = wordinfoHash[w].docs[p] -wordinfoHash[w].docs[p-1]
    for w in wordinfoHash:
        for p in range(len(wordinfoHash[w].pos)-1,0,-1):
            if wordinfoHash[w].pos[p] -wordinfoHash[w].pos[p-1]>=0:
                wordinfoHash[w].pos[p] = wordinfoHash[w].pos[p] -wordinfoHash[w].pos[p-1]
    
    #for w in range(0,len(wordinfoWithoutHash)):
        #for p in range(0,len(wordinfoWithoutHash[w].pos)):
    
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
    for w in range(0,len(wordinfoWithoutHash)):
        f.write(str(wordinfoWithoutHash[w].termid) + " " + str(wordinfoWithoutHash[w].numberOfOccurences) +" "+str(wordinfoWithoutHash[w].totalNoOfDocs) +" ")
        for p in range(0,len(wordinfoWithoutHash[w].pos)):
            f.write(str(wordinfoWithoutHash[w].docs[p]) +","+str(wordinfoWithoutHash[w].pos[p]) + " ")
        f.write("\n")            
    f.close()
    
else:
    print("Folder doesn't exist, try entering the complete path")

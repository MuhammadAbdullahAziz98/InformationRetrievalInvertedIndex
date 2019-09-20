# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 00:38:29 2019

@author: abdullah
"""
# -*- coding: utf-8 -*-
#imports
import os,glob
import sys
from bs4 import BeautifulSoup,Comment
import re
from nltk.stem.porter import PorterStemmer
    
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
if filename == None or filename=="":
    print("No corpus provided")
else:
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
        docid=  0
        worddict =  dict()
        wordinfoHash = dict()
        wordinfoWithoutHash = list()
        p_stemmer = PorterStemmer()
        fd = open(r"C:\Users\lenovo\Documents\irAssignment1\docids.txt", "w",encoding=" utf-8 ")
        fd.write("")
        fd.close()
    
        for file in glob.glob("*"):
            try:
                fp = open(file,"r",encoding="Latin-1")
            except IOError:
                fp = None
                print("Can't open")            #check after opening file
            if fp:
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
                    docWords = soup.body.get_text()
                    pattern = r'\$*\w+\-*\w+|^\s|\$*\w+\.\w+'
                    vocab = re.findall(pattern,docWords)
                    for i, w in enumerate(vocab):
                        w = w.lower()
                        w = p_stemmer.stem(w)
                        if w!= '\n' and w!= '' and w!=' ' and w!='\t' and w not in worddict and w not in stopwords:
                            print(termid)
                            worddict[w] = termid
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
                                t = TokenWithoutHashmap()
                                t.docid = docid
                                t.termid = ids
                                t.pos = i
                                wordinfoWithoutHash.append(t)
                    fp.close()
        
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
        
        for w in range(0,len(wordinfo)):
            for p in range(len(wordinfo[w].docs)-1,0,-1):
                wordinfo[w].docs[p] = wordinfo[w].docs[p] - wordinfo[w].docs[p-1]
        for w in range(0,len(wordinfo)):
            for p in range(len(wordinfo[w].docs)-1,0,-1):
                if wordinfo[w].pos[p] -wordinfo[w].pos[p-1]>=0:
                    wordinfo[w].pos[p] = wordinfo[w].pos[p] - wordinfo[w].pos[p-1]
        
        #inverted index without hashmap 
        f = open(r"C:\Users\lenovo\Documents\irAssignment1\termindex_withouthashmap.txt", "w",encoding=" utf-8 ")
        for w in range(0,len(wordinfo)):
            f.write(str(wordinfo[w].termid) + " " + str(wordinfo[w].numberOfOccurences) +" "+str(wordinfo[w].totalNoOfDocs) +" ")
            for p in range(0,len(wordinfo[w].pos)):
                f.write(str(wordinfo[w].docs[p]) +","+str(wordinfo[w].pos[p]) + " ")
            f.write("\n\n\n")            
        
        f.close()
        
    else:
        print("Folder doesn't exist, try entering the complete path")



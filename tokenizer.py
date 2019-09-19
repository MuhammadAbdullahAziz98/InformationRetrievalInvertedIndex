# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 21:17:32 2019

@author: abdullah
"""

# -*- coding: utf-8 -*-

#imports
import os,glob
import sys
from bs4 import BeautifulSoup,Comment
import re
from nltk.stem.porter import PorterStemmer

class TokenHashmap:
    numberOfOccurences = 0
    totalNoOfDocs = 0
    docs = list()
    pos = list()
    
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
    
        for file in glob.glob("Clueweb12-0901wb-49-18208"):
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
                    pattern = r'\$*\w+\-*\.*\w+|^\s|\$*\w+\.\w+\.w*'
                    vocab = re.findall(pattern,docWords)
                    for i, w in enumerate(vocab):
                        w = w.lower()
                        w = p_stemmer.stem(w)
                        if w!= '\n' and w!= '' and w!=' ' and w!='\t' and w not in worddict and w not in stopwords:
                            print(termid)
                            worddict[w] = termid
                            wordinfoHash[termid] = TokenHashmap()
                            wordinfoHash[termid].docs = list()
                            wordinfoHash[termid].pos = list()
                            wordinfoHash[termid].docs.append(docid)
                            wordinfoHash[termid].pos.append(i)
                            wordinfoHash[termid].numberOfOccurences = wordinfoHash[termid].numberOfOccurences+1
                            wordinfoHash[termid].totalNoOfDocs = wordinfoHash[termid].totalNoOfDocs+1    
                            termid = termid+1
                        else:
                            ids = worddict.get(w,None)
                            if ids:
                                wordinfoHash[ids].pos.append(i)
                                wordinfoHash[ids].docs.append(docid)
                                wordinfoHash[ids].numberOfOccurences = wordinfoHash[ids].numberOfOccurences+1
                                wordinfoHash[ids].totalNoOfDocs = wordinfoHash[ids].totalNoOfDocs+1
                    fp.close()
    
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
            
        #inverted index with hashmap 
        f = open(r"C:\Users\lenovo\Documents\irAssignment1\termindex_hashmap.txt", "w",encoding=" utf-8 ")
        fi = open(r"C:\Users\lenovo\Documents\irAssignment1\terminfo.txt", "w",encoding=" utf-8 ")
        for w in wordinfoHash:
            fi.write(str(w)+"\\t" +str(f.tell()))
            fi.write("\n")            
            f.write(str(w) + " " + str(wordinfoHash[w].numberOfOccurences) +" "+str(wordinfoHash[w].totalNoOfDocs) +" ")
            for p in range(0,len(wordinfoHash[w].pos)):
                f.write(str(wordinfoHash[w].docs[p]) +","+str(wordinfoHash[w].pos[p]) + " ")
            f.write("\n\n\n")            
        f.close()
        fi.close()

    else:
        print("Folder doesn't exist, try entering the complete path")
    

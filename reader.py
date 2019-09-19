# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 13:30:04 2019

@author: abdullah
"""
#part3

import sys
from nltk.stem.porter import PorterStemmer


f = open(r"C:\Users\lenovo\Documents\irAssignment1\termindex_hashmap.txt", "r",encoding=" utf-8 ")
fi = open(r"C:\Users\lenovo\Documents\irAssignment1\terminfo.txt", "r",encoding=" utf-8 ")

ft = open(r"C:\Users\lenovo\Documents\irAssignment1\termids.txt", "r",encoding=" utf-8 ")

# count the arguments
arguments = len(sys.argv) - 1

p_stemmer = PorterStemmer()
position = 2
args = sys.argv[position]
args = args.lower()
args = p_stemmer.stem(args)

terms = ft.read() 
info = list(terms.splitlines())
items = dict()
for i in info:
    items[i.split('\\t')[0]] = i.split('\\t')[1] 

ids = items[args]
if args not in items:
    print("word not found in corpus!")    
else:
    
    terminfo = fi.read() 
    info = list(terminfo.splitlines())
    infoitems = dict()
    for i in info:
        infoitems[i.split('\\t')[0]] = i.split('\\t')[1] 
    offset = infoitems[ids]
    f.seek(int(offset))
    indexed = f.readline()
    #index = indexed.split()
    print("\n")
    index = indexed.split()
    print("Listing for term: " +args +"\nTERMID: " + ids + "\nNumber of documents containing term: "+ index[1] + "\nTerm frequency in corpus: "+index[2])

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

if os.path.exists(filename):
    os.chdir(filename)
    for file in glob.glob("*"):
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
            print(docWords)
            wordlist =  list()
            pattern = '[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+|[]!"$%&\'()*+,./:;=#@?[\\^_`{|}~-]+'
            for w in docWords:
                wordlist.append(re.findall(pattern,w))
           # print(wordlist)            
            print("FILE ENDS HEREE!!!!!!!!!!!!!!!!!!")
        
else:
    print("Folder doesn't exist, try entering the complete path")

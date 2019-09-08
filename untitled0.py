# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 21:17:32 2019

@author: abdullah
"""

# -*- coding: utf-8 -*-

#imports
import glob, os
import sys


#getting arguments:

filename = sys.argv[1]
if os.path.exists(filename):
    os.chdir(filename)
    for file in glob.glob("clueweb12-0000tw-14-17002.txt"):
        #print(file)
        fp = open(file,'r',encoding=" Latin-1 ")
        print(fp.read())
else:
    print("Folder doesn't exist, try entering the complete path")

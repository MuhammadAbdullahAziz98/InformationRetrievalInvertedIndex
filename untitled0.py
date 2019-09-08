# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 21:17:32 2019

@author: abdullah
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import glob, os
os.chdir(r"C:\Users\lenovo\Downloads\corpus\corpus\corpus")
for file in glob.glob("clueweb12-0000tw-14-17002.txt"):
    #print(file)
    fp = open(file,'r',encoding=" Latin-1 ")
    print(fp.read())
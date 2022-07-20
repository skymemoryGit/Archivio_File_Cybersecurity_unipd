# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 13:20:22 2020

@author: Ye Jian_cheng
"""
import numpy as np

myNpArray = np.zeros([0, 32])
for x in range(0,32,1):
    randomList = [list(np.random.randint(99, size=32))]
    myNpArray = np.vstack((myNpArray, randomList))

myNpArray = myNpArray[1:]

print(myNpArray)
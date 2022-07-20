# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:36:44 2020

@author: Ye Jian_cheng
"""

#birth paradox trivial program

import sys

import math


n=500


for i in range(10,90):
    tmp= math.factorial(n)/math.factorial(n-i)
    tmp2= n**i
    ris= 1-(tmp/tmp2)
    
    print (str(i)+"persone-->"+str(ris))
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 10:57:46 2020

@author: Ye Jian_cheng
"""


def subkey_gen(key,r ):  #r= round
    ls=[]
    for i in range(1,33):
        index= ((5*r + i -1)%32) +1
        index=index-1
      
        print("index: "+str(index))
        print ("the position in key: " +str(key[index]))
        ls.append(key[index])

    #return
    r=''
    for i in range(0,len(ls)):
        r=r+ls[i]
    return r
        




        
        
    
    
    
    
#test case

m ='10000000000000000000000000000000'
k ='qwerrfssdsdsdsdsdsddssdsdsdsdsdd'

for i in range(1,2):
    subkey = subkey_gen(k,i) #sub key for round1 

    print(subkey)


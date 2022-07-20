# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 11:14:05 2020

@author: Ye Jian_cheng
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 04:23:08 2020
@author: Ayca & Emanuele
"""

#%%
def hexToBinary(h):
    return "{0:b}".format(int(h))

#outputing the hex version of cipher text
def binaryToHex(x):
    x_str = ""
    for i in range(0,len(x)):
        x_str += str(x[i])
    x_hex = hex(int(x_str, 2))
    print("Hex verison: ",hex(int(x_str, 2)))
    return x_hex

#printEnc function to format output of Encryption
def printEnc(x):
    print("\nEncryption:")
    print("x:", x)
    binaryToHex(x)
    
#printDec function to format output of Decryption
def printDec(u)  :
    print("\nDecryption:")
    print("u:", u)
    binaryToHex(u)
    
    
##Feistel cipher with linear f - Task 1
def linear_f(y,k):
    l=len(y)
    w =[]
    for j in range(1,l+1): #1 to 16
        if j>=1 and j<=l/2: #1 to l/2 = 8
            tmp = y[j-1] ^ k[int(4*j-3)-1]
        elif j>l/2 and j <=l: #15
            tmp = y[j-1] ^ k[int(4*j-2*l)-1]
        w.append(tmp)
    return w


##Feistel cipher with nearly-linear f - Task 5
def nearlyLinear_f(y,k):
    l=len(y)
    w =[]
    for j in range(1,l+1): #1 to 16
        if j>=1 and j<=l/2: #1 to l/2 = 8
            tmp = y[j-1] ^ (k[int(4*j-3)-1] & 
                            (y[(2*j -1) -1] #y[2j-1]
                            | k[(2*j -1) -1] #k[2j-1]
                            | k[(2*j)-1] #k[2j]
                            | k[(4*j -2) -1]))
        elif j>l/2 and j <=l: #15
            tmp = y[j-1] ^ (k[int(4*j-2*l) -1] and 
                            (k[(4*j-2*l-1) -1]
                             or k[(2*j-1) -1]
                             or k[(2*j) -1]
                             or y[(2*j-l)-1]))        
        w.append(tmp)
    return w


##Feistel cipher with non-linear f - Task 7
def nonLinear_f(y,k):
    l=len(y)
    w =[]
    for j in range(1,l+1): #1 to 16
        if j>=1 and j<=l/2: #1 to l/2 = 8
            tmp = ((y[j-1] & k[(2*j-1) -1]) | 
                   (y[(2*j-1) -1] & k[(2*j) -1]) | 
                   k[(4*j) -1])
        elif j>l/2 and j <=l: #15
            tmp = ((y[j-1] & k[(2*j-1) -1]) | 
                   (k[(4*j-2*l-1) -1] & k[(2*j) -1]) | 
                   y[(2*j-l) -1])
        w.append(tmp)
    return w

##bitwise addition function
def addition(z,w):
    v=[]
    for i in range(0,len(w)):
        v.append((w[i]^z[i])) #(w[i]+z[i])%2
    return v

##key generation function - depends only on k0 and roundNumber
def keyGeneration(k,i):
    tmp = []
    for j in range(1,len(k)+1): # 1 to 32
        tmp.append(k[((5*(i+1)+j-1)%len(k))])
    return tmp

#%% Encryption
def Encryption(u,k,n,taskNumber):
    #print("\n\nEncryption:\n")
    y = u[:int(len(u)/2)] #initialize y
    z = u[int(len(u)/2):] #initialize z
    k = []

    for i in range(0,n): # i represents the roundnumber here
        
        new_key = keyGeneration(k0,i) #generate key for i-th round
        k.append(new_key) ##attach it to list of key
        
        #Calculate round functions base on task number
        if taskNumber == 1:
            w = linear_f(y,k[i]) #compute w
        elif taskNumber == 5:
            w = nearlyLinear_f(y,k[i])
        elif taskNumber ==7:
            w = nonLinear_f(y,k[i])
            
        v = addition(z,w) #compute v and attach to its list
        
        if (i<n-1): # we are ignoring the last transposition
            new_z,new_y = y,v #transposition
            y = new_y #y for the next round
            z = new_z #z for the next round
        
        x =  y + v
    return x,k
#calling encryption:
# x = Encryption(null_vector,matrixI[i],17,1)[0]
# k = Encryption(null_vector,matrixI[i],17,1)[1]
# x,k = Encryption(null_vector,matrixI[i],17,1)
#%% Task 2 - Decryption 
def Decryption(x,k,n,taskNumber): # k = is list of generated keys
    #print("\n\nDecryption:\n")

    y = x[:int(len(x)/2)] #initialize y
    v = x[int(len(x)/2):] #initialize v
    k.reverse()
    u_l = []
    for i in range(0,n):
        w = linear_f(y,k[i]) #compute w
        z = addition(v,w) #compute v and attach to its list
        
        if (i<n-1):
            new_v,new_y = y,z #transposition
            y = new_y #y for the next round
            v = new_v #z for the next round
        
        u =  y +z
        u_l.append(u)
    return u
#%%
import numpy as np
#Task 3/4
#find matrix A

def find_A(lu,lk):
    matrixI = np.identity(lk)
    matrixI = matrixI.astype(int)
    a=[]
    null_vector = np.zeros(lu,dtype=int)
    null_vector = null_vector.astype(int)
    
    for i in range (0, lu):
        tmp = Encryption(matrixI[i],null_vector,17,1)[0]
        #print(tmp)
        
        #Encryption func returns 2 values: x and k
        # in that case we need to specify whether we want x or k
        a.append(tmp)
    
    #print(a)
    a1=np.transpose(a)
    
    #print("\n_______________________________________\n")
    #print(a1)
    
    return a1

#find matrix B
def find_B(lu,lk):
    matrixI = np.identity(lk)
    #print(matrixI)
    b=[]
    null_vector = np.zeros(lu, dtype=int)
    for i in range (0, lu):
        tmp = Encryption(null_vector,matrixI[i],17,1)[0]
        b.append(tmp)
        #print(tmp)
    b1=np.transpose(b)
    return b1

#linear cryptoanalusis KPA
def linear_cryptoanalysis_KPA(u,x):
    
    a=find_A(int(len(u)),int(len(u)))
    


    a_inv = np.linalg.inv(a)
    det = np.linalg.det(a)
    a_invb = np.mod(((a_inv.astype(int))*det),2)
  
   
   
    b= find_B(int(len(u)),int(len(u)))
    
    
    tmp = x + np.matmul(b,u)
    k = np.matmul(a_invb,tmp)
    
    
    
    
    #print("hacked key BEFORE MOD 2:" +str(k))
    
    #does not work the follow automatic mod function
    #k = np.mod(k,2)
    #print(k)
     
    
    #MOD 2
    ls=[]
    for i in range(0,32):
       # print((k[i]))     
        if (round(k[i])%2==0):    #round fuction 0.99999 =1 ; 2.000032 = 2;
            ls.append(0)
        else: 
            ls.append(1)
    
        
    
    
    
    return ls






########################################################################################
#main()

#%%Task1 - Test
  
print("Task 1")
lu = 32
lx = 32
l = 16
lk = 32
n = 17

k0 = 0x80000000
k0 = list(hexToBinary(k0))
k0 = [int(i) for i in k0] 


u = 0x80000000 #
u = list(hexToBinary(u))
u = [int(i) for i in u] 
x1,k = Encryption(u,k0,n,1)
printEnc(x1)

print("\n\nTask 2")
u_res1 = Decryption(x1,k,n,1)
printDec(u_res1)


#%%Task 3-4 
print("\n\nTask 3-4")
#trying to find k with linear cipher



pair=[
      
      [0x352E9951,0xB2928F57],
      [0x4D1E7AC0,0x29336CC6],
      [0x788E6EBC,0x08DF78BA],
      [0x3B0145A6,0x604A53A0],
      [0xD8249EFC,0x583588FA]
      
      ]

for i in range (0,len(pair)):
    #print("pair "+str(i+1))
    u = pair[i][0]#
    u = hexToBinary(u)
    u = u.zfill(lu) #zfill func to equalize current size of u to lu
    u = list(u)
    u = [int(i) for i in u] 
    
    x = pair[i][1]
    x = hexToBinary(x)
    x = x.zfill(lx) #zfill func to equalize current size of u to lu
    x = list(x)
    x = [int(i) for i in x] 
    
    
    
    k_hacked = linear_cryptoanalysis_KPA(u,x)
    print("hacked key:"+ str(k_hacked))
    #print("key zero:"+ str(k0))
    #print(k_hacked== k0)



#DECOMMENT FOLLOW FOR CHECK IT WORKS FOR U=0X8000000 AND X =0xD80B1A63
'''
u =0x80000000 
u = hexToBinary(u)
u = u.zfill(lu) #zfill func to equalize current size of u to lu
u = list(u)
u = [int(i) for i in u] 
    
x = 0xD80B1A63
x = hexToBinary(x)
x = x.zfill(lx) #zfill func to equalize current size of u to lu
x = list(x)
x = [int(i) for i in x] 
    
    
    
k_hacked = linear_cryptoanalysis_KPA(u,x)
print("hacked key:"+ str(k_hacked))

'''




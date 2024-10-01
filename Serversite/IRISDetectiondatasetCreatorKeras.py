# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 22:19:55 2020

@author: Arghya
"""

import cv2
import numpy as np
import os
from random import randint

clahe=cv2.createCLAHE()

def dataSetCreate(positivefolder,negetivefolder,datasetname):
    pos_list=os.listdir(positivefolder)
    neg_list=os.listdir(negetivefolder)
    
    l=[]
    r=[]
    t=[]
    z=[]
    for i in range(len(pos_list)):
        m=randint(0, len(neg_list)-1)
        try:
            s=cv2.imread(str(negetivefolder+"\\"+neg_list.pop(m)),cv2.IMREAD_GRAYSCALE)
            k,j=np.shape(s)
            l.append(clahe.apply(s).reshape(1,k*j))
            t.append(0)
            print("success",i,"for m=",m,"length=",len(neg_list))
        except :
            pass
    i=0
    while (len(pos_list)!=0):
        m=randint(0, len(pos_list)-1)
        try:
            s=cv2.imread(str(positivefolder+"\\"+pos_list.pop(m)),cv2.IMREAD_GRAYSCALE)
            k,j=np.shape(s)
            l.append(clahe.apply(s).reshape(1,k*j))
            t.append(1)
            i+=1
            print("success",i,"for m=",m,"length=",len(pos_list))
        except :
            pass
        
    while (len(l)!=0):
        m=randint(0, len(l)-1)
        r.append(l.pop(m))
        z.append(t.pop(m))
        
    return np.array(r,'uint8'),np.array(z,'uint8')
img,label=dataSetCreate("iris_data", "NegetiveImages", "datasetname")

try:    
    np.save('IrisKerasImage_data.npy',img,allow_pickle=True, fix_imports=True)
    print("Successfully File saved as IrisKerasImage_data.npy")
except:
    print("Fail to save Image File")
    
try:    
    np.save('IrisKeraslable_data.npy',label,allow_pickle=True, fix_imports=True)
    print("Successfully File saved as IrisKeraslable_data.npy")
except:
    print("Fail to save Lable File")
    
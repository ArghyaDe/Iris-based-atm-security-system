# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 17:59:16 2020

@author: Arghya
"""

#%%Importing Libraries

import socket
import numpy as np
import cv2
from tensorflow import keras as kr
import pandas as pd
from random import randint

#%%Initialization

GNID=pd.read_excel('GNID.xlsx').get('GNID')
model=kr.models.load_model("IrisRecognition.h5")
clahe=cv2.createCLAHE()

s=socket.socket()
host='192.168.0.4'
port=12033
s.bind((host,port))
s.listen(1)
print(host)
print("Waiting for any connection")

test_No=int(input("Enter test no: "))

#%%Server Running
for m in range(test_No):
    print("Waiting for any connection")
    conn,addr=s.accept()
    print(addr," has connencted")
    i=randint(0, 3)
    filedata=conn.recv(65538)
    try:
        im=filedata.decode('utf-8')
        img=im.split(',')
        img=np.array([img],'uint8')
        print("Received")
        img=clahe.apply(img)
        img=np.array(img,'float64')/255
        a=np.reshape(img,(1,128,128,1))
        pr=model.predict(a).argmax()
        if (pr!=0):
            conn.send(GNID[pr].encode())
        else:
            conn.send(str('None').encode())
    except :
        pass
    conn.close()
s.close()

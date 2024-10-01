# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 13:06:03 2020

@author: Arghya
"""

import numpy as np
import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('atm-security-stcet-firebase-certificate.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

doc_name='GN-********'

doc_ref=db.collection(u'Users').document(doc_name)
x=doc_ref.get()
l=x.to_dict()
noBank=l.get('NoBank')
Bank=l.get('Bank')
AccNo=l.get('AccountNo')
print("success")
print(l.get('Name'))
print(doc_name)
print(l.get('Name'))
print(noBank)
print(l.get('Email'))
for i in range(noBank):
    print(Bank[i])
    print(AccNo[i])
img=l.get('Image').split(',')
img=np.array([[img]],'uint8')
a=np.reshape(img,(200,150,3))
cv2.imwrite('temp.jpg',a)

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 00:21:47 2020

@author: Arghya
"""
#%%Importing Libraries
import numpy as np
import time
import cv2
import pandas as pd
import smtplib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from random import randint

#%%Initialization
cred = credentials.Certificate('atm-security-stcet-firebase-adminsdk-certificate.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
bank=[]
accountNo=[]
ammount=[]

#%%Taking Inputs
name=input("Name: ")
email=input("Enter Your Email: ")
MNo=input("Enter Your Mobile Number: ")
NoBank=int(input("Number of bank account: "))
for i in range(NoBank):
    bank.append(input("Bank Name: "))
    accountNo.append(input("Account Number: "))
    ammount.append(int(input("Enter Balance: ")))
    
path=input("Enter path of image:")

#%%Image to String
img=cv2.imread(path,cv2.IMREAD_COLOR)
img= cv2.resize(img,(int(150),int(200)),interpolation=cv2.INTER_AREA)
img=np.reshape(img,(1,int(150)*int(200)*3))
img=str(img.tolist()).split(', ')
img[len(img)-1]=img[len(img)-1][:len(img[len(img)-1])-2]
img[0]=img[0][2:]
img=','.join(img)

#%%SecretKey podusing
srt=str(randint(0,9))+str(randint(0,9))+str(randint(0,9))

#%%GNID Producing
t=time.localtime(time.time())
t=list(t)
rm=reversed(MNo)
rm=''.join(list(rm))
doc_name='GN-'+name[:3]+rm[:5]+str(t[0])+str(t[1])+str(t[2])+str(t[3])+str(t[4])+str(t[5])

#%%Uploading data to firebase
doc_ref = db.collection(u'Users').document(doc_name)
doc_ref.update({
    u'Name': name,
    u'NoBank': NoBank,
    u'Email':email,
    u'PhNo':MNo,
    u'Bank':bank,
    u'AccountNo':accountNo,
    u'Image':img,
    u'Ammount':ammount,
    u'SecretKey':srt
})

#%%Updating GNID Exel
exel_name="GNID.xlsx"
GNID=pd.read_excel(exel_name).get("GNID").tolist()
GNID.append(doc_name)
df=pd.DataFrame(GNID,columns=['GNID'])
df.to_excel(exel_name)

#%%Sending Mail
mail=smtplib.SMTP('smtp.gmail.com',587)
mail.starttls()

try:
    mail.login('abcd@gmail.com',"password")
    print("Login Successful!!")
except :
    print("Login Failed!!")

con="Your Generic ID is "+doc_name+"\n Your SecretKey is "+srt
try:
    mail.sendmail('abcd@gmail.com',email,con)
    print("Email Send Successfully")
except :
    print("Email is failed to send")
mail.quit()

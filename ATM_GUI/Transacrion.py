# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 15:57:43 2020

@author: Arghya
"""
import smtplib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def sendMail(Password,email,con):
    mail=smtplib.SMTP('smtp.gmail.com',587)
    mail.starttls()
    mail.login('abcd@gmail.com',Password)
    mail.sendmail('abcd@gmail.com',email,con)
    mail.quit()

cred = credentials.Certificate('F:\\4th_year_project\\ATM_GUI\\atm-security-stcet-firebase-adminsdk-certificate.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

doc_name=input()

doc_ref=db.collection(u'Users').document(doc_name)
x=doc_ref.get()
l=x.to_dict()

secretkey=input()
accountno=int(input())
ammount=int(input())
Password=input()

balance=l.get('Ammount')
con=l.get('Name')+',Your accountNo:'+l.get('AccountNo')[accountno][:2]+'xx xxxx xx'+l.get('AccountNo')[accountno][10:]+' has been debited Rs.'+str(ammount);
try:
    if(l.get('SecretKey')==secretkey and ammount<=balance[accountno]):
        balance[accountno]=balance[accountno]-ammount
        doc_ref.update({'Ammount':balance})
        try:
            sendMail(Password,l.get('Email'),con)
        except :
            pass
        print("success")
    else:
        print("failed")
except:
    print("failed")
    

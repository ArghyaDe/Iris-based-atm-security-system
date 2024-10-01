# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 14:23:02 2020

@author: Arghya
"""
#%%Importing Libraries
import cv2
import numpy as np
import socket
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from tensorflow import keras as kr

#%%Initialization
width=128
height=128
dim=(width,height)
eye_cascade=cv2.CascadeClassifier('haarcascade_eye.xml')
clahe=cv2.createCLAHE()
model=kr.models.load_model("IrisDetection.h5")
#%%IrisExtract function
def IrisExtract(gray):
    gray= cv2.resize(gray,dim,interpolation=cv2.INTER_AREA)
    
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray, (4, 4)) 
    
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred, 
    				cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
    			param2 = 30, minRadius = 10, maxRadius =40) 
    
    # Draw circles that are detected. 
    a,b,r=1,1,1
    t=False
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2] 
            m=clahe.apply(cv2.resize(gray[b-r:b+r,a-r:a+r],(50,50),interpolation=cv2.INTER_AREA)).reshape(1,50,50,1)
            norm=np.array(m,'float64')/255
            n=model.predict(norm).argmax()
            if(n==1):
                t=True
                break
    return t,cv2.resize(gray[b-r:b+r,a-r:a+r],dim,interpolation=cv2.INTER_AREA)

#%%Iris Capture function
def IrisCapture():
    cap=cv2.VideoCapture(0)
    while cap.isOpened():
        _,img=cap.read()
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        eye=None
        eye=eye_cascade.detectMultiScale(gray,1.1,4)
        if len(eye)!=0:
            try:
                (x,y,w,h)=eye[len(eye)-1]
                t,s=IrisExtract(gray[y:y+h,x:x+w])
                if t:
                    break
            except :
                pass
    cap.release()
    return s
    
#%%Image Sending Function
def sendImage(im_cl):
    s=socket.socket()
    ip="192.168.0.4"
    port=12033
    m,n=np.shape(im_cl)
    img=np.reshape(im_cl,(1,m*n))
    img=str(img.tolist()).split(', ')
    img[len(img)-1]=img[len(img)-1][:len(img[len(img)-1])-2]
    img[0]=img[0][2:]
    img=','.join(img)
    s.connect((ip,port))
    s.send(img.encode())
    l=s.recv(512)
    s.close()
    return l.decode('utf-8')

#%%Data retriving function
def getData(GNID):
    cred = credentials.Certificate('atm-security-stcet-firebase-adminsdk-6u1vm-a1113b8984.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    doc_ref=db.collection(u'Users').document(GNID)
    x=doc_ref.get()
    l=x.to_dict()
    img=l.get('Image')
    return img,l.get('Name'),l.get('Email'),l.get('NoBank'),l.get('AccountNo'),l.get('Bank')

#%%Main
im_cl=IrisCapture()
GNID=sendImage(im_cl)
if(GNID!=str('None')):
    Image,Name,Email,NoBank,AccountNo,Bank=getData(GNID)
    img=Image.split(',')
    img=np.array([[img]],'uint8')
    img=np.reshape(img,(200,150,3))
    cv2.imwrite("temp.jpg",img)
    print("success")
    print(Name)
    print(GNID)
    print(Name)
    print(NoBank)
    print(Email)
    for i in range(NoBank):
        print(Bank[i])
        print(AccountNo[i])
else:
    print("Failed")
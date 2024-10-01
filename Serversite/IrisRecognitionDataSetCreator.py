# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 20:01:52 2020

@author: Arghya
"""
#%% Importing Libraries
import os
import cv2
import numpy as np
import pandas as pd
from random import randint
from tensorflow import keras as kr

#%%Initialization
person=pd.read_excel("GNID.xlsx")
neg_list=os.listdir("NegetiveImages")
width=128
height=128
dim=(width,height)
eye_cascade=cv2.CascadeClassifier('haarcascade_eye.xml')
clahe=cv2.createCLAHE()
model=kr.models.load_model("IrisDetection.h5")
GNID=person.get('GNID')

#%%IrisExtract function
def IrisExtract(gray):
    gray= cv2.resize(gray,dim,interpolation=cv2.INTER_AREA)
    
    # Blur using 3 * 3 kernel. 
    gray_blurred = cv2.blur(gray, (4, 4)) 
    
    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred, 
    				cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
    			param2 = 30, minRadius = 10, maxRadius =40)  
    a,b,r=1,1,1
    t=False
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2] 
        m=clahe.apply(cv2.resize(gray[b-r:b+r,a-r:a+r],(50,50),interpolation=cv2.INTER_AREA)).reshape(1,50,50,1)
        n=model.predict(m).argmax()
        if(n==1):
            t=True
    return t,cv2.resize(gray[b-r:b+r,a-r:a+r],dim,interpolation=cv2.INTER_AREA)

#%%Data Adding
image_data=[]
lable_data=[]   


for filename in GNID:
    vidcap = cv2.VideoCapture((filename+'.mp4'))
    
    lable_no=person.index(filename)
    
    count=0
    success = True
    try:
        while success and count<3000:
            success,image = vidcap.read()
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            eye=eye_cascade.detectMultiScale(gray,1.1,4)
            if len(eye)!=0:
                try:
                    (x,y,w,h)=eye[len(eye)-1]
                    t,s=IrisExtract(gray[y:y+h,x:x+w])
                    if t:
                        img_=IrisExtract(s)
                        image_data.append(img_.reshape([1,width*height]))
                        lable_data.append(lable_no+1)
                        print('Read ',count,'th frame of',filename,': ', success,' And Iris found!!')
                except :
                    print('Read ',count,'th frame of',filename,': ', success,' But Iris not found!!')
            count+=1
    except :
        print(filename,"Fail")
    vidcap.release()
    
for i in range(3000):
    m=randint(0, len(neg_list)-1)
    try:
        s=cv2.imread(str("NegetiveImages\\"+neg_list.pop(m)),cv2.IMREAD_GRAYSCALE)
        s=cv2.resize(s,dim,cv2.INTER_AREA)
        image_data.append(clahe.apply(s).reshape(1,width*height))
        lable_data.append(0)
        print("Added ",i,"th negetive image Successfully")
    except :
        pass
    
#%%Suffeling

im_arr=[]
la_arr=[]

while len(image_data)!=0:
    i=randint(0,len(image_data)-1)
    im_arr.append(image_data.pop(i))
    la_arr.append(lable_data.pop(i))
    print('Remain data : ',len(image_data))
    
im_arr=np.array(im_arr,'uint8')
la_arr=np.array(la_arr,'uint8')
    
#%%Saving DataSet

try:    
    np.save('IrisRecognitionImage_data.npy',im_arr,allow_pickle=True, fix_imports=True)
    print("Successfully File saved as IrisRecognitionImage_data.npy")
except:
    print("Fail to save Image File")
try:    
    np.save('IrisRecognitionLable_data.npy',la_arr,allow_pickle=True, fix_imports=True)
    print("Successfully File saved as IrisRecognitionLable_data.npy")
except:
    print("Fail to save Lable File")
    

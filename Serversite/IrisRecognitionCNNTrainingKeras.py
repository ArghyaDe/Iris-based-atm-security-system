# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 17:14:49 2020

@author: Arghya
"""
#%%#%% Importing Libraries
import cv2
import numpy as np
from random import randint
import tensorflow as tf
import time
import matplotlib.pyplot as plt
import pandas as ps

#%%Initialization

csv_file='IrisRecognitionTrainingLog'+int(time.time())+'.csv'
csv_logger = tf.keras.callbacks.CSVLogger(csv_file)
clahe=cv2.createCLAHE()

width=128
height=128
IrisImage=np.load('IrisRecognitionImage_data.npy',allow_pickle=True, fix_imports=True)
Label=np.load('IrisRecognitionLable_data.npy',allow_pickle=True, fix_imports=True)

IrisImage=np.array(IrisImage,'float64')/255

#%%Devition of training & test Image

(training_images, training_labels), (test_images, test_labels) =(IrisImage[:int(len(IrisImage)/3)],Label[:int(len(Label)/3)]),(IrisImage[int(len(IrisImage)/3):],Label[int(len(Label)/3):])
training_images=np.array(training_images.reshape(len(training_images), width, height, 1),'float64')
test_images = np.array(test_images.reshape(len(test_images), width, height, 1),'float64')

#%%Defining model
model = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(width, height, 1)),
  tf.keras.layers.MaxPooling2D(2, 2),
  tf.keras.layers.Dropout(0.25),
  tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(width, height, 1)),
  tf.keras.layers.MaxPooling2D(2, 2),
  tf.keras.layers.Dropout(0.50),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(1280, activation='relu'),
  tf.keras.layers.Dense(Label.argmax(), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#%%Training
model.fit(training_images, training_labels,epochs=20,callbacks=[csv_logger])
test_loss, test_acc = model.evaluate(test_images, test_labels)
print("Accuracy: ",test_acc*100,"%")
print("Loss: ",test_loss*100,"%")
model.save("IrisRecognition.h5")
print("Model saved susccessfully")

#%%Ploting Graph

a=ps.read_csv(csv_file)
epoch=[0]
epoch.extend(list(a.get('epoch')+1))
acc=[0]
acc.extend(list(a.get("acc")*100))
loss=[100]
loss.extend(list(a.get("loss")*100))
plt.plot(epoch,acc,'',epoch,loss,'')
plt.grid()
plt.xlim([0,20])
plt.xlabel("Epoch")
plt.ylabel("Percentage")
plt.ylim([0,100])
plt.title("Accuracy and Loss V/S Epoch for Iris Recognition")
plt.show()

#%%Ploting Filter
f, axarr = plt.subplots(2,4)
FIRST_IMAGE=randint(0,9)
SECOND_IMAGE=randint(0,9)
CONVOLUTION_NUMBER = 1
layer_outputs = [layer.output for layer in model.layers]
activation_model = tf.keras.models.Model(inputs = model.input, outputs = layer_outputs)
for x in range(0,4):
  f1 = activation_model.predict(test_images[FIRST_IMAGE].reshape(1, width, height, 1))[x]
  axarr[0,x].imshow(f1[0, : , :, CONVOLUTION_NUMBER], cmap='inferno')
  axarr[0,x].grid(False)
  f2 = activation_model.predict(test_images[SECOND_IMAGE].reshape(1, width, height, 1))[x]
  axarr[1,x].imshow(f2[0, : , :, CONVOLUTION_NUMBER], cmap='inferno')
  axarr[1,x].grid(False)
  
print(model.predict(test_images[FIRST_IMAGE].reshape(1, width, height, 1)).argmax())
print(model.predict(test_images[SECOND_IMAGE].reshape(1, width, height, 1)).argmax())
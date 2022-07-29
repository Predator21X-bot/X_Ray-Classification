# -*- coding: utf-8 -*-
"""Summer_Internship_Project_on X-ray Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j2-JHAkCy6KUiL_c8Dp4IEQiEpWD92Fu
"""

import os
os.environ['KAGGLE_USERNAME'] = "sprihasinha"
os.environ['KAGGLE_KEY'] = "b85d5299a8a1b65f252d7fb521032c38"

!kaggle datasets download -d fusicfenta/chest-xray-for-covid19-detection

!unzip "/content/chest-xray-for-covid19-detection.zip"

len(os.listdir('/content/Dataset'))

len(os.listdir('/content/Dataset/Train'))

len(os.listdir('/content/Dataset/Val'))

len(os.listdir('/content/Dataset/Train/Covid'))

len(os.listdir('/content/Dataset/Train/Normal'))

len(os.listdir('/content/Dataset/Val/Covid'))

len(os.listdir('/content/Dataset/Val/Normal'))

import cv2
img = cv2.imread('/content/Dataset/Train/Normal/IM-0140-0001.jpeg')
import matplotlib.pyplot as plt
plt.imshow(img)

img.shape

urls = os.listdir('/content/Dataset/Train/Covid')        #name of images
path = "/content/Dataset/Train/Covid" + urls[0]         #one image path at a time
path

def loadImages(path, urls, target):
  images = []
  labels = []
  #for root, folder, files in os.walk(path)
  for i in range(len(urls)):
    img_path = path + "/" + urls[i]
    img = cv2.imread(img_path)        #read image one by one
    img = img / 255.0
    #print(img_path)
    # if we want to resize the images
    img = cv2.resize(img, (100, 100))
    images.append(img)                #storing images one by one
    labels.append(target)            
  images = np.asarray(images)
  return images, labels

import numpy as np
covid_path = "/content/Dataset/Train/Covid"
covidUrl = os.listdir(covid_path)
covidImages, covidTargets = loadImages(covid_path, covidUrl, 1)

normal_path = "/content/Dataset/Train/Normal"
normal_urls = os.listdir(normal_path)
normalImages, normalTargets = loadImages(normal_path, normal_urls, 0)

#convert data as numpy array as list cannot do everything like size, shape
covidImages = np.asarray(covidImages)
normalImages = np.asarray(normalImages)

len(covidUrl), len(covidImages)

covidImages.shape

covidImages[0].shape

normalImages.shape

data = np.r_[covidImages, normalImages]  #np.r_-----to stack the data row wise, similarly c_ to concatenate col wise.
data.shape

targets = np.r_[covidTargets, normalTargets]
targets.shape

data = data / 255.0

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(data, targets, test_size=0.25)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

model = Sequential([
    Conv2D(32, 3, input_shape=(100,100,3), activation='relu'),
    MaxPooling2D(),   #by default 2x2 pooling size so wrote nothing in brackets
    
    Conv2D(16, 3, activation='relu'),
    MaxPooling2D(),
    
    Conv2D(16, 3, activation='relu'),
    MaxPooling2D(),
    
    Flatten(),
    
    Dense(512, activation='relu'),    
    
    Dense(256, activation='relu'),
    
    Dense(1, activation='sigmoid')
])

from tensorflow.keras.utils import plot_model as plotter
plotter(model, to_file="arch.png", show_shapes=True, show_layer_names=True)

model.summary()

model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(),metrics=['accuracy'])
model.fit(x_train, y_train,batch_size=3,epochs=5,validation_data=(x_test, y_test))

!pip install visualkeras

import visualkeras
visualkeras.layered_view(model,legend=True)

plt.plot(model.history.history['accuracy'], label = 'train accuracy')
plt.plot(model.history.history['val_accuracy'],label = 'test_accuracy')
plt.legend()
plt.show()

plt.plot(model.history.history['loss'], label = 'train loss')
plt.plot(model.history.history['val_loss'],label = 'test_loss')
plt.legend()
plt.show()

#experimenting with other models
from tensorflow.keras.applications import Xception,VGG16,VGG19,ResNet50,InceptionV3,InceptionResNetV2,MobileNet,MobileNetV2

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    rotation_range=45,
    fill_mode='nearest'
    )

# test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = datagen.flow_from_directory(
    '/content/Dataset/Train',
    target_size=(224,224),
    batch_size=6,
    class_mode='binary',
    shuffle=True,
    # color_mode="grayscale"
    )

validation_generator = datagen.flow_from_directory(
    '/content/Dataset/Val',
    target_size=(224,224),
    batch_size=6,
    class_mode='binary',
    shuffle=True,
    # color_mode="grayscale"
    )

#experimenting with other models
from tensorflow.keras.applications import Xception,VGG16,VGG19,ResNet50,InceptionV3,InceptionResNetV2,MobileNet,MobileNetV2

hist = []

#Xception
model = Sequential()
pretrained_model= Xception(include_top=False,input_shape=(224,224,3),weights='imagenet')
for layer in pretrained_model.layers:
    layer.trainable=False
model.add(pretrained_model)
model.add(Flatten())
model.add(Dense(200, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
opt = keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train_generator,steps_per_epoch=148/6,epochs=3,validation_data=validation_generator,validation_steps=40/6,verbose=1)
h = model.evaluate(validation_generator,verbose=1)
hist.append([h[0],h[1],"Xception"])

#VGG16
model = Sequential()
pretrained_model= VGG16(include_top=False,input_shape=(224,224,3),weights='imagenet')
for layer in pretrained_model.layers:
    layer.trainable=False
model.add(pretrained_model)
model.add(Flatten())
model.add(Dense(200, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
opt = keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train_generator,steps_per_epoch=148/6,epochs=3,validation_data=validation_generator,validation_steps=40/6,verbose=1)
h = model.evaluate(validation_generator,verbose=1)
hist.append([h[0],h[1],"VGG16"])

#VGG19
model = Sequential()
pretrained_model= VGG19(include_top=False,input_shape=(224,224,3),weights='imagenet')
for layer in pretrained_model.layers:
    layer.trainable=False
model.add(pretrained_model)
model.add(Flatten())
model.add(Dense(200, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
opt = keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train_generator,steps_per_epoch=148/6,epochs=3,validation_data=validation_generator,validation_steps=40/6,verbose=1)
h = model.evaluate(validation_generator,verbose=1)
hist.append([h[0],h[1],"VGG19"])

#ResNet50
model = Sequential()
pretrained_model= ResNet50(include_top=False,input_shape=(224,224,3),weights='imagenet')
for layer in pretrained_model.layers:
    layer.trainable=False
model.add(pretrained_model)
model.add(Flatten())
model.add(Dense(200, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
opt = keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train_generator,steps_per_epoch=148/6,epochs=3,validation_data=validation_generator,validation_steps=40/6,verbose=1)
h = model.evaluate(validation_generator,verbose=1)
hist.append([h[0],h[1],"ResNet50"])

#InceptionV3
model = Sequential()
pretrained_model= InceptionV3(include_top=False,input_shape=(224,224,3),weights='imagenet')
for layer in pretrained_model.layers:
    layer.trainable=False
model.add(pretrained_model)
model.add(Flatten())
model.add(Dense(200, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
opt = keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train_generator,steps_per_epoch=148/6,epochs=3,validation_data=validation_generator,validation_steps=40/6,verbose=1)
h = model.evaluate(validation_generator,verbose=1)
hist.append([h[0],h[1],"InceptionV3"])

#InceptionResNetV2
model = Sequential()
pretrained_model= InceptionResNetV2(include_top=False,input_shape=(224,224,3),weights='imagenet')
for layer in pretrained_model.layers:
    layer.trainable=False
model.add(pretrained_model)
model.add(Flatten())
model.add(Dense(200, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
opt = keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train_generator,steps_per_epoch=148/6,epochs=3,validation_data=validation_generator,validation_steps=40/6,verbose=1)
h = model.evaluate(validation_generator,verbose=1)
hist.append([h[0],h[1],"InceptionResNetV2"])

#MobileNet
model = Sequential()
pretrained_model= MobileNet(include_top=False,input_shape=(224,224,3),weights='imagenet')
for layer in pretrained_model.layers:
    layer.trainable=False
model.add(pretrained_model)
model.add(Flatten())
model.add(Dense(200, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
opt = keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

model.fit(train_generator,steps_per_epoch=148/6,epochs=3,validation_data=validation_generator,validation_steps=40/6,verbose=1)
h = model.evaluate(validation_generator,verbose=1)
hist.append([h[0],h[1],"MobileNet"])

import pandas as pd
df = pd.DataFrame(hist)
df.columns = ["loss","accuracy","model_name"]

import seaborn as sns
sns.set(style='dark')
df.set_index('model_name').plot(kind='bar',color=['orange', 'blue'])


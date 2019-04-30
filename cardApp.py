#from darkflow.net.build import TFNet

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import matplotlib.pyplot as plt
import cv2
import os
from os import path
import numpy as np
import sys
import logging as log

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)
window.show()
app.exec_()

'''
options = {"model": "cfg/yolo-52c.cfg", 
           "load": -1, 
           "threshold": 0.001,
           "gpu": 0}

tfnet = TFNet(options)
#%%
def boxing(original_img, predictions, threshold):
    newImage = np.copy(original_img)

    for result in predictions:
        top_x = result['topleft']['x']
        top_y = result['topleft']['y']

        btm_x = result['bottomright']['x']
        btm_y = result['bottomright']['y']

        confidence = result['confidence']
        label = result['label'] #+ " " + str(round(confidence, 3))

        if confidence > threshold:
            newImage = cv2.rectangle(newImage, (top_x, top_y), (btm_x, btm_y), (255,155,0), 3)
            newImage = cv2.putText(newImage, label, (top_x, top_y-3), cv2.FONT_HERSHEY_PLAIN , 1.5, (255, 55, 0), 2, cv2.LINE_AA)
            
    return newImage

#%% 

threshold = 0.1
load_img = cv2.imread('sample_img/sample_cards7.jpg')
original_img = cv2.cvtColor(load_img, cv2.COLOR_BGR2RGB)
results = tfnet.return_predict(original_img)
'''
# Example Results Output
results = [
   {'label': 'AC', 'confidence': 0.21588273, 'topleft': {'x': 89, 'y': 273}, 'bottomright': {'x': 152, 'y': 408}}, 
   {'label': '4C', 'confidence': 0.007568298, 'topleft': {'x': 187, 'y': 200}, 'bottomright': {'x': 233, 'y': 288}}, 
   {'label': 'KS', 'confidence': 0.21859957, 'topleft': {'x': 175, 'y': 176}, 'bottomright': {'x': 249, 'y': 320}}, 
   {'label': '10S', 'confidence': 0.9281746, 'topleft': {'x': 535, 'y': 137}, 'bottomright': {'x': 602, 'y': 256}}, 
   {'label': '10C', 'confidence': 0.02675374, 'topleft': {'x': 522, 'y': 149}, 'bottomright': {'x': 615, 'y': 250}}, 
   {'label': '10C', 'confidence': 0.015623447, 'topleft': {'x': 731, 'y': 822}, 'bottomright': {'x': 815, 'y': 961}}, 
   {'label': '10S', 'confidence': 0.8346538, 'topleft': {'x': 728, 'y': 808}, 'bottomright': {'x': 817, 'y': 961}}, 
   {'label': 'QC', 'confidence': 0.0065161083, 'topleft': {'x': 301, 'y': 161}, 'bottomright': {'x': 357, 'y': 257}},
   {'label': '7C', 'confidence': 0.030605286, 'topleft': {'x': 425, 'y': 143}, 'bottomright': {'x': 474, 'y': 259}},
   {'label': 'JS', 'confidence': 0.4261645, 'topleft': {'x': 424, 'y': 122}, 'bottomright': {'x': 495, 'y': 277}}, 
   {'label': '9S', 'confidence': 0.49044922, 'topleft': {'x': 306, 'y': 142}, 'bottomright': {'x': 356, 'y': 285}}, 
   {'label': '7C', 'confidence': 0.0016710977, 'topleft': {'x': 320, 'y': 168}, 'bottomright': {'x': 359, 'y': 270}}, 
   {'label': '4S', 'confidence': 0.24186157, 'topleft': {'x': 172, 'y': 192}, 'bottomright': {'x': 255, 'y': 321}}, 
   {'label': 'AS', 'confidence': 0.35704327, 'topleft': {'x': 80, 'y': 276}, 'bottomright': {'x': 154, 'y': 403}}, 
   {'label': 'JS', 'confidence': 0.013619435, 'topleft': {'x': 316, 'y': 138}, 'bottomright': {'x': 367, 'y': 290}},
   {'label': '5S', 'confidence': 0.0014446479, 'topleft': {'x': 156, 'y': 209}, 'bottomright': {'x': 262, 'y': 315}}
]

'''
# Iterate through list of dictionaries
extension="png"
card_dir="card_imgs"
'''
itCnt = 0
#If detected 5 out of the last 10 fromes, detected.
confidence = 0
detDict = {}
cardList = [d['label'] for d in results]
confList = [d['confidence'] for d in results]
'''for i in range(results):
    for key,val in results[i].items():
        if key == 'label':
            card_name = val
            #img_dir = os.path.join(card_dir,card_name+"."+extension)
        if key == 'confidence' and val>=0.01:
            confidence = val*10
            detDict[card_name] = confidence #out of 100
'''
ccDict = dict(zip(cardList,confList)) #create dictionary of cards
ccDict_fixed = {card:conf for card,conf in ccDict.items() if conf>=0.1}
for card,conf in ccDict_fixed.items():
    ccDict_fixed[card] *= 10
'''Debugging
for k,v in ccDict.items():
    print(k,v)
for k,v in ccDict_fixed.items():
    print(k,v)
print(*cardList)
print(*confList)
'''




# If card detected 5 times out of 10 frames, output as 

'''
_, ax = plt.subplots(figsize=(20, 10))
plt.imshow(boxing(original_img, results, threshold))
'''
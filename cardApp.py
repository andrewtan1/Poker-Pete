#from darkflow.net.build import TFNet

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QProgressBar, QGridLayout, QDialog, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
import cv2
import os
from os import path
import numpy as np
import sys
import logging as log
import operator

class recordVideo:
    def __init__(self, camera_port=0):
            self.camera = cv2.VideoCapture(0)
            self.running = False

    def run(self):
            self.running = True
            while self.running:
                read, frame = self.camera.read()
           
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
# Example Results Output - TODO: Replace with continuous input
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


itCnt = 0
#If detected 5 out of the last 10 fromes, detected.
confidence = 0
detDict = {}

# Declare Confidence Threshold for Display
thresh = 0.1

# Grab Detected Cards w/ their Confidences
cardList = [d['label'] for d in results]
confList = [d['confidence'] for d in results]

# Sort the Detected Cards w/ their Confidences
ccDict = dict(zip(cardList,confList)) #create dictionary of cards
ccDict_fixed = {card:conf for card,conf in ccDict.items() if conf>=thresh} #only take values of acceptable confidence
for card,conf in ccDict_fixed.items():
    newConf = float("{0:.1f}".format(ccDict_fixed[card]*100))
    ccDict_fixed[card] = newConf
sorted_cc = sorted(ccDict_fixed.items(), key=operator.itemgetter(1), reverse=True)

# Create a list of Tuples for the number representation of each card
# Map Ranks to Numbers for Calculations
def rankMap(rank):
    rankNum = {
        'A':0,
        '2':1,
        '3':2,
        '4':3,
        '5':4,
        '6':5,
        '7':6,
        '8':7,
        '9':8,
        '10':9,
        'J':10,
        'Q':11,
        'K':12
    }
    return rankNum.get(rank,"no rank")
# Map Suits to Numbers for Calculations
def suitMap(suit):
    suitNum = {
        'D':0,
        'C':1,
        'H':2,
        'S':3
    }
    return suitNum.get(suit,"no suit")
# Iterate through each detected card and map to numbers
cards = [item[0] for item in sorted_cc]
rankList = []
suitList = []
for c in cards:
    if len(c)>2:
        rank = c[:2]
        suit = c[2:3]
    else:
        rank = c[:1]
        suit = c[1:2]
    rankList.append(rankMap(rank))
    suitList.append(suitMap(suit))
cardNumConv = list(zip(rankList,suitList))
print(cardNumConv) # Check Output

class App(QDialog):
    def __init__(self):
        super(App, self).__init__()
        self.title = 'Poker Pete Visualization'
        # Set Window Location/Dimensions At Startup
        self.left = 200
        self.top = 200
        self.width = 500
        self.height = 500
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
        self.show()
    
    def createLayout(self):
        self.horizontalGroupBox = QGroupBox("Cards-Confidence List")
        layout = QGridLayout()
        layout.setColumnStretch(1, 7)

        card_dir = "card_imgs"
        extension = "png"
        cardList = [item[0] for item in sorted_cc]
        confList = [item[1] for item in sorted_cc]
        
        for ind in range(len(sorted_cc)):
            # Create Card Image Widget
            pic = QtWidgets.QLabel(self) 
            img_dir = os.path.join(card_dir,cardList[ind]+"."+extension)
            imgPix = QtGui.QPixmap(os.getcwd()+"/"+img_dir)
            imgPixScaled = imgPix.scaledToHeight(98) # 98x70 image
            pic.setPixmap(imgPixScaled)
            self.resize(imgPixScaled.width(),imgPixScaled.height())
            layout.addWidget(pic,ind,0)
            # Create Project Bar Widget
            bar = QtWidgets.QProgressBar(self)
            bar.setValue(confList[ind])
            layout.addWidget(bar,ind,1)
        
        self.horizontalGroupBox.setLayout(layout)
        
#Debugging
#for k,v in ccDict.items():
#    print(k,v)
#for k,v in ccDict_fixed.items():
#    print(k,v)
#print(*cardList)
#print(*confList)
#print(results)
#print(ccDict_fixed)
#print(sorted_cc)





# If card detected 5 times out of 10 frames, output as 

'''
_, ax = plt.subplots(figsize=(20, 10))
plt.imshow(boxing(original_img, results, threshold))
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
'''
window.setLayout(layout)
window.show()
app.exec_()
'''
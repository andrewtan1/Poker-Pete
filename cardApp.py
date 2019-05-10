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
           
class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        h_layout = QHBoxLayout()
        self.layout().addLayout(h_layout)
        label = QLabel(self)
        label.setText('Card')

        bar = QProgressBar(self)
        policy = bar.sizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Expanding)
        bar.setSizePolicy(policy)

        h_layout.addWidget(label)
        h_layout.addWidget(bar)
        button = QPushButton('Ok')
        self.layout().addWidget(button)
        self.resize(200, 50)
        self.show()        


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


itCnt = 0
#If detected 5 out of the last 10 fromes, detected.
confidence = 0
detDict = {}
cardList = [d['label'] for d in results]
confList = [d['confidence'] for d in results]

ccDict = dict(zip(cardList,confList)) #create dictionary of cards
ccDict_fixed = {card:conf for card,conf in ccDict.items() if conf>=0.1} #only take values of acceptable confidence
for card,conf in ccDict_fixed.items():
    newConf = float("{0:.1f}".format(ccDict_fixed[card]*100))
    ccDict_fixed[card] = newConf
    # append card img to each key
    #ccDict_fixed[card].
sorted_cc = sorted(ccDict_fixed.items(), key=operator.itemgetter(1), reverse=True)
'''
#Display Image
pic = QtWidgets.QLabel(window)
pic.setGeometry(10, 10, 238, 333) #TODO: Change geometry to be size of resized image
pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/card_imgs/10C.png"))
'''

class cardImg(QWidget):

    def _init_(self):
        super(cardImg, self)._init_()
        #self.window = QtWidgets.QMainWindow()
        card_dir = "card_imgs"
        extension = "png"
        cardList = sorted_cc
        numCard = len(cardList)
        lay = QVBoxLayout(self)
        self.cardBar()

    def cardBar(self):
        # Image Representation of Card
        for ind in range(numCard):
            pic = QtWidgets.QLabel(self)
            #pic.setGeometry(10, 10, 71, 100) 
            img_dir = os.path.join(card_dir,cardList[ind]+"."+extension)
            imgPix = QtGui.QPixmap(os.getcwd()+"/"+img_dir)
            imgPixScaled = imgPix.scaledToHeight(100)
            pic.setPixmap(imgPixScaled)
            self.resize(imgPixScaled.width(),imgPixScaled.height())
            lay.addWidget(pic)

class cardConf(QWidget):

    def _init_(self,*conf):
        super(cardConf, self)._init_()
        self.card = card
        self.conf = conf
        self.bar = QtGui.QProgressBar(self)
        self.bar.setGeometry(200,80,250,20)

    def cardBar(self):
        # Create Progress Bar
        bar.setValue(conf)

class App(QDialog):

    def __init__(self):
        super(App, self).__init__()
        self.title = 'Poker Pete Visualization'
        self.left = 200
        self.top = 200
        self.width = 500
        self.height = 500
        self.window = QtWidgets.QMainWindow()
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
        cardNames = [cList[0] for cList in cardList]
        layout.addWidget(cardImg())
        '''for item in range(self.numItems):
            card = self.card_list[item]
            imgArg = {"cardNum": card[0], "window":self.window}
            img = cardImg(imgArg)
            bar = cardConf(card[1])
            layout.addWidget(img,item,0)
            layout.addWidget(bar,item,1)
        '''
        self.horizontalGroupBox.setLayout(layout)

'''app = QApplication(sys.argv)
window = QtWidgets.QMainWindow()
window.setGeometry(0,0,400,200)
layout = QGridLayout()
'''


'''QProgressBar *proBar = new QProgressBar
    proBar.set
    layout.addWidget(QProgressBar(ccDict_fixed[card]))'''
#Debugging
#for k,v in ccDict.items():
#    print(k,v)
#for k,v in ccDict_fixed.items():
#    print(k,v)
#print(*cardList)
#print(*confList)
#print(results)
print(ccDict_fixed)
print(sorted_cc)





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
import numpy as np
import cv2
import imutils
import argparse

# Test load img in grayscale
img = cv2.imread('img/cards-[C0]-001.jpg',0)
scale_percent = 10
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

# Test opencv functions

# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

 # find contours in the thresholded image and initialize the
# shape detector
#cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#cnts = imutils.grab_contours(cnts)
#sd = ShapeDetector()
# 
cv2.imshow('image', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("pls")
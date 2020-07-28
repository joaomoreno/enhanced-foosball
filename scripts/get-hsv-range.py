#!/usr/bin/python3
# 2018.01.21 20:46:41 CST
import cv2

# Capturing video through webcam 
stream = cv2.VideoCapture('/Users/joao/Downloads/mixed.mp4')
_, img = stream.read()
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# red
# mask = cv2.inRange(hsv,(136, 87, 110), (180, 255, 255))

# blue
mask = cv2.inRange(hsv,(94, 80, 110), (120, 255, 255))

cv2.imshow("orange", mask);cv2.waitKey();cv2.destroyAllWindows()
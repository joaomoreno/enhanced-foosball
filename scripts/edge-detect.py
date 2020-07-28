# Python code for Multiple Color Detection 
# From https://www.geeksforgeeks.org/multiple-color-detection-in-real-time-using-python-opencv/

import numpy as np 
import cv2 
from timeit import default_timer as timer
from functools import reduce

# Capturing video through webcam 
# stream = cv2.VideoCapture('/Users/joao/Desktop/untitled.mov')
stream = cv2.VideoCapture('/Users/joao/Downloads/mixed.mp4')
# stream = cv2.VideoCapture(1)

cv2.namedWindow('stream', cv2.WND_PROP_FULLSCREEN)
cv2.resizeWindow('stream', 1200,700)
# cv2.setWindowProperty('stream', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def render(frame):
	# cv2.Canny(frame, threshold1, threshold2[, edges[, apertureSize[, L2gradient)
	edges = cv2.Canny(frame, 100, 200)
	return edges

# Start a while loop 
while(1):
	# Reading the video from the 
	# stream in image frames 
	_, frame = stream.read()

	start = timer()
	frame = render(frame)
	duration = timer() - start
	
	# Program Termination 
	cv2.imshow("stream", frame) 
	if cv2.waitKey(10) & 0xFF == ord('q'): 
		cap.release() 
		cv2.destroyAllWindows() 
		break

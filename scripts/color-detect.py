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
# cv2.resizeWindow('stream', 700,700)
cv2.setWindowProperty('stream', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def merge(a, b):
	xa, ya, wa, ha = a
	xb, yb, wb, hb = b
	return (min(xa, xb), ya, max(wa, wb), ha + hb)

def aggregate(rects):
	if len(rects) == 2:
		return rects
	
	gaps = list(y2 - (y1 + h) for (_, y1, _, h), (_, y2, _, _) in zip(rects, rects[1:]))
	index = gaps.index(max(gaps))
	return [reduce(merge, rects[0:index+1]), reduce(merge, rects[index+1:])]

def render(frame):
	redBoundary = ((50, 312), (170, 820))
	redFrame = frame[redBoundary[0][1]:redBoundary[1][1], redBoundary[0][0]:redBoundary[1][0]]
	cv2.rectangle(frame, (redBoundary[0][0], redBoundary[0][1]), (redBoundary[1][0], redBoundary[1][1]), (255, 255, 255), 1)
	redHsvFrame = cv2.cvtColor(redFrame, cv2.COLOR_BGR2HSV)

	blueBoundary = ((1650, 318), (1800, 796))
	blueFrame = frame[blueBoundary[0][1]:blueBoundary[1][1], blueBoundary[0][0]:blueBoundary[1][0]]
	cv2.rectangle(frame, (blueBoundary[0][0], blueBoundary[0][1]), (blueBoundary[1][0], blueBoundary[1][1]), (255, 255, 255), 1)
	blueHsvFrame = cv2.cvtColor(blueFrame, cv2.COLOR_BGR2HSV)

	# Set range for red color and define mask 
	# https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv
	red_lower1 = np.array([0, 135, 71], np.uint8) 
	red_upper1 = np.array([6, 255, 255], np.uint8) 
	red_lower2 = np.array([165, 195, 71], np.uint8) 
	red_upper2 = np.array([179, 255, 255], np.uint8) 
	red_mask = cv2.bitwise_or(cv2.inRange(redHsvFrame, red_lower1, red_upper1), cv2.inRange(redHsvFrame, red_lower2, red_upper2))
	
	# Set range for blue color and define mask 
	blue_lower = np.array([95, 135, 71], np.uint8) 
	blue_upper = np.array([114, 255, 255], np.uint8) 
	blue_mask = cv2.inRange(blueHsvFrame, blue_lower, blue_upper) 
	
	# Morphological Transform, Dilation 
	# for each color and bitwise_and operator 
	# between frame and mask determines 
	# to detect only that particular color 
	kernal = np.ones((5, 5), "uint8") 
	
	# For red color 
	red_mask = cv2.dilate(red_mask, kernal) 
	res_red = cv2.bitwise_and(redFrame, redFrame, mask = red_mask)

	# For blue color 
	blue_mask = cv2.dilate(blue_mask, kernal) 
	res_blue = cv2.bitwise_and(blueFrame, blueFrame, mask = blue_mask) 

	# Creating contour to track red color 
	contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	redRects = sorted((cv2.boundingRect(contour) for _, contour in enumerate(contours) if cv2.contourArea(contour) > 300), key = lambda r : r[1])

	# Creating contour to track blue color 
	contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	blueRects = sorted((cv2.boundingRect(contour) for _, contour in enumerate(contours) if cv2.contourArea(contour) > 300), key = lambda r : r[1])

	for x, y, w, h in redRects: 
		x += redBoundary[0][0]
		y += redBoundary[0][1]
		frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)

	for x, y, w, h in blueRects: 
		x += blueBoundary[0][0]
		y += blueBoundary[0][1]
		frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

	if len(redRects) < 2 or len(blueRects) < 2:
		print("skipping frame")
		return frame # skip frame
	
	redRects = aggregate(redRects)

	for x, y, w, h in redRects: 
		x += redBoundary[0][0]
		y += redBoundary[0][1]
		frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
	
	blueRects = aggregate(blueRects)

	for x, y, w, h in blueRects: 
		x += blueBoundary[0][0]
		y += blueBoundary[0][1]
		frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

	# https://keisan.casio.com/exec/system/1223508685
	red = round(0.018518518518519 * (redRects[1][3] - redRects[0][3]) + 5)
	blue = round(-0.018518518518519 * (blueRects[1][3] - blueRects[0][3]) + 5)
	cv2.putText(frame, str(red), (redBoundary[0][0], redBoundary[0][1]), cv2.FONT_HERSHEY_DUPLEX, 3.0, (255, 255, 255))    
	cv2.putText(frame, str(blue), (blueBoundary[0][0], blueBoundary[0][1]), cv2.FONT_HERSHEY_DUPLEX, 3.0, (255, 255, 255))
	return frame

# Start a while loop 
while(1):
	# Reading the video from the 
	# stream in image frames 
	_, frame = stream.read()

	start = timer()
	frame = render(frame)
	duration = timer() - start
	
	cv2.putText(frame, str(round(duration/1000.0, 2)), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255))
	
	# Program Termination 
	cv2.imshow("stream", frame) 
	if cv2.waitKey(10) & 0xFF == ord('q'): 
		cap.release() 
		cv2.destroyAllWindows() 
		break

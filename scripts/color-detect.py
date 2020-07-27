# Python code for Multiple Color Detection 
# From https://www.geeksforgeeks.org/multiple-color-detection-in-real-time-using-python-opencv/

import numpy as np 
import cv2 

# Capturing video through webcam 
stream = cv2.VideoCapture('C:\\Users\\jomo\\OneDrive\\Enhanced Foosball\\mixed.mp4')

# Start a while loop 
while(1):
	# Reading the video from the 
	# stream in image frames 
	_, imageFrame = stream.read()

	redBoundary = ((131, 332), (218, 770))
	redFrame = imageFrame[redBoundary[0][1]:redBoundary[1][1], redBoundary[0][0]:redBoundary[1][0]]
	redHsvFrame = cv2.cvtColor(redFrame, cv2.COLOR_BGR2HSV)

	blueBoundary = ((1733, 338), (1821, 746))
	blueFrame = imageFrame[blueBoundary[0][1]:blueBoundary[1][1], blueBoundary[0][0]:blueBoundary[1][0]]
	blueHsvFrame = cv2.cvtColor(blueFrame, cv2.COLOR_BGR2HSV)

	# Set range for red color and define mask 
	# https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv
	red_lower = np.array([136, 87, 110], np.uint8) 
	red_upper = np.array([180, 255, 255], np.uint8) 
	red_mask = cv2.inRange(redHsvFrame, red_lower, red_upper)

	# Set range for blue color and define mask 
	blue_lower = np.array([94, 80, 110], np.uint8) 
	blue_upper = np.array([120, 255, 255], np.uint8) 
	blue_mask = cv2.inRange(blueHsvFrame, blue_lower, blue_upper) 
	
	# Morphological Transform, Dilation 
	# for each color and bitwise_and operator 
	# between imageFrame and mask determines 
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
	rects = sorted((cv2.boundingRect(contour) for _, contour in enumerate(contours) if cv2.contourArea(contour) > 300), key = lambda r : r[1])

	if len(rects) != 2:
		print("skipping frame")
		continue # skip frame

	# https://keisan.casio.com/exec/system/1223508685
	red = round(0.018518518518519 * (rects[1][3] - rects[0][3]) + 5)

	for x, y, w, h in rects: 
		x += redBoundary[0][0]
		y += redBoundary[0][1]
		imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)

	# Creating contour to track blue color 
	contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	rects = sorted((cv2.boundingRect(contour) for _, contour in enumerate(contours) if cv2.contourArea(contour) > 300), key = lambda r : r[1])

	if len(rects) != 2:
		print("skipping frame")
		continue # skip frame

	blue = round(-0.018518518518519 * (rects[1][3] - rects[0][3]) + 5)

	for x, y, w, h in rects: 
		x += blueBoundary[0][0]
		y += blueBoundary[0][1]
		imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
	
	cv2.putText(imageFrame, str(red), (redBoundary[0][0], redBoundary[0][1]), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255))    
	cv2.putText(imageFrame, str(blue), (blueBoundary[0][0], blueBoundary[0][1]), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255))    
	
	# Program Termination 
	cv2.imshow("stream", imageFrame) 
	if cv2.waitKey(10) & 0xFF == ord('q'): 
		cap.release() 
		cv2.destroyAllWindows() 
		break

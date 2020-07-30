import numpy as np 
import cv2 

webcam = cv2.VideoCapture('C:\\Users\\jomo\\OneDrive\\Enhanced Foosball\\mixed.mp4') 

while(1): 
	
	_, inputFrame = webcam.read()

	h, _, _ = inputFrame.shape
	box = inputFrame[0:h, 0:400]

	lower = np.array([0, 0, 0], np.uint8) 
	upper = np.array([179, 98, 158], np.uint8) 
	mask = cv2.inRange(box, lower, upper)
	filtered = cv2.bitwise_and(box, box, mask = mask) 

	greyFrame = cv2.cvtColor(filtered,cv2.COLOR_BGR2GRAY)
	_, thresholdFrame = cv2.threshold(greyFrame, 20, 255, cv2.THRESH_BINARY)
	contours, hierarchy = cv2.findContours(thresholdFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	outputFrame = np.zeros(filtered.shape)
	cv2.drawContours(outputFrame, contours, -1, (0,255,0), 3)

	cv2.imshow("opencv", outputFrame) 
	if cv2.waitKey(10) & 0xFF == ord('q'): 
		webcam.release() 
		cv2.destroyAllWindows() 
		break

# Python code for Multiple Color Detection 
# From https://www.geeksforgeeks.org/multiple-color-detection-in-real-time-using-python-opencv/

import numpy as np 
import cv2 
import time
from functools import reduce
import requests
import threading, queue
from ringbuffer import RingBuffer
import datetime
import uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings
import random

class Narrator:
  def __init__(self):
    self.red = 0
    self.blue = 0
  
  def goal(self, red, blue):
    wasEqual = self.red == self.blue

    scorer = 'red' if red > self.red else 'blue'
    sufferer = 'blue' if red > self.red else 'red'
    scorerScore = red if red > self.red else blue
    suffererScore = blue if red > self.red else red

    self.red = red
    self.blue = blue

    if red == 7 or blue == 7:
      return random.choice([
        'END!',
        'gg',
      ])

    elif red == 0 and blue == 0:
      return random.choice([
        'gl hf',
        'Ready, set, go! 🔫 ',
        'Zero goals yet, better start hitting the ⚽!',
        'Good luck and fair play!'
      ])
    
    elif red == 6 and blue == 6:
      return random.choice([
        'Head to head on the last mile. 🏁 ',
        'Team %s equalizes, and this match goes for golden goal! ' % (scorer),
        'Strap yourselves in, we are going for final goal rush! ',
        'As they say in hockey: Sudden death is on! ',
        'High noon 🤠! ',
        'Sing along: It’s the final countdown – tadadadaa dadadida… '
      ])
    
    elif red == blue:
      return random.choice([
        'Reset! Both are %d goals away from the win!' % (7 - red),
        'Team %s just caught up by equalizing.' % (scorer),
        'This makes this a draw: The stands are in suspense!'
      ])
    
    elif red == 6 or blue == 6:
      winning = 'red' if red == 6 else 'blue'
      losing = 'blue' if red == 6 else 'red'
      return random.choice([
        'Goal! - Last chance for %s: Step it up! ' % (losing),
        'Oh, this pushes %s to the brink of defeat. Can they save themselves? ' % (losing),
        'Nearly there %s: Finish them! ' % (winning)
      ])

    elif wasEqual:
      return random.choice([
        '%s takes the lead! Gogo-goal! ' % (scorer),
        'Goal! Team %s is stepping it up.'  % (scorer),
        'Surprise - %s is one up already! ' % (scorer),
        'Watch out %s, don\'t let them get away!' % (sufferer)
      ])

    else:
      return random.choice([
        'Hello goalkeeper? Ball just passed by you!',
        'What a shot 🙀 - and it lands in the net!',
        'Congrats %s striker: This is a contender for goal of the week! 🏆 ' % (scorer),
        'Awesome shot! ✨ ',
        'You got this team %s: Push on!' % (scorer),
        'Goooooooooooooooooooooooal!',
        'Bot says: Foosball is best ball game.',
        'Team %s: score = score + 1' % (scorer),
        'Team %s: score++' % (scorer),
        'Team %s: score += 1' % (scorer)
      ])

live = True
# live = False

# Capturing video through webcam 

if live:
	stream = cv2.VideoCapture(1)
	# stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	# stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
	# stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'));
	# stream.set(cv2.CAP_PROP_FPS, 60)
else:
	stream = cv2.VideoCapture('raw/output.mp4')

cv2.namedWindow('live', cv2.WND_PROP_FULLSCREEN)
cv2.resizeWindow('live', 1200,700)
# cv2.setWindowProperty('live',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

# cv2.namedWindow('live', cv2.WND_PROP_FULLSCREEN)
# cv2.resizeWindow('processed', 1200,700)

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

teamsQueue = queue.Queue()

def teamsWorker():
	id = None
	while True:
		red, blue, url = teamsQueue.get()
		score = '%d - %d' % (red, blue)

		if id is None or (red == 0 and blue == 0):
			r = requests.post('https://foosbot-as.azurewebsites.net/api/game/start', json = {
				'Title': 'RED vs BLUE',
				'Score': score,
				'Message': 'Foosball'
			})
			id = r.text
		
		if red != 0 or blue != 0:
			requests.post('https://foosbot-as.azurewebsites.net/api/game/update', json = {
				'ConversationId': id,
				'Title': 'RED vs BLUE',
				'Score': score,
				'Message': 'Foosball',
				'Replay': url
			})
		
		if red == 7 or blue == 7:
			requests.post('https://foosbot-as.azurewebsites.net/api/game/update', json = {
				'ConversationId': id,
				'Title': 'Some team wins',
				'Score': score,
				'Message': 'Game over, congrats team!'
			})
		
		teamsQueue.task_done()

threading.Thread(target=teamsWorker, daemon=True).start()

recordingsQueue = queue.Queue()
fourcc = cv2.VideoWriter_fourcc(*'avc1')

def recordingWorker():
	blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=foosballmediaservices;AccountKey=KEY;EndpointSuffix=core.windows.net')

	id = None
	count = 0
	while True:
		(red, blue, iterator) = recordingsQueue.get()
		
		id = str(uuid.uuid4())
		filename = '%s.mp4' % id
		count += 1
		out = None

		frames = list(iterator)
		duration = frames[-1][0] - frames[0][0]
		fps = len(frames) / duration

		for _, frame in frames:
			frame = cv2.resize(frame, None, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
			if out is None:
				height, width, _ = frame.shape
				out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
			out.write(frame)

		out.release()
		out = None

		blob = blob_service_client.get_blob_client(container='recordings', blob=filename)
		with open(filename, "rb") as data:
			blob.upload_blob(data, content_settings = ContentSettings(content_type='video/mp4'))

		print('uploaded', blob.url)
		teamsQueue.put((red, blue, blob.url))
		recordingsQueue.task_done()

threading.Thread(target=recordingWorker, daemon=True).start()

class Game:
	def __init__(self, buffer):
		self.buffer = buffer
		self.started = False
		self.red = None
		self.blue = None
		self.nextRed = None
		self.nextBlue = None
		self.nextCount = 0
	
	def update(self, red, blue):
		if red == self.red and blue == self.blue:
			return
		
		if red == self.nextRed and blue == self.nextBlue:
			if self.nextCount < 30:
				self.nextCount += 1
			else:
				self.nextRed = None
				self.nextBlue = None
				self.setScore(red, blue)
		else:
			self.nextRed = red
			self.nextBlue = blue
			self.nextCount = 0
		
	def setScore(self, red, blue):
		self.red = red
		self.blue = blue

		if red == 0 and blue == 0:
			self.started = True
		
		if not self.started:
			print('reset to 0 - 0 to start the game')
			return

		print('%d - %d' % (red, blue))
		if self.buffer.isFull():
			recordingsQueue.put((red, blue, self.buffer.__iter__()))
		
		if red == 7 or blue == 7:
			self.started = False

redBoundary = ((140, 212), (220, 920))
blueBoundary = ((1630, 218), (1740, 896))

def process(game, frame, draw = True):
	redFrame = frame[redBoundary[0][1]:redBoundary[1][1], redBoundary[0][0]:redBoundary[1][0]]
	redHsvFrame = cv2.cvtColor(redFrame, cv2.COLOR_BGR2HSV)

	blueFrame = frame[blueBoundary[0][1]:blueBoundary[1][1], blueBoundary[0][0]:blueBoundary[1][0]]
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

	if draw:
		for x, y, w, h in redRects: 
			x += redBoundary[0][0]
			y += redBoundary[0][1]
			frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)

		for x, y, w, h in blueRects: 
			x += blueBoundary[0][0]
			y += blueBoundary[0][1]
			frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

	if len(redRects) < 2 or len(blueRects) < 2:
		# print("skipping frame")
		return frame # skip frame
	
	redRects = aggregate(redRects)

	if draw:
		for x, y, w, h in redRects: 
			x += redBoundary[0][0]
			y += redBoundary[0][1]
			frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
	
	blueRects = aggregate(blueRects)

	if draw:
		for x, y, w, h in blueRects: 
			x += blueBoundary[0][0]
			y += blueBoundary[0][1]
			frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

	# https://keisan.casio.com/exec/system/1223508685
	red = round(0.018518518518519 * (redRects[1][3] - redRects[0][3]) + 5)
	blue = round(-0.018518518518519 * (blueRects[1][3] - blueRects[0][3]) + 5)

	if red > 7 or blue > 7:
		return frame

	game.update(red, blue)

	return frame

framesQueue = queue.Queue(maxsize = 1)

def detectionWorker(game, draw):
	while True:
		frame = framesQueue.get()
		frame = process(game, frame, draw)
		framesQueue.task_done()

# delays = []
#debug = True
debug = False

def main():
	buffer = RingBuffer(150) # 30 fps * 5 seconds
	game = Game(buffer)
	then = None
	shape = None

	threading.Thread(target=detectionWorker, args=[game, False], daemon=True).start()

	while(1):
		# Reading the video from the 
		# stream in image frames 
		_, frame = stream.read()

		if shape is None:
			shape = frame.shape

		try:
			framesQueue.put(frame, False)
		except:
			pass

		now = time.time()

		# logic
		if debug:
			frame = process(game, frame)
		else:
			buffer.push((now, frame))
		
		# measure

		# if then is not None:
		# 	delay = round((now - then) * 1000)
		# 	delays.append(delay)
		# 	print(delay, round(1000.0/delay))
		# 	# cv2.putText(frame, str(delay), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255))
		# then = now
		# if len(delays) > 0:
		# 	print(round(1000.0/ (sum(delays)/len(delays))))

		#	draw
		cv2.putText(frame, str(game.red), (redBoundary[0][0], redBoundary[0][1]), cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 3)    
		cv2.putText(frame, str(game.blue), (blueBoundary[0][0], blueBoundary[0][1]), cv2.FONT_HERSHEY_PLAIN, 6, (255, 255, 255), 3)

		# footer
		cv2.rectangle(frame, (0, shape[0] - 100), (shape[1], shape[0]), (0, 0, 0), -1)
		cv2.putText(frame, 'LIVE', (50, shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)
		
		cv2.imshow('live', frame)

		if cv2.waitKey(10) & 0xFF == ord('q'): 
			stream.release() 
			cv2.destroyAllWindows() 
			break

if __name__ == '__main__':
	main()
import numpy as np
import cv2

cap = cv2.VideoCapture(1)

fourcc = cv2.VideoWriter_fourcc(*'avc1')
out = None

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        # frame = cv2.resize(frame, None, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
        if out is None:
            height, width, _ = frame.shape
            out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (width, height))
        
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
 
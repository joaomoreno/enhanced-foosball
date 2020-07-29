import numpy as np
import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = None

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:

        if out is None:
            print(frame.shape)
            height, width, _ = frame.shape
            out = cv2.VideoWriter('output.mov', fourcc, 20.0, (width, height))
        
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

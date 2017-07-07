# Code isn't encrypted , feel free to copy from it, if it's gonna help you :).

from collections import deque
from dollar import *
import cv2
import numpy as np
import argparse

cap = cv2.VideoCapture(0)
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# pts is an array that holds laser points ( sequence )
pts = deque(maxlen=args["buffer"])
while (1):
    # Making sure every point is non  zero,zero
    if not all(pts):
        pts = deque(maxlen=args["buffer"])
    # Take each frame
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 0, 255])
    upper_red = np.array([255, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
    # maxLoc represents laser point at a frame
    pts.appendleft(maxLoc)
    for i in xrange(1, len(pts)):
        # Drawing connected line
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 0), 2)
    # Please check dollar.py for more clarification about recognize
    Name, Score = recognize(pts, templates)
    cv2.putText(frame, "(" + Name + " " + "%.2f" % Score + ")", (20, 50), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), 1)
    cv2.imshow('Draw Shapes', frame)
    cv2.imshow('frame', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()

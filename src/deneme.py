import cv2
import time

while True:
    cap = cv2.VideoCapture(0)
    s, img = cap.read()
    if s:
        cv2.imshow("test", img)
        cv2.waitKey(1)
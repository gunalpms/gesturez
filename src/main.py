import cv2
import mediapipe as mp
import time
import Tracker

ptime = 0
ctime = 0
cap = cv2.VideoCapture(0)

model = Tracker.handDetector()

while True:
    success, img = cap.read()
    img = model.findHands(img)
    landmarksList = model.findPosition(img)
    if len(landmarksList) != 0:
        print(landmarksList[4])

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (30, 80), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255) , 4)
    cv2.imshow("test", img)
    cv2.waitKey(1)
import cv2
import tracker
import math
import asyncio
from actions import *
import rateLimiter

# initialization

limiter = rateLimiter.rateLimiter(5, 1.0)
limiter2 = rateLimiter.rateLimiter(1, 2.0)


widthCam, heightCam = 640, 480
# see camera sources in windows settings
# use 0 if you have only one camera9
cap = cv2.VideoCapture(0)
# it is not advised to change the values of the camera dimensions as the gesture detection model
# relies on algorithms designed around these values. 
cap.set(3, widthCam)
cap.set(4, heightCam)

# if the model has difficulties registering your hand, try lowering the trackCon value 
model = tracker.handDetector(detectionCon=0.5, trackCon=0.9)

async def main():

    while True:
        s, img = cap.read()
        im = model.findHands(img)
        landmarkList = model.findPosition(im)

        if len(landmarkList) != 0:

            # for finger indices: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
            thumb_x, thumb_y = landmarkList[4][1], landmarkList[4][2]
            index_x, index_y = landmarkList[8][1], landmarkList[8][2]
            middle_x, middle_y = landmarkList[12][1], landmarkList[12][2]
            ring_x, ring_y = landmarkList[16][1], landmarkList[16][2]

            # displays a line between landmarks for debugging
            cv2.line(im, (index_x, index_y), (thumb_x, thumb_y), (0, 255, 0), 3)
            cv2.line(im, (middle_x, middle_y), (thumb_x, thumb_y), (255, 0 , 255), 3)
            
            # these are to check the relative positions of the fingers to prevent false actions
            index_to_thumb_is_horizontal = False
            middle_to_thumb_is_horizontal = False
            index_middle_ring_is_horizontal = False
            
            index_to_thumb = math.hypot(index_x - thumb_x, index_y - thumb_y)
            middle_to_thumb = math.hypot(middle_x - thumb_x, middle_y - thumb_y)

            # an algorithm to check the relative positions of landmarks to determine if
            # an action should be taken or not. 

            # https://www.desmos.com/calculator/g4ckkpoits        
            
            if (abs((index_y - thumb_y))/abs(((index_x - thumb_x)+0.001)) < 
                0.2):
                index_to_thumb_is_horizontal = True

            if (abs((middle_y - thumb_y))/(abs((middle_x - thumb_x)+0.001)) < 
                0.4):
                middle_to_thumb_is_horizontal = True
            
            # checking the horizontality of the three main fingers. 
            if ((abs(max(index_y, middle_y, ring_y))-min(index_y, middle_y, ring_y)) < 30
                and (abs(max(index_x, middle_x, ring_x))-min(index_x, middle_x, ring_x)) > 45):
                index_middle_ring_is_horizontal = True

            # calling actions

            if (index_to_thumb < 65 and index_to_thumb_is_horizontal and not middle_to_thumb_is_horizontal):
                async with limiter:
                    await volumeDown()

            if (index_to_thumb > 200 and index_to_thumb_is_horizontal and not middle_to_thumb_is_horizontal):
                async with limiter:
                    await volumeUp()

            if (middle_to_thumb < 65 and middle_to_thumb_is_horizontal):
                async with limiter:
                    await brightnessDown()

            if (middle_to_thumb > 120 and middle_to_thumb_is_horizontal):
                async with limiter:
                    await brightnessUp()
            
            if (index_middle_ring_is_horizontal and not index_to_thumb_is_horizontal 
            and not middle_to_thumb_is_horizontal):
                async with limiter2:
                    await altTab()

            # for debugging
            # a = (str(index_to_thumb) + "\t" + str(index_to_thumb_is_horizontal))
            # b = str(abs(index_x-middle_x))
            # print(str(middle_to_thumb) + "\t" + str(middle_to_thumb_is_horizontal) + "\t" + a + "\t" + b + "\t" + str(index_middle_ring_is_horizontal))

            # print(str(middle_to_thumb_is_horizontal) + "\t" + str(middle_to_thumb))

        cv2.imshow("test", img)
        cv2.waitKey(1)

asyncio.run(main())
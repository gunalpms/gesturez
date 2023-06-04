import cv2
import mediapipe as mp

class handDetector():
    def __init__(self, mode=False, maxHands=1, modelComplexity = 1, detectionCon=0.5, trackCon=0.5):
        # instance variables
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # initializing hand detection and tracking module
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity,
                                        self.detectionCon, self.trackCon)
        # initializing drawing utils
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # adding found landmarks to the results variable - available for the instance
        self.results = self.hands.process(imgRGB)

        # the results var is None for any frame that does not contain any hands
        # this draws the hands with connections - for debugging
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    # calculating the position of each landmark and returning an array for each landmark and their positions
    # where the positions are returned as x and y coordinates within the capture. the capture height and width
    # are determined in the main runner, but it is advised not to touch it unless absolutely necessary
    def findPosition(self, img, handNo=0, draw=False):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h) # normally a coordinate between 0 and 1 is returned
                lmList.append([id, cx, cy])
                # drawing for debugging
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList

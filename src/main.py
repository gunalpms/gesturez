import cv2
import mediapipe as mp
import time 

cap = cv2.VideoCapture(0)

handModel = mp.solutions.hands

hands = handModel.Hands()

draw = mp.solutions.drawing_utils

ct = 0
pt = 0

while True:

    s, im = cap.read()

    imrgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    res = hands.process(imrgb)

    # print(res.multi_hand_landmarks)

    if res.multi_hand_landmarks:
        for hl in res.multi_hand_landmarks:
            xlist = []
            ylist = []
           
            for i, mark in enumerate(hl.landmark):
                
                h, w, c = im.shape
                xc, yc = int(mark.x*w), int(mark.y*h)
                # print(str(i) + "    " + str(xc) + "     " + str(yc))

                xlist.append(xc)
                ylist.append(yc)
            print("XLIST")
            print(xlist[8])
            print("YLIST")
            print(ylist[8])
         
        draw.draw_landmarks(im, hl)

    ct = time.time()
    fps = 1 / (ct-pt)
    pt = ct

    cv2.putText(im, str(int(fps)), (10, 70), 
    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    


    cv2.imshow("Image", im)
    cv2.waitKey(1)





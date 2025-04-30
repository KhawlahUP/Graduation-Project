import cv2
from HandTrackingModule import HandDetector
import time

ACTIONS = {"All Leds On":[[1,1,1,1,1],[1,1,1,1,1]],
           "All Leds Off":[[0,0,0,0,0],[0,0,0,0,0]],
           "Led 1 On":[[1,1,1,1,1],[]],
           "Led 2 On":[[],[1,1,1,1,1]],
           "Led 1 Off":[[0,0,0,0,0],[]],
           "Led 2 Off":[[],[0,0,0,0,0]],
           "Fan On":[[],[0,1,1,0,0]],
           "Fan Off":[[],[0,1,0,0,0]]
           }


detector=HandDetector(detectionCon=0.8,maxHands=2,glasses=True)
video=cv2.VideoCapture(0)
f_type = 0
c_type = 0
start_time = time.time()

color  = (255,255,255) 
action = ""
while True:
    ret,frame=video.read()
    frame = cv2.resize(frame,(640,480))
    if not ret:
        break
    hands,handsType,img=detector.findHands(frame)
    if hands:
        if len(hands)==2:
            lmList1=hands[0]
            lmList2=hands[1]
            fingerUp1=detector.fingersUp(lmList1)
            fingerUp2=detector.fingersUp(lmList2)
            f_type = [fingerUp1,fingerUp2]
        else:
            lmList=hands[0]
            fingerUp=detector.fingersUp(lmList)
            if handsType[0] == "Right":
                f_type = [fingerUp,[]]
            else:
                f_type = [[],fingerUp]
        # print(f_type)
        if f_type == c_type:
            elapsed_time = time.time() - start_time
            if elapsed_time >=1:
                try:
                    action = "Current action: " + next(key for key, value in ACTIONS.items() if value == f_type)
                except StopIteration:
                    continue
        else:
            start_time = time.time()
            c_type = f_type
    if "on" in action.lower():
        color = (0,255,0)
    if "off" in action.lower():
        color = (0,0,255)
    cv2.putText(frame,action,(0,50),cv2.FONT_HERSHEY_COMPLEX,1,color,1,cv2.LINE_AA)
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
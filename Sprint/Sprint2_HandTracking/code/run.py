import cv2
from HandTrackingModule import HandDetector
import time

detector=HandDetector(detectionCon=0.8,maxHands=2,glasses=True)
video=cv2.VideoCapture(0)
f_count = 0
h_count = 0
start_time = time.time()
while True:
    ret,frame=video.read()
    frame = cv2.resize(frame,(640,480))
    if not ret:
        break
    hands,img=detector.findHands(frame)
    if hands:
        cv2.putText(frame,f'Hands count:{len(hands)}',(20,40),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1,cv2.LINE_AA)
        if len(hands)==2:
            lmList1=hands[0]
            lmList2=hands[1]
            fingerUp1=detector.fingersUp(lmList1)
            fingerUp2=detector.fingersUp(lmList2)
            f_count = fingerUp1.count(1) + fingerUp2.count(1)
            if f_count == h_count:
                elapsed_time = time.time() - start_time
                if elapsed_time >=1:
                    if f_count == 1:
                        cv2.putText(frame,f'Led 1 is on',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1,cv2.LINE_AA)
                    if f_count == 2:
                        cv2.putText(frame,f'Led 2 is on',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1,cv2.LINE_AA)
                    
                    cv2.putText(frame,f'Finger count: {f_count}',(20,460),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1,cv2.LINE_AA)
                else:
                    cv2.putText(frame,f'Finger count: {h_count}',(20,460),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1,cv2.LINE_AA)
            else:
                start_time = time.time()
                h_count = f_count
        else:
            lmList=hands[0]
            fingerUp=detector.fingersUp(lmList)
            f_count = fingerUp.count(1)
            if f_count == h_count:
                elapsed_time = time.time() - start_time
                if elapsed_time >=1:
                    if f_count == 0:
                        cv2.putText(frame,f'Leds are off',(200,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv2.LINE_AA)
                    if f_count == 5:
                        cv2.putText(frame,f'Leds are on',(200,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1,cv2.LINE_AA)
                    cv2.putText(frame,f'Finger count: {f_count}',(20,460),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1,cv2.LINE_AA)
                else:
                    cv2.putText(frame,f'Finger count: {h_count}',(20,460),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1,cv2.LINE_AA)
            else:
                start_time = time.time()
                h_count = f_count
    cv2.imshow("frame",frame)
    # print(f_count)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
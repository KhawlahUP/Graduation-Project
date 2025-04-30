import math
import cv2
import mediapipe as mp


class HandDetector:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """
    glasses: bool
    def __init__(self, staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5,glasses=True):

        """
        :param mode: In static mode, detection is done on each image: slower
        :param maxHands: Maximum number of hands to detect
        :param modelComplexity: Complexity of the hand landmark model: 0 or 1.
        :param detectionCon: Minimum Detection Confidence Threshold
        :param minTrackCon: Minimum Tracking Confidence Threshold
        """
        self.staticMode = staticMode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.staticMode,
                                        max_num_hands=self.maxHands,
                                        model_complexity=modelComplexity,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)

        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []
        self.glasses = glasses
    def is_back_faced(self,hand_landmarks, hand_type):
        """
        Determines if the hand is back-faced or front-faced based on thumb and pinky tip positions.

        :param hand_landmarks: NormalizedLandmarkList object containing landmarks for the hand.
        :param hand_type: Type of the hand ("Left" or "Right").
        :return: True if the hand is back-faced, False if front-faced.
        """
        thumb_tip_index = 4
        pinky_tip_index = 20

        thumb_tip_x = hand_landmarks.landmark[thumb_tip_index].x
        pinky_tip_x = hand_landmarks.landmark[pinky_tip_index].x
        if hand_type.classification[0].label == "Left":
            return thumb_tip_x < pinky_tip_x
        elif hand_type.classification[0].label == "Right":
            return thumb_tip_x > pinky_tip_x
        else:
            raise ValueError("Invalid hand type. Use 'Left' or 'Right'.")


    def findHands(self, img, draw=True, flipType=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                ## lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                ## bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)


                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                    
                if self.glasses:
                    # Assuming hand_landmarks is a list of landmarks and hand_type is obtained from MULTI_HANDEDNESS
                    is_back = self.is_back_faced(handLms, handType)
                    print((boxW+boxH)*2)
                    is_close = (boxW+boxH)*2 >=900
                    if is_back and is_close:
                        allHands.append(myHand)
                    ## draw
                    if draw and is_back:
                        self.mpDraw.draw_landmarks(img, handLms,
                                                self.mpHands.HAND_CONNECTIONS)
                        cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                    (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                    (255, 0, 255), 2)
                        cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 0, 255), 2)
                else:
                    allHands.append(myHand)
                    ## draw
                    if draw:
                        self.mpDraw.draw_landmarks(img, handLms,
                                                self.mpHands.HAND_CONNECTIONS)
                        cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                    (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                    (255, 0, 255), 2)
                        cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 0, 255), 2)
                        
        return allHands, img

    def fingersUp(self, myHand):
        """
        Finds how many fingers are open and returns in a list.
        Considers left and right hands separately
        :return: List of which fingers are up
        """
        fingers = []
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            # Thumb
            if not self.glasses:
                if myHandType == "Right":
                    if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                # 4 Fingers
                for id in range(1, 5):
                    if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            else: # when the camera is on the glasses, the hand tracking pose must be flipped backwards
                if myHandType == "Right":
                    if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                # 4 Fingers
                for id in range(1, 5):
                    if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img=None, color=(255, 0, 255), scale=5):
        """
        Find the distance between two landmarks input should be (x1,y1) (x2,y2)
        :param p1: Point1 (x1,y1)
        :param p2: Point2 (x2,y2)
        :param img: Image to draw output on. If no image input output img is None
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """

        x1, y1 = p1
        x2, y2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), scale, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), scale, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, max(1, scale // 3))
            cv2.circle(img, (cx, cy), scale, color, cv2.FILLED)

        return length, info, img




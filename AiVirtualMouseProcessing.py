import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy 
import pyautogui
from settings import wCam, hCam, frameR, smoothening, press_length

class AiVirtualMouse:
    def __init__(self) -> None:
        self.plocX = 0
        self.plocY = 0
        self.clocX = 0
        self.clocY = 0
        self.pTime = 0
        self.cTime = 0
        self.x1, self.y1, self.x2, self.y2 = None, None, None, None
        self.pinky = None

        self.cap = cv2.VideoCapture(1)
        self.cap.set(3, wCam)
        self.cap.set(4, hCam)
        self.img = self.cap.read()
        self.detector = htm.handDetector(maxHands=1)
        self.fingers = []
        self.lmList = []
        self.is_pressed = False
        self.is_dragged = False
        self.drag_time = 0
        
        self.wScr, self.hScr = autopy.screen.size()
        self.fps = None


    def FindFingers(self):
        # 1. Find hand Landmarks
        _, self.img = self.cap.read()
        self.img = self.detector.findHands(self.img)
        self.lmList, _ = self.detector.findPosition(self.img)
        # 2. Get the tip of the index and middle fingers
        if len(self.lmList) != 0:
            self.x1, self.y1 = self.lmList[8][1:]
            self.x2, self.y2 = self.lmList[12][1:]
            self.pinky = self.lmList[20][1:]
            
            # print(x1, y1, x2, y2)

    def CheckFingers(self):
        # 3. Check which fingers are up
        self.fingers = self.detector.fingersUp()
        # print(fingers)
        cv2.rectangle(self.img, (frameR, frameR), (wCam - frameR, hCam - frameR),
        (255, 0, 255), 2)


    # 4. Only Index Finger : Moving Mode
    def Moving(self):
        # 5. Convert Coordinates
        x3 = np.interp(self.x1, (frameR, wCam - frameR), (0, self.wScr))
        y3 = np.interp(self.y1, (frameR, hCam - frameR), (0, self.hScr))
        # 6. Smoothen Values
        self.clocX = self.plocX + (x3 - self.plocX) / smoothening
        self.clocY = self.plocY + (y3 - self.plocY) / smoothening

        # 7. Move Mouse
        autopy.mouse.move(self.wScr - self.clocX, self.clocY)
        cv2.circle(self.img, (self.x1, self.y1), 15, (255, 0, 255), cv2.FILLED)
        self.plocX, self.plocY = self.clocX, self.clocY


    # 8. Both Index and middle fingers are up : Clicking Mode
    def Clicking(self):
        # 9. Find distance between fingers
        length, self.img, lineInfo = self.detector.findDistance(8, 12, self.img)
        # print(length)
        
        if self.is_dragged:
            self.Moving()
            
        # 10. Click mouse if distance short
        if length < press_length and not self.is_pressed:
            cv2.circle(self.img, (lineInfo[4], lineInfo[5]),
            15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click()
            self.drag_time = time.time()
            
        elif length < press_length and self.is_pressed and not self.is_dragged and time.time() - self.drag_time > 1:
            self.is_dragged = True
            if self.is_dragged:
                pyautogui.mouseDown()
                
        self.is_pressed = length < press_length


    def RightClicking(self):
        length, self.img, lineInfo = self.detector.findDistance(8, 12, self.img)
        if length < press_length and not self.is_pressed:
            cv2.circle(self.img, (lineInfo[4], lineInfo[5]),
            15, (0, 255, 0), cv2.FILLED)
            autopy.mouse.click(autopy.mouse.Button.RIGHT)


    def Scrooll(self):
        if self.pinky[1] > hCam / 2:
            pyautogui.scroll(-50)
        else:
            pyautogui.scroll(50)


    def FrameCalculating(self):
        # 11. Frame Rate
        self.cTime = time.time()
        self.fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime
        cv2.putText(self.img, str(int(self.fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.putText(self.img, str(self.is_pressed), (100, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3 )
        cv2.putText(self.img, str(self.is_dragged), (230, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3 )


    def Run(self):
        while True:
            self.FindFingers()
            self.CheckFingers()
            
            if self.fingers[1] == 1 and self.fingers[2] == 0:
                self.Moving()
                self.is_pressed = False
            
            if self.fingers[4] == 1 and self.fingers[1] == 1 and self.fingers[2] == 1:
                self.RightClicking()
            elif self.fingers[1] == 1 and self.fingers[2] == 1:
                self.Clicking()
            elif self.fingers[4] == 1 and self.fingers[1] == 0:
                self.Scrooll()

            
            if self.is_dragged and not self.is_pressed:
                self.is_dragged = False
                pyautogui.mouseUp()
                
            self.FrameCalculating()
            # 12. Display
            cv2.imshow("Image", self.img)
            cv2.waitKey(1)
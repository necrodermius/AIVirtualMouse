import cv2
import numpy as np
import HandTrackingModule as htm
import AiVirtualMouseProcessing as avmp
import time
import autopy 
import pyautogui
from settings import wCam, hCam, frameR, smoothening


plocX, plocY = 0, 0
clocX, clocY = 0, 0
pTime = 0

cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

is_pressed = False
detector = htm.handDetector()

while True:
    img, x1, y1, x2, y2 = avmp.FindFingers(cap, detector)
    fingers = avmp.CheckFingers(img, detector)
    if fingers[1] == 1 and fingers[2] == 0:
        plocX, plocY, clocX, clocY = avmp.Moving(img, x1, y1, wScr, hScr, plocX, plocY)
    if fingers[1] == 1 and fingers[2] == 1:
        is_pressed = avmp.Clicking(img, detector, is_pressed)
    
    pTime = avmp.FrameCalculating(img, pTime)
    
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
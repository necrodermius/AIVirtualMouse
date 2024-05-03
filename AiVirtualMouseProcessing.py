import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy 
import pyautogui
from settings import wCam, hCam, frameR, smoothening


def FindFingers(cap, detector):
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)
        return (img, x1, y1, x2, y2)
    return (img, None, None, None, None)


def CheckFingers(img, detector):
    # 3. Check which fingers are up
    fingers = detector.fingersUp()
    # print(fingers)
    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
    (255, 0, 255), 2)
    return fingers


# 4. Only Index Finger : Moving Mode
def Moving(img, x1, y1, wScr, hScr, plocX, plocY):
    # 5. Convert Coordinates
    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
    # 6. Smoothen Values
    clocX = plocX + (x3 - plocX) / smoothening
    clocY = plocY + (y3 - plocY) / smoothening

    # 7. Move Mouse
    autopy.mouse.move(wScr - clocX, clocY)
    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
    plocX, plocY = clocX, clocY
    return plocX, plocY, clocX, clocY

# 8. Both Index and middle fingers are up : Clicking Mode
def Clicking(img, detector, is_pressed):
    # 9. Find distance between fingers
    length, img, lineInfo = detector.findDistance(8, 12, img)
    print(length)
    # 10. Click mouse if distance short
    if length < 30 and not is_pressed:
        cv2.circle(img, (lineInfo[4], lineInfo[5]),
        15, (0, 255, 0), cv2.FILLED)
        autopy.mouse.click()
    is_pressed = length < 30
    return is_pressed

def FrameCalculating(img, pTime):
    # 11. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    return cTime
import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)

cx, cy, w, h = 100, 100, 200, 200
cz=0


class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # If the index finger tip is in the rectangle region
        if cx - w // 2 < cursor[0] < cx + w // 2 and \
                cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor


rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands,img3= detector.findHands(img)
    if hands:
        lmList = hands[0]["lmList"]
        l, _, img2 = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        if l < 70:
            cursor = lmList[8][0:2]  # index finger tip landmark
            # call the update here
            for rect in rectList:
                rect.update(cursor)

    ## Draw Transperency
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                      (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Image", out)
    cv2.waitKey(1)
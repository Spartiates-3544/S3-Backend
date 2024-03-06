import cv2
from qreader import QReader

cap = cv2.VideoCapture(0)
qreader = QReader()

#if not cap.isOpened():
#    raise IOError("Cannot open webcam")

def detect():
    while True:
        _, img = cap.read()
        data = qreader.detect_and_decode(image=img, return_detections=False)
        cv2.imshow('QR Code Scanner', img)
        cv2.waitKey(1)
        if data and data != (None,):
            break

    dataStr = data[0]
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    return dataStr

def detect(img):
    while True:
        # _, img = cap.read()
        data = qreader.detect_and_decode(image=img, return_detections=False)
        cv2.imshow('QR Code Scanner', img)
        cv2.waitKey(1)
        if data and data != (None,):
            break

    dataStr = data[0]
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    return dataStr
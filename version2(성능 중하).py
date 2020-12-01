import cv2
from matplotlib import pyplot as plt
import skimage.measure
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import requests

url=['http://127.0.0.1:8080/a','http://127.0.0.1:8080/w','http://127.0.0.1:8080/d','http://127.0.0.1:8080/s']
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

capture=cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,128)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,80)
time.sleep(0.1)
while True:
    _, frame=capture.read()
    img = np.array(frame)
    #cv2.imshow("Frame", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
   

    #img = rescale_frame(img, 10)
    # BGR -> HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    _, _, img = cv2.split(hsv)
    # cv2.imshow("1", img)


    # MORPH_GRADIENT
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    img = cv2.morphologyEx(img,cv2.MORPH_GRADIENT, k)

    # Thresold
    _, img = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)


    # Pooling
    w, h = int(img.shape[1] / 8) , int(img.shape[0] / 4)
    img = skimage.measure.block_reduce(img, (h,w), np.mean)
    #cv2.imshow("2", img)

    #go?
    left = 0
    front = 0
    right = 0
    back = 0
    l_t = 0
    f_t = 0
    r_t = 0

    ld = 1
    rd = 1
    # 4 * 8
    for i in range(4):
        left += img[i][0]
        for j in range(1, 7):
            front += img[i][j]
        right += img[i][7]

    if left != 0 and right != 0:
        left = 0
        front = 1
        right = 0
    elif left != 0 and right == 0:
        left = 1
        front = 0
        right = 0
    elif left == 0 and right != 0:
        left = 0
        front = 0
        right = 1
    elif left == 0 and right == 0 and front != 0:
        left = 0
        front = 1
        right = 0
    else:
        left = 0
        front = 0
        right = 0






    d = max(left, front, right)
    if d==0:
        #print('back')
        requests.get(url[3])
    else:    
        left /= d
        front /= d
        right /= d
        list=[left,front,right]
        #print(["l", "f", "r"][list.index(max(list))],list)
        requests.get(url[list.index(max(list))])
        #print(list.index(max(list)))
    #print(left, front, right)

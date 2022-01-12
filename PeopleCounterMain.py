import argparse
import datetime
import imutils
import math
import cv2
import numpy as np
from urllib.request import urlopen
import time

width = 800

textDoorIn = 0
textIn = 0
textOut = 0

#url="http://192.168.43.223:81/stream"
url="http://192.168.43.211:81/stream"

def testIntersectionIn(x,w,y,h):
    #res = -450 * x + 400 * y + 157500
    #print(str(res))
    #if ((res >= -550) and (res < 550)):
        #print(str(res))
        #return True
        
    #if((x > 200)and(y> 440))
    
    return False


def testIntersectionOut(x, y):
    #res = -450 * x + 400 * y + 180000
    #if ((res >= -550) and (res <= 550)):
        #print(str(res))
        #return True

    return False


if __name__ == "__main__":
    camera = cv2.VideoCapture(url)

    firstFrame = None

    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        #cv2.findContour：檢測物體的輪廓、cv2.RETR_LIST：取輪廓、cv2.RETR_EXTERNAL：取外輪廓
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        
        # loop over the contours
        for c in cnts:
            #print(c)
            
            #忽略輪廓面積過小的，(12k太小，40k太大)
            print(str(cv2.contourArea(c)))
            if cv2.contourArea(c) < 22000:
                continue
            
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            
            #cv2.boundingRect(圖)，返回四值，x,y為左上座標，w,h為寬和高
            (x, y, w, h) = cv2.boundingRect(c)
            #然後利用下方畫出矩形
            #第一個引數：img是原圖
            #第二個引數：（x，y）是矩陣的左上點座標
            #第三個引數：（x+w，y+h）是矩陣的右下點座標
            #第四個引數：（0,255,0）是畫線對應的rgb顏色
            #第五個引數：2是所畫的線的寬度
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            #cv2.line(影像，開始座標，結束座標，顏色、線條寬度)
            #cv2.line(frame, (width // 4, 450), (width // 2, 450), (250, 0, 1), 2)  # blue line_new(200,450)、(400,450)
            cv2.line(frame, (width // 4, 480), (width // 2, 480), (0, 0, 255), 2)  # red line_new
            cv2.rectangle(frame,(width // 4, 10 ), (width // 2, 450) , (250, 0, 1) , 2)
            #cv2.line(frame, (width // 2, 0), (width, 450), (250, 0, 1), 2)  # blue line
            #cv2.line(frame, (width // 2 - 50, 0), (width - 50, 450), (0, 0, 255), 2)  # red line

            #矩形中心點
            rectagleCenterPoint = ((x + (x + w)) // 2, (y + (y + h)) // 2)
            #畫中心點的圓
            cv2.circle(frame, rectagleCenterPoint, 1, (0, 0, 255), 5)

            #if (testIntersectionIn((x + (x + w)) // 2, (y + (y + h)) // 2)):
            #    textDoorIn += 1
            
            if (testIntersectionIn(x,w,y,h)):
                textDoorIn = 1
            else:
                textDoorIn = 0

            if (testIntersectionOut((x + (x + w)) // 2, (y + (y + h)) // 2)):
                textOut += 1

            # draw the text and timestamp on the frame

            # show the frame and record if the user presses a key
            # cv2.imshow("Thresh", thresh)
            # cv2.imshow("Frame Delta", frameDelta)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.putText(frame, "In: {}".format(str(textDoorIn)), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "door: {}".format(str(textOut)), (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Security Feed", frame)

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()

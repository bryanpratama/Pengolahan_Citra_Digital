# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 23:45:28 2022

@author: bprat
"""

import cv2
import numpy as np
from time import sleep

width_min=40
height_min=50
offset=5
pos_line=350

delay=600
detec = []
person = 0

def pega_centro(x,y,w,h):
        x1 = int(w / 2)
        y1 = int(h / 2)
        cx = x + x1
        cy = y + y1
        return cx,cy
#cctv_pipel
#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('cctv_pipel2.mp4')
subtrachtion = cv2.createBackgroundSubtractorMOG2()

while True:
    ret , frame1 = cap.read()
    time = float(1/delay)
    sleep(time)
    
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    
    img_sub =subtrachtion.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    expand = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
    expand = cv2.morphologyEx (expand, cv2. MORPH_CLOSE , kernel)
    contour,h=cv2.findContours(expand,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame1, (25, pos_line), (1250, pos_line), (255,127,0), 3)
    #cv2.line(frame1, (width_min // 2, 0), (width_min, 450), (250, 0, 1), 2)
    for(i,c) in enumerate(contour):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_outline = (w >= width_min) and (h >= height_min)
        if not validate_outline:
            continue
        
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        center = pega_centro(x, y, w, h)
        detec.append(center)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)
        
        for (x,y) in detec:
            if y<(pos_line+offset) and y>(pos_line-offset):
                person+=1
                cv2.line(frame1, (25, pos_line), (1250,pos_line), (0,127,255), 3)
                detec.remove((x,y))
                print("person is detect :" +str(person))
                
        cv2.putText(frame1, "orang lewat : " + str(person), (0,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,50,255), 3)
        cv2.imshow("detector", expand)
        cv2.imshow("video original", frame1)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(0);
cv2.destroyAllWindows();
cv2.waitKey(1)

                
        
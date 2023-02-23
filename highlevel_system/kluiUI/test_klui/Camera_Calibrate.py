import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

def calibrate_cam(port):
    cap = cv2.VideoCapture(port,cv2.CAP_DSHOW)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 900)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 900)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # names = "img"
    # angle = 0
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        frame = frame[0:0+h, 100:100+730] 
        if ret==True:
            #จุดสีเขียว
            cv2.circle(frame,(int(730/2),int(h/2)),3,(0, 255, 0),-1)
            cv2.line(frame,(int(730/2),int((h/2)-50)),(int(730/2),int((h/2)+50)),(0,255,0),1)
            cv2.line(frame,(int((730/2)-50),int((h/2))),(int((730/2)+50),int((h/2))),(0,255,0),1)
            cv2.imshow('frame',frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.waitKey(1)
            if cv2.getWindowProperty('frame',cv2.WND_PROP_VISIBLE) < 1:        
                break 
        else:
            break
    
    #frame=cv2.imread("kuy.jpg")
    # (h,w) = frame.shape[:2]    
    # center = (w//2,h//2)
    # M = cv2.getRotationMatrix2D(center,angle,1.0)
    # rotated = cv2.warpAffine(frame,M,(w,h),borderMode=cv2.BORDER_REPLICATE)
    # path = 'c:/Users/OAT/Module 8-9/main/img'
    # cv2.imwrite(os.path.join(path , names+".jpg"),rotated)

    # Release everything if job is finished
    cap.release()
    cv2.destroyAllWindows()

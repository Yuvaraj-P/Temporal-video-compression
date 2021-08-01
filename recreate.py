# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 23:36:44 2021

@author: yuvar
"""

import cv2
import csv

frame_list = []
cap = cv2.VideoCapture("C:\\Users\\yuvar\\Documents\\temporal_vc\\outputs\\keyframesvid.mp4")
n=cap.get(cv2.CAP_PROP_FRAME_COUNT)
for i in range(int(n)):
    check,current_frame = cap.read()
    frame_list.append(current_frame)

shape = current_frame.shape
print("Shape of video frame :" + str(shape))

with open('C:/Users/yuvar/Documents/temporal_vc/outputs/meta.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        frame_no=row
        break
        print(row)
csv_file.close()
print(frame_no)
print(len(frame_no))

#Below code runs based on compressed or extracted key frame    
print("Choose the operation:\n1. Play\n2. Re-create")
choice=int(input("Enter the choice :"))
if(choice==1):
    #display module 
    for i in frame_no:
        frame = frame_list[int(i)]
        cv2.imshow("Frame",frame)
        if cv2.waitKey(75) & 0xFF==ord('q'):
            break 
        if frame.any == None:
            break
    for i in range(len(frame_no)):
        frame = frame_list[-1]
        cv2.imshow("Frame",frame)
        if cv2.waitKey(75) & 0xFF==ord('q'):
            break 
        if frame.any == None:
            break
elif(choice==2):
    pathout="C:/Users/yuvar/Documents/temporal_vc/outputs/reinit_vid.mp4"
    height, width, layers = shape
    size=(width,height)
    fps=cap.get(cv2.CAP_PROP_FPS)
    print("Frame rate : "+str(fps))
    out=cv2.VideoWriter(pathout, cv2.VideoWriter_fourcc(*'mp4v'),fps,size)
    for i in frame_no:
        out.write(frame_list[int(i)])
    out.release()
else:
    print("*********** Invalid Choice *************")
   
cap.release()
cv2.destroyAllWindows()
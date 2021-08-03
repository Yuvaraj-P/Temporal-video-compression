# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#! python3

import cv2
import numpy as np
from skimage import measure
import csv

from tkinter import *
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename()
    return file_path

#button=Button(root, text="open", command=open).pack()

#Defining the mean squared error
def mse(imga,imgb):
    
    err = np.sum((imga.astype("float")-imgb.astype("float"))**2)
    err /=float(imga.shape[0]*imga.shape[1])
    
    return err

def main():
    
    # module 1: Read the frame from the video and init var
    root = Tk()
    filepath=open_file()
    print("FIle_Path : "+filepath)
    root.mainloop()
    cap = cv2.VideoCapture(filepath)
    check,current_frame = cap.read()
    
    #Initializing the variables
    frame_list = []
    counter = 0
    frame_no=[]
    check = True
    choice = 1 #default choice
    print("Choose the method for key frame Extraction :")
    print(" 1. Subtraction (default) ")
    print(" 2. Mean Squared Error ")
    print(" 3. Structaral similarity index ")
    choice = int(input("Enter the choice :"))
    
    shape = current_frame.shape
    frame_list.append(current_frame)
    frame_no.append(counter)
    print("Shape of video frame :" + str(shape))
    n=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    
    #module 2 mapper
    for i in range(int(n)-1):
        #cv2.imwrite("frame%d.jpg" %counter ,current_frame)
        check,current_frame = cap.read()
        #MSE
        if(choice == 2):
            diff = mse(frame_list[-1],current_frame)
        
            if(diff <= 10):
                frame_no.append(counter)
                continue
            else:
                frame_list.append(current_frame)
                counter+=1
        #SSIM
        elif(choice == 3):
            b1,g1,r1 = cv2.split(frame_list[-1])
            b2,g2,r2 = cv2.split(current_frame)

            sb = measure.compare_ssim(b1,b2)
            sg = measure.compare_ssim(g1,g2)
            sr = measure.compare_ssim(r1,r2)
            
            if(sb >= 0.95 and sg >= 0.95 and sr >= 0.95):
                frame_no.append(counter)
                continue
            else:
                frame_list.append(current_frame)
                counter+=1
        #subtraction
        else:
            diff =cv2.subtract(frame_list[counter],current_frame)
            b,g,r = cv2.split(diff)
            if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
                frame_no.append(counter)
                continue
            else:
                frame_list.append(current_frame)
                counter+=1
        
        frame_no.append(counter)
        
        
    check=True
    while(check==True):
        check,current_frame = cap.read()
        frame_list.append(current_frame)
        frame_no.append(counter)
        
    print("\nInitial number of frame : " + str(cap.get(cv2.CAP_PROP_FRAME_COUNT)+1) )
    print("Total key_frames after extraction :"+ str(counter))
    print("The Frame No are:")
    print(frame_no)
    print("length :"+str(len(frame_no)))
    
    #print(len(frame_no))
    
    with open('C:/Users/yuvar/Documents/temporal_vc/outputs/meta.csv', mode='w') as out_file:
        out_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        out_writer.writerow(frame_no)
    out_file.close()
    
    
    pathout="C:/Users/yuvar/Documents/temporal_vc/outputs/keyframesvid.mp4"
    height, width, layers = shape
    size=(width,height)
    fps=cap.get(cv2.CAP_PROP_FPS)
    print("Frame rate : "+str(fps))
    out=cv2.VideoWriter(pathout, cv2.VideoWriter_fourcc(*'mp4v'), fps,size)
    for i in range(len(frame_list)):
       out.write(frame_list[i])
    out.release()

    cap.release()
    cv2.destroyAllWindows()
    
if __name__=="__main__":
    main() 

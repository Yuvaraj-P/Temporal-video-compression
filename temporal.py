# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import numpy as np
from ffpyplayer.player import MediaPlayer as mply 
from skimage import measure

#Defining the mean squared error
def mse(imga,imgb):
    
    err = np.sum((imga.astype("float")-imgb.astype("float"))**2)
    err /=float(imga.shape[0]*imga.shape[1])
    
    return err

def main():

    #Read the frame from the video
    cap = cv2.VideoCapture("C:\\Users\\yuvar\\Documents\\Bandicam\\screen2.mp4")
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
    
    frame_list.append(current_frame)
    print("Shape of video frame :" + str(current_frame.shape))
    n=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    for i in range(int(n)-1):
        cv2.imwrite("frame%d.jpg" %counter ,current_frame)
        frame_no.append(counter)
        check,current_frame = cap.read()
        #subtraction
        if(choice == 1):
            diff =cv2.subtract(frame_list[counter],current_frame)
            b,g,r = cv2.split(diff)
            if cv2.countNonZero(b)==0 and cv2.countNonZero(g)==0 and cv2.countNonZero(r)==0:
                continue
            else:
                frame_list.append(current_frame)
                counter+=1
        #MSE
        elif(choice == 2):
            diff = mse(frame_list[-1],current_frame)
        
            if(diff <= 100):
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
            
            if(sb >= 0.9 and sg >= 0.9 and sr >= 0.9):
                continue
            else:
                frame_list.append(current_frame)
                counter+=1
                
    print("\nInitial number of frame : " + str(cap.get(cv2.CAP_PROP_FRAME_COUNT)+1) )
    print("Total key_frames after extraction :"+ str(counter))
    print(frame_no)
    #print(len(frame_no))
    
    #player = mply("C:\\Users\\yuvar\\Documents\\Bandicam\\screen2.mp4") 
    
    #Below code runs based on compressed or extracted key frame

    for i in frame_no:
        frm = frame_list[i]
        cv2.imshow("frame",frm)
        #audio_frame ,val =player.get_frame()
        if cv2.waitKey(75) & 0xFF==ord('q'):
            break 
        if frm.any == None:
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main() 

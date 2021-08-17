import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

########################################

WCam , HCam = 640 , 480  # defining width and height of camera

#########################################


capture = cv.VideoCapture(0)

#setting the weight and height of the camera
capture.set(3, WCam)
capture.set(4, HCam)
pTime = 0

#creating an object from the hand tracking class
detector = htm.handDetector(detectionCon=0.7) #changing the detection confidence 


#Python Core Audio Windows Library from github
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#VolumeMute= volume.GetMute()
#volume.GetMasterVolumeLevel()

#Getting minimun and maximum range
VolumeRange = volume.GetVolumeRange()

MinVolume =  VolumeRange[0]
MaxVolume =  VolumeRange[1]
vol = 0
volBar = 400
volPercent = 0
#VolumeMute = -1

while True:
    success, image = capture.read()

    #finding hand
    image = detector.findHands(image)

#getting the position of the hand
    lmList = detector.findPosition(image, draw =False)
    if len(lmList) != 0:
      # print(lmList[4],lmList[8])

       
       #Allocating variables to list 4 and 8
       x1, y1 = lmList[4][1], lmList[4][2]
       x2, y2 = lmList[8][1], lmList[8][2]  

       #getting the centre of the line
       cx, cy = (x1 + x2)// 2 , (y1 + y2)//2

        #creating a circle around the tip of the hands we need 
       cv.circle(image, (x1, y1), 12, (255, 0, 255), cv.FILLED)
       cv.circle(image, (x2, y2), 12, (255, 0, 255), cv.FILLED)


#creating a line between the two points of the fingers
       cv.line(image, (x1,y1), (x2,y2), (255,0,255), thickness= 2)


#making a cicle for the cetre line
       cv.circle(image, (cx, cy ), 12, (255, 0, 255), cv.FILLED)


#getting the lenght of the line
       lenght = math.hypot(x2 - x1, y2 - y1)
       #print(lenght)



#converting minimun and maximun range
#converting hand range to volume
   #Hand range from 50 to 300
   #Volume range from -65 to 0

       vol = np.interp(lenght, [50,300], [MinVolume, MaxVolume])
      
      #volume for the bar
       volBar = np.interp(lenght, [50,300], [400, 150])


       #volume percentage for the bar
       volPercent = np.interp(lenght, [50,300], [0, 100])
      
      
       print(int(lenght),vol)
       volume.SetMasterVolumeLevel(vol, None) 
       #volume.GetMute(VolumeMute, None)



    # creating a button for when the value is less than 50
       if lenght < 50:
              cv.circle(image, (cx,cy), 15, (0,255,0), cv.FILLED)   
  

# creating a rectangle for the volume bar
    cv.rectangle(image,(50,150),(85,400),(255,0,0),thickness=3 )
    
    #assigning the volume to the height
    cv.rectangle(image,(50,int(volBar)),(85,400),(255,0,0),cv.FILLED )

# frame rate input
    cTime = time.time()
    fps = 1/ (cTime - pTime)   # fps(frame per second)
    pTime = cTime
    
#adding a percentage for the level of the volume
    cv.putText(image,f"FPS: {int(fps)}",(0,50), cv.FONT_HERSHEY_PLAIN,2,(0,0,0), thickness= 2)  

    
 #putting fps on image
    cv.putText(image,f"{int(volPercent)} %",(40,450), cv.FONT_HERSHEY_PLAIN,2,(255,0,0), thickness= 2)  

    
    
    
    cv.imshow("video", image)
    cv.waitKey(1)

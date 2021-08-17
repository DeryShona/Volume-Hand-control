import cv2 as cv
import mediapipe as mp
import time


#Reading from the web camera
capture = cv.VideoCapture(0)

#creating an object for the hand class
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# frame rate
pTime = 0    #previous time
cTime = 0     #current time

#Video read for a success
while True:
    success,image = capture.read()

#Converting image to RGB image...because the hand module uses the RGB format of an image
    imageRGB =cv.cvtColor(image,cv.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

#Detecting a single hand in the image
#And displaying a draw on the image
   # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:

            # Getting information for the hand ie.. landmark information and ID numbers
            for id, lm in enumerate(handlms.landmark): #lm - landmark
                print(id,lm)

        # Calculating pixels value
#h - hieght, #w  - weight,  #c  - channel
                h,w, c = image.shape
# finding position 
                cx,cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)   
            
            #printing  landmarks according to their IDS 
               # if id == 7:
                cv.circle(image, (cx, cy), 12, (255,0,255), cv.FILLED) 
            
            
            mpDraw.draw_landmarks(image,handlms, mpHands.HAND_CONNECTIONS) # hnadlms - hand landmark


# frame rate input
    cTime = time.time()
    fps = 1/ (cTime - pTime)   # fps(frame per second)
    pTime = cTime

# Displaying time
    cv.putText(image,str(int(fps)),(0,50), cv.FONT_HERSHEY_PLAIN,3,(255,0,0), thickness= 3)  

    cv.imshow("Video", image)
    cv.waitKey(1)
    
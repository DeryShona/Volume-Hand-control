import cv2 as cv
import mediapipe as mp
import time

#Reading from the web camera
#capture = cv.VideoCapture(0)


#creating a class
#initialiazation

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

         #creating an object for the hand class
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
   

  
   # frame rate
#pTime = 0    #previous time
#cTime = 0     #current time

#Video read for a success
#while True:
    #success,image = capture.read()

#Converting image to RGB image...because the hand module uses the RGB format of an image
    def findHands(self, image, draw=True):
        imageRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:

             #Detecting a single hand in the image
            #And displaying a draw on the image
            # print(results.multi_hand_landmarks)

            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms,self.mpHands.HAND_CONNECTIONS)
        return image
    
    
    
    #Finding the position of the fingers
    def findPosition(self, image, handNo=0, draw=True):
        
        #creating a list for the land mark
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            
            #Getting information for the hand ie.. landmark information and ID numbers
            for id, lm in enumerate(myHand.landmark): #lm - landmark
                # print(id, lm)
                
                 # Calculating pixels value
            #h - hieght, #w  - weight,  #c  - channel
                h, w, c = image.shape
                
                 # finding position 
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                
                 #printing  landmarks according to their IDS 
                        # if id == 7:
                if draw:
                    cv.circle(image, (cx, cy), 12, (255, 0, 255), cv.FILLED)
        return lmList



def main():
   
   # frame rate
    pTime = 0    #previous time
    cTime = 0     #current time
#Reading from the web camera

    #cTime = 0
    capture = cv.VideoCapture(0)
    detector = handDetector()
   
   #Video read for a success
    while True:
        success, image = capture.read()
        image = detector.findHands(image)
        lmList = detector.findPosition(image)
        if len(lmList) != 0:
            print(lmList[4])
        
        
        # frame rate input
        cTime = time.time()
        fps = 1 / (cTime - pTime)  # fps(frame per second)
        pTime = cTime
        
        # Displaying fps
        cv.putText(image, str(int(fps)), (0, 50), cv.FONT_HERSHEY_PLAIN, 3,(255, 0, 255), 3)
        
        cv.imshow("Image", image)
        
        cv.waitKey(1)


if __name__ == "__main__":
    main()
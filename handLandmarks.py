# -*- coding: utf-8 -*-
"""
This module will use googles mediapipe module to detect and track  hands
The module creates 21 landmarks on the hand to detect its oriention
it will return a list of all the landmarks positions in pixel values

@author: yaron
"""

import cv2
import mediapipe as mp
import time
import math
import numpy as np

from google.protobuf.json_format import MessageToDict


#creates an object of te hand detector and tracker
class handDetector():
    def __init__(self, 
                 mode =False,
                 maxHands=2,
                 modelComplex=1,
                 detectionCon= 0.6,
                 trackCon = 0.6):
        self.mode = mode # 
        self.maxHands = maxHands
        self.modelComplex = modelComplex
        self.detectionCon =detectionCon
        self.trackCon= trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,
                                        self.maxHands,
                                        self.modelComplex,
                                        self.detectionCon,
                                        self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils # drawing utilities to draw landmarks, connections
        self.tipIds = [4,8,12,16,20]# thumb, fore, middle, ring, pinky
        self.hand = 'no hand'
    #method to detct the hands
    def findHands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # the module requires and RGB Image
        self.results = self.hands.process(imgRGB) # detects the hand
       
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks: # if  a hand exists
            for handLms in self.results.multi_hand_landmarks: # done for each hand
                n=0
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                                    self.mpHands.HAND_CONNECTIONS) # draws landmarks and connections


        return img
    

    
    #returns a list with all the landmark postionsin pixel values
    def findPosition(self, img, handNo=0, draw= True, boundingBox=False):
        
        self.lmList=[]
        self.lmListLeft=[]
            
            


        
        xList=[]
        yList=[]
        bbox = []
        
        if self.results.multi_hand_landmarks: # if  a hand exists
            n=0
            for handType,handLms in zip(self.results.multi_handedness,self.results.multi_hand_landmarks):
                # try:myHand = self.results.multi_hand_landmarks[handNo] # gets the results for the required hand
                # except: print("hand doesnt exist")
                # else:   

                    
                    if handType.classification[0].label=='Right':
                        
                    
                        for id,  lm in enumerate(handLms.landmark):
                            #print(id,lm) print id of landmark and location
                            h,w,c  = img.shape # width height and channels
                            cx,cy = int(lm.x *w), int(lm.y * h) # gets the position in pixel values relative to the image
                            #print(id, cx, cy)
                            self.lmList.append([id,cx,cy,lm.z])

                            if boundingBox:
                                xList.append(cx)
                                yList.append(cy)
                                
                        if boundingBox:
                            xmin,xmax = min(xList), max(xList)
                            ymin,ymax = min(yList), max(yList)
                            
                            bbox = xmin,ymin,xmax,ymax
                            if draw:
                                cv2.rectangle(img,(bbox[0]-20,bbox[1]-20),(bbox[2]+20,bbox[3]+20),(0,255,0),2)
                        cv2.putText(img, str(n), (self.lmList[0][1], self.lmList[0][2]), cv2.FONT_HERSHEY_COMPLEX,
                                    3,
                                    (255, 0, 255), 3)
                        n += 1


                    elif  handType.classification[0].label=='Left': 
                        for id,  lm in enumerate(handLms.landmark):
                            #print(id,lm) print id of landmark and location
                            h,w,c  = img.shape # width height and channels
                            cx,cy = int(lm.x *w), int(lm.y * h) # gets the position in pixel values relative to the image
                            #print(id, cx, cy)
                            self.lmListLeft.append([id,cx,cy,lm.z])
                        cv2.putText(img, str(n), (self.lmListLeft[0][1], self.lmListLeft[0][2]), cv2.FONT_HERSHEY_COMPLEX,
                                    3,
                                    (255, 0, 255), 3)
                        n += 1
                        #print(n)

        return self.lmList, self.lmListLeft
    
    def handedness(self):
        if self.results.multi_hand_landmarks:
            for idx, hand_handedness in enumerate(self.results.multi_handedness):
                handedness_dict = MessageToDict(hand_handedness)
                #print(handedness_dict['classification'][0]['label'])
                hand = handedness_dict['classification'][0]['label']
                self.hand = hand
            return hand
        else:
            self.hand = 'no hand'
            return "no hand"
    
    
    #returns a list with 1 where a finger is raised and 0 where finger is lowered
    # [thumb, fore, middle, ring, pinky]
    # if called with noOfFingers true - will return the num of finfgers
    def fingerCounter(self, noOfFingers = False, hand = 'Any'):
        fingersUp = []
        leftUp = []
        rightUp = []
        
        if len(self.lmList)!=0 and hand!='Left':
        

            if self.lmList[4][1] < self.lmList[3][1]:
                fingersUp.append(1)
            else: fingersUp.append(0)

            
            
            if self.lmList[8][2] < self.lmList[6][2]:
                fingersUp.append(1)
            else: fingersUp.append(0)
            if self.lmList[12][2] < self.lmList[10][2]:
                fingersUp.append(1)
            else: fingersUp.append(0)
            if self.lmList[16][2] < self.lmList[14][2]:
                fingersUp.append(1)
            else: fingersUp.append(0)
            if self.lmList[20][2] < self.lmList[18][2]:
                fingersUp.append(1)
            else: fingersUp.append(0)
        
        
        if len(self.lmListLeft)!=0 and hand!='Right':
        

            if self.lmListLeft[4][1] > self.lmListLeft[3][1]:
                fingersUp.append(1)
            else: fingersUp.append(0)

            
            
            if self.lmListLeft[8][2] < self.lmListLeft[6][2]:
                fingersUp.append(1)
            else: fingersUp.append(0)
            if self.lmListLeft[12][2] < self.lmListLeft[10][2]:
                fingersUp.append(1)
            else: fingersUp.append(0)
            if self.lmListLeft[16][2] < self.lmListLeft[14][2]:
                fingersUp.append(1)
            else: fingersUp.append(0)
            if self.lmListLeft[20][2] < self.lmListLeft[18][2]:
                fingersUp.append(1)
            else: fingersUp.append(0)
      
        if noOfFingers: return np.count_nonzero(fingersUp)
        else: return fingersUp
    
    # the method will return the distance between the given fingers.
    # 0 thumb, 1 fore, 2 middle, 3 ring, 4 pinky
    # note th distance is NOT normalised and does not take into account depth
    # distance is NOT given in any particular units
    def fingerDistance(self, fin1,fin2, handedness):
        a = self.tipIds[fin1]
        b = self.tipIds[fin2]
        
        if handedness== 'Right':
            y = abs(self.lmList[a][2]-self.lmList[b][2])
            x = abs(self.lmList[a][1]-self.lmList[b][1])
        elif handedness == 'Left':
            y = abs(self.lmListLeft[a][2]-self.lmListLeft[b][2])
            x = abs(self.lmListLeft[a][1]-self.lmListLeft[b][1])
        else: x, y =0,0            
    
        d = math.sqrt(y**2 + x**2)
        #print (d)
        return d
    
    def pointDistance(self, p1,p2, handedness):
        if handedness== 'Right':
            y = abs(self.lmList[p1][2]-self.lmList[p2][2])
            x = abs(self.lmList[p1][1]-self.lmList[p2][1])
        elif handedness == 'Left':
            y = abs(self.lmListLeft[p1][2]-self.lmListLeft[p2][2])
            x = abs(self.lmListLeft[p1][1]-self.lmListLeft[p2][1])
        else: x, y =0,0    
    
        d = math.sqrt(y**2 + x**2)
        #print (d)
        return d
    
    # finds the distance while taking into account the depth
    # uses the distance between point 1 and 0( wrist and next point) as aref
    # min and max were taken from measuring when the hand is closest to camera
    # and when furthest away
    # there might be a btter way to do this like with the lm.z value
    # or with the solution i offered in the project
    def pointDistanceNormal(self, p1,p2, minRef = 40, maxRef = 120):

        ref = self.pointDistance(0,1,'Right')
            #print(ref)
        norm = np.interp(ref,[minRef,maxRef],[1,0])
            
        dist = self.pointDistance(p1,p2)
            #print(dist)
        d = norm*dist

        return d

    #returns the angle in degrees of the index finger
    #default with x axis. 
    # if called with False angle with y axis will be returned
    # 0 thumb, 1 fore, 2 middle, 3 ring, 4 pinky
    def fingerAngle(self, finger,handedness, with_x_axis = True):
        a = self.tipIds[finger]
        
        if handedness == 'Right':
            y = abs(self.lmList[a][2]-self.lmList[a-3][2])
            x= abs(self.lmList[a][1] - self.lmList[a-3][1])
        elif handedness =='left':
            y = abs(self.lmListLeft[a][2]-self.lmListLeft[a-3][2])
            x= abs(self.lmListLeft[a][1] - self.lmListLeft[a-3][1])
        else: x,y = 0,0
        
        
        h = math.sqrt(y**2 + x**2)
    
        if h>y and h>x :
            if with_x_axis:
                angle = math.degrees(math.asin(y/h))
            else: angle = math.degrees(math.asin(x/h))
        else: angle=-1
    
        return angle

    def pointAngle(self, p1,p2, with_x_axis=True):
        #a = self.tipIds[finger]

        if self.hand == 'Right':
            y = abs(self.lmList[p1][2] - self.lmList[p2][2])
            x = abs(self.lmList[p1][1] - self.lmList[p2][1])
        elif self.hand == 'Left':
            y = abs(self.lmListLeft[p1][2] - self.lmListLeft[p2][2])
            x = abs(self.lmListLeft[p1][1] - self.lmListLeft[p2][1])
        else:
            x, y = 0, 0

        h = math.sqrt(y ** 2 + x ** 2)

        if h > y and h > x:
            if with_x_axis:
                angle = math.asin(y / h)
            else:
                angle = math.asin(x / h)
        else:
            angle = -1

        #print(x,y,h)
        return angle
    
    #returns true if fist is shown
    def fist(self, handedness):

        if handedness=='Right':
            if self.lmList[8][2] > self.lmList[5][2] and self.lmList[12][2] > self.lmList[9][2]  and self.lmList[16][2] > self.lmList[13][2] and self.lmList[20][2] > self.lmList[17][2]:
                return True
        elif handedness == 'Left':
            if self.lmListLeft[8][2] > self.lmListLeft[5][2] and self.lmListLeft[12][2] > self.lmListLeft[9][2]  and self.lmListLeft[16][2] > self.lmListLeft[13][2] and self.lmListLeft[20][2] > self.lmListLeft[17][2]:
                return True
        return False
        
        
        
        

    #retunrs true if thumbs up
    def thumbsUp(self):
        
        if len(self.lmListLeft)!=0:
            for idx in range(20):
                if idx!=4:
                    if self.lmListLeft[4][2]> self.lmListLeft[idx][2]:
                    #print("nope")
                        return False
            return True
        
        if len(self.lmList)!=0:
            for idx in range(20):
                if idx!=4:
                    if self.lmList[4][2]> self.lmList[idx][2]:
                        #print("nope")
                        return False
            return True
        
        return False
    

        
    def isolateHand(self,img,handedness, bg=[], scale = 1, offset = 12, R=255,G=255,B=255):

        # if len(bg) !=0:
        #     mask = bg.copy()
        # else:
        mask = np.zeros_like(img) # create ablack image with same dimensions as image
        
        if handedness == 'Right':
            l = self.lmList
            
        elif handedness == 'Left':
            l = self.lmListLeft
        
        else: l = []
        # cropped = img.copy()
        # if len(l) != 0:
        #     cropped = img[l[8][2]-10:l[0][2]+10,l[4][1]:l[20][1]]
        points = []



        points = np.array([
                            [l[0][1] - 2*offset,l[0][2]],
                            [l[1][1]-offset,l[1][2]],
                            [l[2][1]-offset, l[2][2]],
                            [l[3][1] - offset, l[3][2]],
                            [l[4][1]-offset, l[4][2]],
                            [l[4][1], l[4][2]-offset],
                            [l[4][1] + offset, l[4][2]],
                            [l[3][1] + offset, l[3][2]],
                            [l[2][1] +offset, l[2][2]],
                            [l[1][1] + offset, l[1][2]],

                            [l[5][1]-offset,l[5][2]],
                            [l[6][1]-offset, l[6][2]],
                            [l[7][1] - offset, l[7][2]],
                            [l[8][1]-offset, l[8][2]],
                            [l[8][1], l[8][2]-offset],
                            [l[8][1] + offset, l[8][2]],
                            [l[7][1] + offset, l[7][2]],
                            [l[6][1] +offset, l[6][2]],
                            [l[5][1] + offset, l[5][2]],

                            [l[9][1]-offset,l[9][2]],
                            [l[10][1]-offset, l[10][2]],
                            [l[11][1] - offset, l[11][2]],
                            [l[12][1]-offset, l[12][2]],
                            [l[12][1], l[12][2]-offset],
                            [l[12][1] + offset, l[12][2]],
                            [l[11][1] + offset, l[11][2]],
                            [l[10][1] +offset, l[10][2]],
                            [l[9][1] + offset, l[9][2]],

                            [l[13][1]-offset,l[13][2]],
                            [l[14][1]-offset, l[14][2]],
                            [l[15][1] - offset, l[15][2]],
                            [l[16][1]-offset, l[16][2]],
                            [l[16][1], l[16][2]-offset],
                            [l[16][1] + offset, l[16][2]],
                            [l[15][1] + offset, l[15][2]],
                            [l[14][1] +offset, l[14][2]],
                            [l[13][1] + offset, l[13][2]],

                            [l[17][1]-offset,l[17][2]],
                            [l[18][1]-offset, l[18][2]],
                            [l[19][1] - offset, l[19][2]],
                            [l[20][1]-offset, l[20][2]],
                            [l[20][1], l[20][2]-offset],
                            [l[20][1] + offset, l[20][2]],
                            [l[19][1] + offset, l[19][2]],
                            [l[18][1] +offset, l[18][2]],
                            [l[17][1] + offset, l[17][2]],

                            [l[0][1]+ 2*offset, l[0][2]]
                              ])

        # use the given points to color the required shape in white

        mask = cv2.fillPoly(mask, np.int32([points]), (R,G,B))

        #extract the white oints from the original image
        hand = cv2.bitwise_and(img,mask)
        #cv2.imshow("hand",hand)
        #mask = cv2.GaussianBlur(mask, (7,7), 10)
        if len(bg)!=0:
            hand = cv2.add(hand,bg)

        return hand, mask

    def broad_isolate_hand(self, img, handedness, bg=[], scale=1, offset=12, R=255, G=255, B=255):

        # if len(bg) !=0:
        #     mask = bg.copy()
        # else:
        mask = np.zeros_like(img)  # create ablack image with same dimensions as image

        if handedness == 'Right':
            l = self.lmList

        elif handedness == 'Left':
            l = self.lmListLeft

        else:
            l = []
        # cropped = img.copy()
        # if len(l) != 0:
        #     cropped = img[l[8][2]-10:l[0][2]+10,l[4][1]:l[20][1]]
        points = []

        points = np.array([
            [l[4][1] - offset, l[4][2]],
            [l[4][1], l[4][2] - offset],
            [l[4][1] + offset, l[4][2]],

            [l[8][1] - offset, l[8][2]],
            [l[8][1], l[8][2] - offset],
            [l[8][1] + offset, l[8][2]],

            [l[12][1] - offset, l[12][2]],
            [l[12][1], l[12][2] - offset],
            [l[12][1] + offset, l[12][2]],

            [l[16][1] - offset, l[16][2]],
            [l[16][1], l[16][2] - offset],
            [l[16][1] + offset, l[16][2]],

            [l[20][1] - offset, l[20][2]],
            [l[20][1], l[20][2] - offset],
            [l[20][1] + offset, l[20][2]],

            [l[0][1] + 2 * offset, l[0][2]]
        ])

        # use the given points to color the required shape in white

        mask = cv2.fillPoly(mask, np.int32([points]), (R, G, B))

        # extract the white oints from the original image
        hand = cv2.bitwise_and(img, mask)
        # cv2.imshow("hand",hand)
        # mask = cv2.GaussianBlur(mask, (7,7), 10)
        if len(bg) != 0:
            hand = cv2.add(hand, bg)

        return hand, mask


    def get_info(self, img):

        img = self.findHands(img)
        lmListR, lmListL = self.findPosition(img)
        handedness  = self.handedness()

        return img, lmListR, lmListL, handedness
    




    
def main():

    snap = False

if __name__ == "__main__":
    main()
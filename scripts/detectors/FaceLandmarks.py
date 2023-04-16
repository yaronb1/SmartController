#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 11:35:13 2022

@author: yaron
"""

import cv2
import mediapipe as mp
import numpy as np

class FaceDetector():
    def __init__(self, 
                 mode =False,
                 maxFaces=1,
                 modelComplexity=1,
                 detectionCon= 0.6,
                 trackCon = 0.6):
        self.mode = mode # 
        self.maxFaces = maxFaces
        self.modelComplex = modelComplexity
        self.detectionCon =detectionCon
        self.trackCon= trackCon
        
        self.mpFaces = mp.solutions.face_mesh
        self.face = self.mpFaces.FaceMesh(self.mode,
                                        self.maxFaces,
                                        True,
                                        self.detectionCon,
                                        self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils # drawing utilities to draw landmarks, connections

    #method to detct the hands
    def findFaces(self,img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # the module requires and RGB Image
        self.results = self.face.process(imgRGB) # detects the hand
       
        #print(results.multi_hand_landmarks)
        if self.results.multi_face_landmarks: # if  a hand exists
            for handLms in self.results.multi_face_landmarks: # done for each hand
                if draw: self.mpDraw.draw_landmarks(img, handLms,
                                                    self.mpFaces.FACEMESH_TESSELATION) # draws landmarks and connections

        return img
    
    #returns a list with all the landmark postionsin pixel values
    def findPosition(self, img, draw= True, boundingBox=False):
        
        self.lmList=[]
        xList=[]
        yList=[]
        bbox = []
        
        if self.results.multi_face_landmarks: # if  a hand exists
            try:myFace = self.results.multi_face_landmarks[0] # gets the results for the required hand
            except: print("hand doesnt exist")
            else:
                # if depth:
                #     for id,  lm in enumerate(myHand.landmark):
                #     #print(id,lm) print id of landmark and location
                #         h,w,c  = img.shape # width height and channels
                #         x = lm.x/(1-abs(lm.z))
                #         y = lm.y / (1-abs(lm.z))
                #         cx,cy = int(x *w), int(y * h) # gets the position in pixel values relative to the image
                #     #print(id, cx, cy)
                #         self.lmList.append([id,cx,cy])
                # else:
                    
                    for id,  lm in enumerate(myFace.landmark):
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
                        #return self.lmList, bbox
                            
                    
        return self.lmList, bbox
    
    def getLips(self,img,colour=(255,255,255)):
        l=self.lmList
        mask = np.zeros_like(img)
        if len(l)!=0:
            
            #mask.fill(255)
            
            points= np.array([
                [l[61][1], l[61][2]],
                [l[185][1], l[185][2]],
                [l[40][1], l[40][2]],
                [l[39][1], l[39][2]],
                #[l[37][1], l[27][2]],
                [l[0][1], l[0][2]],
                [l[267][1], l[267][2]],
                [l[269][1], l[269][2]],
                [l[270][1], l[270][2]],
                [l[291][1], l[291][2]],
                [l[375][1], l[375][2]],
                [l[321][1], l[321][2]],
                [l[405][1], l[405][2]],
                [l[314][1], l[314][2]],
                [l[17][1], l[17][2]],
                [l[84][1], l[84][2]],
                [l[181][1], l[181][2]],
                [l[91][1], l[91][2]],
                [l[146][1], l[146][2]]
                ])
            
            mask = cv2.fillPoly(mask, np.int32([points]), colour)
            
            #cv2.imshow("mask", mask)
            lips = cv2.bitwise_and(img,mask)
            return lips
        
        else:return mask
    
def main():
    cap = cv2.VideoCapture(0)
    
    faceDetector= FaceDetector()
    while True:
        success,img= cap.read()
        img= faceDetector.findFaces(img, draw=False)
        lmList, bbox = faceDetector.findPosition(img)
        
        if len(lmList)!=0:
            
            lips = faceDetector.getLips(img)
            #lips = cv2.bitwise_and(img,lips)
            
            cv2.imshow("lips", lips)
            

        
        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            #driver.close()
            break
        
if __name__ == "__main__":
    main()
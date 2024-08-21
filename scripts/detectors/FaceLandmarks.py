#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 11:35:13 2022

@author: yaron
"""
import random

import cv2
import mediapipe as mp
import numpy as np


features = {
    'nose': [168,122,196,236,198,209,49,64,235,59,79,239,238,19,354,457,309,392,294,279,429,420,456,419,168],

}

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

    #retrives the lips and coliurs them in
    #isolat mode will get just the lips on a black bg
    #coloyred will return the image with the coloured lips
    def getLips(self,img,colour=(255,255,255), mode='isolate'):
        l=self.lmList
        if mode =='isolate':
            mask = np.zeros_like(img)
        elif mode =='coloured':
            mask = img.copy()
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
                [l[146][1], l[146][2]],

                [l[78][1], l[78][2]],
                [l[191][1], l[191][2]],
                [l[80][1], l[80][2]],
                [l[81][1], l[81][2]],
                [l[82][1], l[82][2]],
                [l[13][1], l[13][2]],
                [l[312][1], l[312][2]],
                [l[311][1], l[311][2]],
                [l[310][1], l[310][2]],
                [l[415][1], l[415][2]],

                [l[306][1], l[306][2]],
                #[l[323][1], l[323][2]],
                [l[318][1], l[318][2]],
                [l[402][1], l[402][2]],
                [l[317][1], l[317][2]],
                [l[14][1], l[14][2]],
                [l[87][1], l[87][2]],
                [l[178][1], l[178][2]],
                [l[88][1], l[88][2]],
                [l[95][1], l[95][2]],
                [l[61][1], l[61][2]],

                ])
            
            mask = cv2.fillPoly(mask, np.int32([points]), colour)
            
            #cv2.imshow("mask", mask)
            lips = cv2.bitwise_and(img,mask)
            return lips
        
        else:return mask

    def getEyes(self, img, colour=(255, 255, 255), mode='isolate', eye='both'):
        l = self.lmList
        if mode == 'isolate':
            mask = np.zeros_like(img)
        elif mode == 'coloured':
            mask = img.copy()
        if len(l) != 0:

            # mask.fill(255)

            pointsL = np.array([
                [l[463][1], l[463][2]],
                [l[398][1], l[398][2]],
                [l[384][1], l[384][2]],
                [l[385][1], l[385][2]],
                # [l[37][1], l[27][2]],
                [l[386][1], l[386][2]],
                [l[387][1], l[387][2]],
                [l[388][1], l[388][2]],
                [l[466][1], l[466][2]],
                [l[263][1], l[263][2]],
                [l[249][1], l[249][2]],
                [l[390][1], l[390][2]],
                [l[373][1], l[373][2]],
                [l[374][1], l[374][2]],
                [l[380][1], l[380][2]],
                [l[381][1], l[381][2]],
                [l[382][1], l[382][2]],
                [l[362][1], l[362][2]],
            ])

            pointsR = np.array([
                [l[33][1], l[33][2]],
                [l[246][1], l[246][2]],
                [l[161][1], l[161][2]],
                [l[160][1], l[160][2]],
                # [l[37][1], l[27][2]],
                [l[159][1], l[159][2]],
                [l[158][1], l[158][2]],
                [l[157][1], l[157][2]],
                [l[173][1], l[173][2]],
                [l[155][1], l[155][2]],
                [l[154][1], l[154][2]],
                [l[153][1], l[153][2]],
                [l[145][1], l[145][2]],
                [l[144][1], l[144][2]],
                [l[163][1], l[163][2]],
                [l[7][1], l[7][2]],

            ])
            if eye =='left':
                mask = cv2.fillPoly(mask, np.int32([pointsL]), colour)

            elif eye=='right':
                mask = cv2.fillPoly(mask, np.int32([pointsR]), colour)

            elif eye=='both':
                mask = cv2.fillPoly(mask, np.int32([pointsR]), colour)
                mask = cv2.fillPoly(mask, np.int32([pointsL]), colour)


            # cv2.imshow("mask", mask)
            lips = cv2.bitwise_and(img, mask)
            return lips

        else:
            return mask


    def get_feature(self,img, list, colour=(255, 255, 255), mode='isolate',):
        l = self.lmList

        if mode == 'isolate':
            mask = np.zeros_like(img)
        elif mode == 'coloured':
            mask = img.copy()

        if len(l) != 0:
            # mask.fill(255)

            pointsL = np.ndarray((len(list), 2))

            for i, item in enumerate(list):
                #pointsL.append([l[item][1], l[item][2]])
                pointsL[i] =[l[item][1], l[item][2]]
                # pointsL[i][1]  =

            mask = cv2.fillPoly(mask, np.int32([pointsL]), colour)
            lips = cv2.bitwise_and(img, mask)

            return lips
        else: return mask


    
def main():
    import os
    from definitions.config import ROOTDIR
    bg = cv2.imread(os.path.join(ROOTDIR,'images', 'cursor.png'))
    bg = cv2.resize(bg,(20,20))

    print(bg.shape)


    cap = cv2.VideoCapture(0)
    c = (0,255,0)
    faceDetector= FaceDetector()
    while True:
        success,img= cap.read()
        img= faceDetector.findFaces(img, draw=False)
        lmList, bbox = faceDetector.findPosition(img)
        
        if len(lmList)!=0:
            
            lips = faceDetector.getLips(img, colour=c,mode='isolate')
            eyes = faceDetector.getEyes(img, colour=c,mode='isolate')

            nose = faceDetector.get_feature(img, features['nose'], mode ='isolate', colour = (0,255,0))

            #img = cv2.bitwise_and(img,lips)
            #lips = lips+img

            aug_img = lips+eyes+nose
            cv2.imshow("lips", aug_img)


            

        #img = cv2.addWeighted(img,1,bg, 0.5, 0.0)
        #print(img.shape)
        
        cv2.imshow("img", img)
        key = cv2.waitKey(1)
        if key==27:
            c=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            print(c)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            #driver.close()
            break

        
if __name__ == "__main__":
    main()



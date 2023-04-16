#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 14:10:00 2022

@author: yaron
"""

import handLandmarks as hl
import FaceLandmarks as fl
import cv2

import numpy as np

import time
import os





class Drawer():
    def __init__(self,
                 colour=(0,0,0),
                 thickness=0,
                 start=True
                 ):
        self.colour=colour
        self.thickness=thickness
        self.start= start
        self.faceDetector = fl.FaceDetector()
        self.imgCanvas = np.zeros((720,1280,3),np.uint8)


    def draw(self,canvas,x,y,xp,yp):
        cv2.line(canvas,(xp,yp),(x,y),self.colour,self.thickness)


    def drawLips(self,img):
        
        img = img.copy()
        
        img = self.faceDetector.findFaces(img,draw=False)
        lmList = self.faceDetector.findPosition(img)
        lips = self.faceDetector.getLips(img,self.colour)
        
        return lips
        
        

class Button():
    def __init__(self,
                 size=50,
                 startX=100,
                 startY=100,
                 endX =150,
                 endY=150,
                 bID =0,
                 pressed=False
                 
            ):
        self.size=size
        self.startX=startX
        self.startY=startY
        
        self.endX= endX
        self.endY= endY
        self.bID= bID
        self.pressed = pressed
        
    def press(self):
        self.pressed=True
        
    def buttonPressed(self,x,y):
        
        
        if (x > self.startX and x < self.endX and
            y > self.startY and y < self.endY) :
            self.pressed = True
            return True
        else :
            return False

class Screen():
    def __init__(self
            ):
        self.buttons=[]
    
    def addButton(self,button):
        self.buttons.append(button)
        

def buttonPressed(button,x,y):
    
    
    if (x > button.startX and x < button.endX and
        y > button.startY and y < button.endY) :
        return True
    else :
        return False

    
class ScreenDraw():
    def __init__(self):
        self.main()
#write out the function of the button based on his img value
    def buttonFunctions(self,value):
        # global ui
        # global cs
        # global brush
        
        #colour pallatte button
        if value ==0:
            self.ui=1
            self.cs= 1
            
        #red brush stroke
        elif value==1:
            #brush = Drawer(colour=(0,0,255),thickness=15)
            self.brush.colour=(0,0,255)
            self.brush.thickness=15
            self.ui=2
        
        #green brush stroke
        elif value==2:
            #brush = Drawer(colour=(0,255,0),thickness=15)
            self.brush.colour=(0,255,0)
            self.brush.thickness=15
            self.ui=3
    
        #eraser        
        elif value==3:
            #brush = Drawer(colour=(0,0,0),thickness=100)
            self.brush.colour=(0,0,0)
            self.brush.thickness=100
            self.ui=5
            
        #blue brush stroke
        elif value ==4:
            #brush = Drawer(colour=(255,0,0),thickness=15)
            self.brush.colour=(255,0,0)
            self.brush.thickness=15
            self.ui=4
            
        #lip pallatte button
        elif value==5:
            self.brush.colour = (255,255,255)
            self.ui=9
            self.cs=2
        
        #blue lips button
        elif value==6:
            self.brush.colour=(255,0,0)
            self.ui= 6
        
        #green lips button
        elif value==7:
            self.brush.colour= (0,255,0)
            self.ui=7
        
        #red lips
        elif value==8:
            self.brush.colour = (0,0,255)
            self.ui=8
            
        #default lips
        elif value ==9:
            self.brush.colour= (255,255,255)
            self.ui=9
            
           
        elif value=="back":
            self.cs=0
            self.ui=0
        
    def main(self):
        print("drawing started")
        self.done = False
        self.startT1 = 0
        self.xp,self.yp=0,0
        #create a list of imagges from the ggiven folder
        folderPath = "headers"
        myList = os.listdir(folderPath)
        myList.sort()
        self.overlayList = []
        for imPath in myList:
            image = cv2.imread(f'{folderPath}/{imPath}')
            self.overlayList.append(image)
            
        
        #print(overlayList)
            
        #global cs
        self.cs=0
        #global ui
        self.ui=0
        #global brush
        self.brush=Drawer(colour=(0,0,0),thickness=15)
        
        self.detector = hl.handDetector()
        self.faceDetector = self.brush.faceDetector
        
        self.cap = cv2.VideoCapture("/dev/video2")
        self.cap.set(3,1280)
        self.cap.set(4,720)
        self.cTime=0
        self.pTime=0
        
        self.imgCanvas = self.brush.imgCanvas
        #create buttons
        colour_pallatte_button = Button(startX=100, startY=100, endX=150, endY=150,bID=0)
        lipAdd = Button(startX=570, startY=70, endX=690, endY=120, bID=5) 
        
        painterRed=Button(startX=450, startY=50, endX=580,endY=90, bID=1)
        painterBlue = Button(startX=90,startY=50, endX=220,endY=90,bID=4)
        painterGreen = Button(startX=270, startY=50, endX=400, endY=90, bID=2)
        eraser = Button(startX=1100,startY=50,endX=1200, endY=90,bID=3)
        
        blueLips = Button(startX=100,startY=60,endX=170,endY=120,bID=6)
        greenLips = Button(startX=430,startY=60,endX=550,endY=120,bID=7)
        redLips = Button(startX=780,startY=60,endX=900,endY=120,bID=8)
        defaultLips = Button(startX=1160,startY=60,endX=1270,endY=120,bID=9)
        
        #create screnns
        mainScreen= Screen()
        painterScreen = Screen()
        lipScreen = Screen()
        
    
        
        #add buttons to screnns
        mainScreen.addButton(colour_pallatte_button)
        mainScreen.addButton(lipAdd)
        
        
        painterScreen.addButton(painterRed)
        painterScreen.addButton(painterGreen)
        painterScreen.addButton(painterBlue)
        painterScreen.addButton(eraser)
        
        lipScreen.addButton(blueLips)
        lipScreen.addButton(greenLips)
        lipScreen.addButton(redLips)
        lipScreen.addButton(defaultLips)
        
        
        #add screens to screen list 
        self.screens=[mainScreen,painterScreen,lipScreen]
        
        
        
                
            
            
        #success,img = cap.read()
        #img.flags.writeable= False
    
    def loop(self,img):
        #while True:
            
            #success, img = self.cap.read()
            #if success:
                size = img.shape
                img = cv2.resize(img,(1280,720))
                #img = cv2.flip(img,1)
                img = self.detector.findHands(img)
                
                hand = self.detector.handedness()
                right, left= self.detector.findPosition(img) # returns a list with the positions of all the landmarks
                
                if hand == 'Right':
                    lmList = right
                elif hand == 'Left':
                    lmList = left
                else: lmList = []
            
            
                currentScreen = self.screens[self.cs]
                img[0:125,0:1280]=self.overlayList[self.ui]
                #cv2.imshow("header",overlayList[0])
                
                
                if len(lmList)!=0:
                    #print(detector.fingerCounter("Left"))
                    fingers = self.detector.fingerCounter()
                    
                    if self.cs==0:
                        if fingers == [1,1,1,1,1]:
    
                            if self.done:
                                now = time.time()
                                elapsed = now - self.startT1
                                if elapsed >2:
                                    self.done = False
                                    #break
                            else:
                                self.done = True
                                self.startT1 = time.time()
                           
                        else: self.done = False                   
                    
                    #print(fingers)
                    
                    if fingers==[0,1,1,0,0]:
                        x,y = lmList[8][1], lmList[8][2]
                        #print(x,y)
                        #print(len(currentScreen.buttons))
                        for button in currentScreen.buttons:
                            if button.buttonPressed(x,y):
                                self.buttonFunctions(button.bID)
                            
                    
                    if fingers ==[0,1,0,0,0]:        
                        x,y = lmList[8][1], lmList[8][2]
                        
                        #if we are on the colour pallate screen
                        if self.cs ==1:
                            if self.brush.start:
                                self.xp = x
                                self.yp=y
                                self.brush.start = False
                            
                            #cv2.line(imgCanvas,(xp,yp),(x,y),(0,0,255),5)
                            self.brush.draw(self.imgCanvas,x,y,self.xp,self.yp) 
                            self.xp,self.yp=x,y
                            print("drawing")
                            
                        
                        #if we are on lips screen
                        elif self.cs==2 and self.brush.start:
                            lips = self.brush.drawLips(img)
                            #cv2.imshow("lips", lips)
                            self.imgCanvas = cv2.bitwise_or(lips, self.imgCanvas)
                            self.brush.start=False
            
                        
                    else:self.brush.start=True
            
                    if fingers==[1,1,1,1,1]:
                        self.buttonFunctions("back")
                    
                #create black and white mask from the drawing canvas
                imgGray = cv2.cvtColor(self.imgCanvas, cv2.COLOR_BGR2GRAY)
                _,imgInv = cv2.threshold(imgGray,10,254,cv2.THRESH_BINARY_INV)
                #_, imgInv = cv2.threshold(imgGray, 50, 250, cv2.THRESH_BINARY_INV)
                #cv2.imshow("imgInv",imgInv)
                #convert back to colour so we can overlay them
                imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
                #imgg and imgInv will give black where drawing is done on the img
                img = cv2.bitwise_and(img,imgInv)
                #or with the canvas will convert the black spots (drawings from canvas)
                #with their origginal colour
                img = cv2.bitwise_or(img,self.imgCanvas)
                
                #cv2.imshow("canvas", imgCanvas)
                
                # displays the frames per second
                self.cTime = time.time()
                fps = 1/(self.cTime - self.pTime)
                self.pTime = self.cTime
                cv2.putText(img, str(int(fps)), (10,700), cv2.FONT_HERSHEY_COMPLEX,3,
                                (255,0,255),3)
                
                #cv2.imshow("img",img)
                #cv2.imshow("canvas",self.imgCanvas)
                img = cv2.resize(img,(size[1],size[0]))
                return img
            
            


if __name__=='__main__':
    
    sd = ScreenDraw()
    while True:
        
        img = sd.loop()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            sd.cap.release()
            cv2.destroyAllWindows()
            #driver.close()
            break
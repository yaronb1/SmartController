#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 20:48:18 2022

@author: yaron

The following program is designed to create a virtual touch screen that contains
buttons, hand gestures and motions which will allow the user to control the
program.
We can add multiple screens with multiple UI elemnets.

Note: this proggram must get variables from handLandmarks and FaceLandmarks modules

NOTE: this module is still under construction and has not been fully tested
All functions should work weel but future updates will further optimise the
program and remove any bugs that might come up


"""


import numpy as np

import cv2
#import mediapipe as mp
import time
import scripts.detectors.handLandmarks as hl  #imports the module we have written
import scripts.detectors.FaceLandmarks as fl

#import systemFunctions as system

import sys

# import math

try:from win32api import GetSystemMetrics
except: pass
import subprocess
import os


import time
import datetime

from definitions.config import ROOTDIR


import concurrent.futures
import multiprocess
import threading

from loky import get_reusable_executor

'''
@brief
this is the base object we will use. It will contain all the different screens 
as well as foolow along what the current screen is. 
If we are tryingg to control  a web page such as youtube or home assistant
we will add it here as well

@param screens
a list of the screens we have added to the program

@param cs
int of the current screen we are on while the proggram runs

@param web_object
if we are on a screen which interacts with the internet 
we will pass the relavant web object.
Note: this webobject must be created usingg the given classe:
    youtube
    home assistant



'''
class Controller():
    
    def __init__(self,
                 screen_dict = {},
                 web_object =None,
                 csn = '',
                 view_webcam = False,
                 ):

        self.screen_dict = screen_dict

        self.csn =csn
        self.web_object=web_object
        self.idle=True
        self.capture = ''
        self.view_webcam = view_webcam
        
    
    '''
    the main function will run continusly and control the logic of the program
    
    call the run func in a while loop
    gets image and detector as inputs
    shows bg - green when detects and red when no detection plus the fps
    
    should be called with multiprocess
    
    '''
    def main(self, controllers):
        pTime, cTime = 0, 0

        bg = np.zeros((64, 64, 3))


        cap = controllers['cap']
        #detector = controllers['detector']

        detector = hl.handDetector()
        while True:

            # p1= threading.Thread(target = uiii, daemon = True)


            success, img = cap.read()

            if success:
                img = cv2.flip(img, 1)

                self.img, self.lmListR, self.lmListL, self.handedness = detector.get_info(img)


                if len(self.lmListR) != 0 or len(self.lmListL) != 0:
                    # cv2.circle(img, (400, 400), 50, (0, 255, 0), -1)
                    # fingers = detector.fingerCounter()
                    bg[:, :, 1] = 255
                    bg[:, :, 2] = 0


                    if self.handedness == 'Right':
                        x, y = self.lmListR[8][1], self.lmListR[8][2]


                    elif self.handedness == 'Left':
                        x, y = self.lmListL[8][1], self.lmListL[8][2]

                    else:
                        x, y = 0, 0


                else:
                    x, y = 0, 0
                    bg[:, :, 2] = 255
                    bg[:, :, 1] = 0
                self.run([], detector, x, y)


                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    break

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(bg, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 0, 0), 1)


                if self.view_webcam:
                    cv2.imshow('img', img)
                cv2.imshow('bg', bg)
                self.x, self.y = x, y

                if len(self.capture) !=0:
                    cv2.imwrite(os.path.join(ROOTDIR, 'datasets', 'screenshots',str(datetime.datetime.now().strftime('%d_%b-%H_%M'))+self.capture+'.jpg'),img)
                    self.capture=''

            else:
                time.sleep(1)
                controllers['cap'] = cv2.VideoCapture(0)
                cap = controllers['cap']


    """
    call this func to add a screen to the list
    
    """

    def add_screen(self,screen):

        if len(self.screen_dict)==0:
            self.csn= screen.name
        self.screen_dict[screen.name] = screen
        
        
    '''
    @brief
    run is our main function that should run continuously in a while loop 
    from our main program
    it will check the gesture the camera sees and compare it the gestures we have
    added to the current screen.
    
    It will aslo check if we are "pressing" (hovering with our fingers) over 
    any of the buttons in the screen
    
    @param finggers
    This is the ggesture that the camera is currently seeing. 
    This has to be comparable to the gesture we have added to the screen. 
    as a strat the gestures include how many fingers are up
    represented in a list - [thumb, fore, middle, ring, pinky]
    where 0 represents finger is down and 1 represents finger is up
    eg: [0,0,1,0,0]  is not very nice
    
    @param x,y 
    coordinates of finer (or other) that will be used to press the button
    
    all paramaters should be constructed using th handlandmarks module 
    
    '''    
    def run(self,args,detector, x=0, y=0,hover=False,fingers=[]):

        if len(fingers) ==0:
            fingers = detector.fingerCounter()

        #print(fingers)
        #hand, mask = detector.isolateHand()

        screen = self.screen_dict[self.csn]

        if screen.timeout>0 and self.idle:

            if screen.elapsed_time==0:
                screen.start_time = time.time()

            screen.elapsed_time = time.time() - screen.start_time

            if screen.elapsed_time>screen.timeout:
                screen.elapsed_time=0
                try:screen.timeout_func()
                except:
                    print('screen timeout. moving to previous screen')
                    self.back()

        else: screen.elapsed_time=0



        #the select ges will always be called with the x,y coor
        if screen.select_ges is not None:
            ges = screen.select_ges
            try: b =  ges.check_ges(fingers)
            except Exception as e:
                print(e)
                try:
                    a = ges.check_ges(detector)
                except Exception as e: print (e)
                else:
                    if a:ges.func(x,y)

            else:
                if b:ges.func(x,y)



        for ges in screen.gestures:
            try: b =  ges.check_ges(fingers)
            except:
                #print('fingers error')
                try:
                    a = ges.check_ges(detector)
                except:pass
                else:
                    if a:
                        self.capture = ges.name
                        try:ges.func(ges.args)
                        except:ges.func()

            else:
                if b:
                    self.capture = ges.name
                    try:ges.func(ges.args)
                    except:ges.func()
                
        for button in screen.buttons:
            if button.active and button.buttonPressed(x,y):


                if hover:
                    button.hover_over(args)
                else:
                    try:button.func(button.args)
                    except:button.func()

        if 'canvas' in self.screen_dict:
            canvas = self.screen_dict['canvas']

            for ges in canvas.gestures:
                try:
                    b = ges.check_ges(fingers)
                except:
                    # print('fingers error')
                    try:
                        a = ges.check_ges(detector)
                    except:
                        pass
                    else:
                        if a:
                            self.capture= ges.name
                            try:
                                ges.func()
                            except:
                                ges.func(ges.args)

                else:
                    if b:
                        self.capture=ges.name
                        try:
                            ges.func(ges.args)
                        except:
                            ges.func()

            for button in canvas.buttons:
                if button.active and button.buttonPressed(x, y):

                    if hover:
                        button.hover_over(args)
                    else:
                        button.func(button.args)

    # def run_process(self,args,detector, x=0, y=0,hover=False,fingers=[]):
    #
    #
    #     if len(fingers) ==0:
    #         fingers = detector.fingerCounter()
    #     screen = self.screen_dict[self.csn]
    #     processes=[]
    #     #q = multiprocessing.Queue()
    #     for ges in screen.gestures:
    #         #p = multiprocess.Process(target=ges.check_ges,args=[fingers])
    #         p = threading.Thread(target=ges.check_ges, args=[fingers])
    #         p.start()
    #         processes.append(p)


        #print(q.get())
        # for process in processes:
        #     process.join()
        #     #print(process.get())


        results = []
        # with concurrent.futures.ProcessPoolExecutor() as executer:
        #     for ges in screen.gestures:
        #         f= executer.submit(ges.check_ges,fingers)
        #         #except: f = executer.submit(check_gesture,ges,detector)
        #
        #         results.append(f)
        #         #
        #         # f= executer.submit(check_gesture,'s','s')
        #         # results.append(f)
        #
        #
        #     for f in concurrent.futures.as_completed(results): #  prints in order they compltee complete
        #         print(f.result())

        # executer = get_reusable_executor()
        #
        # for ges in screen.gestures:
        #     res=executer.submit(ges.check_ges,fingers)
        #     results.append(res)
        #
        # for res in results:
        #     print(res.result())
        #     if res.result():
        #         cv2.waitKey(0)













    def back(self):
        try: self.move_to_screen(self.psn)
        except:pass
            
    def move_to_screen(self, name):
        print('moved to ' + str(name) + ' screen')
        try:self.psn = self.csn
        except:pass
        self.csn = str(name)
    #gets the screen res on linux
    #still needs some work 
    def get_screen_resolution(self):
        output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
        resolution = output.split()[0].split(b'x')
        return int(resolution[0]), int(resolution[1])
    
    #gets screen res on windows
    #stiil needs some work
    def get_screen_resolution_win(self):
        return GetSystemMetrics(0), GetSystemMetrics(1)
        
    #store images when converting to exe
    # if you are using windows and want to convert to exe this func should be used 
    # to load the images used for UI
    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    
    
    def overlay_transparent(self,background_img, img_to_overlay_t, x, y, overlay_size=None):
        """
        @brief      
        Overlays a transparant PNG onto another image using CV2
        used to add UI images onto the screen to let the user understand what 
        his options are
    	
        @param      background_img    The background image
        @param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
        @param      x                 x location to place the top-left corner of our overlay
        @param      y                 y location to place the top-left corner of our overlay
        @param      overlay_size      The size to scale our overlay to (tuple), no scaling if None
    	
    	@return     Background image with overlay on top
    	"""
    	
        bg_img = background_img
    	
        if overlay_size is not None:
            #print("resized")
            img_to_overlay_t = cv2.resize(img_to_overlay_t, overlay_size)

    	# Extract the alpha mask of the RGBA image, convert to RGB 
        b,g,r,a = cv2.split(img_to_overlay_t)
        overlay_color = cv2.merge((b,g,r))
        
    	# Apply some simple filtering to remove edge noise
        mask = cv2.medianBlur(a,5)

        img1_bg = cv2.bitwise_and(bg_img,bg_img,mask = cv2.bitwise_not(mask))
        
        bg_img = cv2.add(img1_bg, overlay_color)


        return bg_img

'''
@brief
Gestures that are used to control the program
each gesture once created must be added to a screen so that the program can
check if they are used
gestures can either be single gestures such as fingers raised or
motions which will involve one getsure that will trigggeer the beginning of the
motion and one gesture that will complete the motion.  such as swiping

@param gestureTime (seconds)
if we are using a single gesture thuis is how long the camera must see the 
gesture before it recognises it as a gesture. defaults to 2 seconds

@param timeout (seconds)
if we are in motion gesture, if te camera sees the trigger gesture but sees the
ending gesture after the timeout, it will NOT recogise it as motion

@param gesture
variable to symbolise the ggesture. Fingesr uo can be used as dicussed above.
other ggestures should be used accordingg to handlandmarks module.
Note: this script is still under construction and more gestures will be added in
future updates

@param single_ggesture
True if one gesture
False if motion

@param func 
funtion to call one gesture has been triggered
 
'''
class Gesture():
    def __init__(self,
                 gestureTime=1,
                 timeout=3,
                 gesture = [],
                 single_gesture=True,
                 func= None,
                 args = []
                 ):

        self.startTime= 0
        self.started=False
        self.completed = False
        self.gestureTime=gestureTime
        self.timeout=timeout
        self.gesture = gesture
        self.single_gesture=single_gesture
        self.func= func
        self.args = args
        

                
        self.elapsed=0

        
        
    #controller.run will continuasly check this func to return
    #true is gesture is seen
    def check_ges(self,fingers, start_ges = False, end_ges=False):

        if len(fingers)>5 and len(self.gesture) <=5 :
            fingers1= fingers[:5]
            fingers2 = fingers[5:]




            if fingers1==self.gesture or fingers2==self.gesture:
                if self.started:
                    now=time.time()
                    self.elapsed=now-self.startTime
                    #print(int(elapsed))
                    if self.elapsed>self.gestureTime:
                        self.started=False
                        #self.func(self.args)
                        return True
                else:
                     self.started=True
                     self.startTime=time.time()
                     
            else:
                self.started=False
                self.elapsed=0
            
            return False

        else:

            if fingers == self.gesture:
                if self.started:
                    #print('staretd')
                    now = time.time()
                    self.elapsed = now - self.startTime
                    # print(int(elapsed))
                    if self.elapsed > self.gestureTime:
                        self.started = False
                        #self.func(self.args)
                        return True
                else:
                    #print('starting')
                    self.started = True
                    self.startTime = time.time()

            else:
                #print('enduing')
                self.started = False
                self.elapsed = 0

            return False





            #defines a movemnet as input
    def movement(self,start_ges, end_ges):
        
        if start_ges:
            self.started=True
            self.startTime=time.time()
            
        if self.started:
            now=time.time()
            self.elapsed= now-self.startTime
            if self.elapsed<self.gestureTime and end_ges:
                self.started= False
                return True
            
            if self.elapsed > self.timeout:
                self.started=False
                self.elapsed= 0

        return False

'''
@brief
the prigram can cycle through its different screens. On each screen we will
have different ways of interacting with the program and of course different UI

@param cui
int which will follow which UI image to currently display
UI images should be placed in a specific folder and loaded with the add-images
function. they should be placed in alphabetical order and the cui will represent
the numbered order in which they are placed

@param ui_mode
string to tell the screen what mode to display the UI
3 options (for now, more might be added in future)
crop:
    will put the image into part of the video stream
    
transparent: 
    puts a single image on the screen. image must be made with transparency
    
inside_screen:
    will take the desired image from the camera (such as fingers)
    and put them into our desired image
    
@param draw
if we are going to draw on the screen this will be true

@param web_object
if we using a web page such as youtube, we will pass that object here
this should be created using the relevant modules - youtube or homeasssistant
    
@param images_folder
each screen will have images inside their respective folders. all folders
must be placed inside this folder
'''
class Screen():
    def __init__(self,
                 cui=0,
                 ui_mode='transparent',
                 draw=False,
                 web_object = None,
                 name = 'default_screen',
                 args = [],
                 timeout=0,
                 timeout_func= None,
                 select_ges = None,

                 
                 ):
        self.buttons=[]
        self.gestures=[]
        self.ui= []
        self.draw=draw
        self.web_object = web_object
        self.ui_mode = ui_mode
        self.cui=cui

        self.name = name

        self.args = args
        
        self.start=True
        
        self.images_folder = 'images'

        self.timeout= timeout
        self.elapsed_time=0


        self.select_ges = select_ges
        

    def add_args(self,arg):
         self.args=arg

    #once a button is created we will add it with this func
    def add_button(self,button):
        self.buttons.append(button)
    #once a gesture is created we will add it with this func        
    def add_gesture(self,gesture):
        self.gestures.append(gesture)
    
        
    def add_ui(self,img):
        self.ui.append(img)

    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    '''
    @brief called to addd the required images for this specific screen
    
    @param folderPath
    the folder in which the the images are in. this folder must be in the above
    param: self.images_folder
    
    @param size 
    size of the screen eg: (1280,720)
    '''
    def add_images(self, folderPath,size):
        path = self.images_folder + "/" + folderPath
        myList = os.listdir(path)
        myList.sort()
        for imPath in myList:
            if self.ui_mode=='crop':
                image = cv2.imread(self.resource_path(f'{path}/{imPath}'))
                image= cv2.resize(image,(size[0], image.shape[0]))
                print('crope shape = ' + str(image.shape))
                
            elif self.ui_mode=='transparent':
                image = cv2.imread(f'{path}/{imPath}',-1)
                image= cv2.resize(image,size)
                print('tarans shape = ' + str(image.shape))
                
            
                
                
            self.ui.append(image)
    
    
    '''
    @brief
    will add the ui to the video strem. must be running continuously in th
    while loop
    
    @param img
    the videostrem image
    
    @param canvas
    if we are drawingg the canvas must be passed, this must be obtained from
    Drawer object
    
    @param hand
    if we want to put our hand onto another scrren (ui_mode = inside_screen)
    hand will be passed, must be obtained from handlandmarks module
    '''
    def ui_handler(self, img,canvas=None, hand=None):
        
        
        try:UI = self.ui[self.cui]
        except: pass
        if self.ui_mode=='crop':
                        
            img[0:UI.shape[0],0:img.shape[1]]=UI
            
        elif self.ui_mode=='transparent':
           bg_img = img
       	
    
           	# Extract the alpha mask of the RGBA image, convert to RGB 
           b,g,r,a = cv2.split(UI)
           overlay_color = cv2.merge((b,g,r))
           
           	# Apply some simple filtering to remove edge noise
           mask = cv2.medianBlur(a,5)
    
           img1_bg = cv2.bitwise_and(bg_img,bg_img,mask = cv2.bitwise_not(mask))
           
           img = cv2.add(img1_bg, overlay_color)
           
        elif self.ui_mode=='inside_screen':
             if self.start:
                 self.cui=self.web_object.getScreen(hand.shape[1],hand.shape[0])
                 self.start=False
             img = cv2.addWeighted(self.cui, 0.5, hand, 1.0, 0.0)
             
             
        if self.draw:
            #create black and white mask from the drawing canvas
            imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
            _,imgInv = cv2.threshold(imgGray,10,254,cv2.THRESH_BINARY_INV)
            #_, imgInv = cv2.threshold(imgGray, 50, 250, cv2.THRESH_BINARY_INV)
            #cv2.imshow("imgInv",imgInv)
            #convert back to colour so we can overlay them
            imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
            #imgg and imgInv will give black where drawing is done on the img
            img = cv2.bitwise_and(img,imgInv)
            #or with the canvas will convert the black spots (drawings from canvas)
            #with their origginal colour
            img = cv2.bitwise_or(img,canvas)
             
        return img
             
            
    

'''
@brief      
#button will be considered pressed if a given x, y is inside the imaginary rectangle
#given by the buttons dimensions
# the x,y can be fingers, or anything else. However it must be proportional to
screen size and should be obtained using the handLandmarks module

@param startX, startY, endX, endY
all integers which are propotrtional to screen size representing the rectangle
of the button. 
recoomend run the program whilst printing the x, y of your fore finger. Then
hover over the button and obtain the coordinates

@param func
the function called when the butoon is pressed
''' 
class Button():
    def __init__(self,
                 func= None,
                 startX=100,
                 startY=100,
                 endX =150,
                 endY=150,
                 pressed=False,
                 args= [],
                 active=True,
                 button_time = 1,
                 name='lights'
                 
                 
            ):
        self.func=func
        self.startX=startX
        self.startY=startY
        self.args = args

        self.endX= endX
        self.endY= endY
        self.pressed = pressed
        self.button_time=button_time

        self.name=name

        self.active =active
        self.started=False
        
    def press(self):
        self.pressed=True

    def hover_over(self, args):
        img= args[0]
        #print(args)
        cv2.rectangle(img, (self.startX+10, self.startY+10),
                      (self.endX-10, self.endY-10), (255, 0, 0), 3)
        #cv2.imshow('hover', img)
        
    def buttonPressed(self,x,y):
        
        
        if (x > self.startX and x < self.endX and
            y > self.startY and y < self.endY) :

                self.pressed=True

                if self.started:
                    now = time.time()
                    self.elapsed = now - self.startTime
                    # print(int(elapsed))
                    if self.elapsed > self.button_time:
                        self.started = False
                        return True
                else:
                    self.started = True
                    self.startTime = time.time()

        else:
            self.started = False
            self.elapsed = 0
            self.pressed=False
            return False





        
'''
@brief gives us the option to draw and leave imprints (such as our lips) on the
screen

@param colour
colour of the drawer in (b,g,r)

@param thickness
int - thickness of brush 
'''      
class Drawer():
    def __init__(self,
                 colour=(0,0,0),
                 thickness=15,
                 ):
        self.colour=colour
        self.thickness=thickness
        
        self.start= True
        self.faceDetector = fl.FaceDetector()
        self.imgCanvas = np.zeros((720,1280,3),np.uint8)
        
        self.xp=0
        self.yp=0

    '''
    @brief 
    if we are drawing call this func in the loop
    
    @param img
    img to draw on
    
    @param x,y
    coordinates where to draw. proportional to screen size
    
    @param draw
    if draw is flase wwe will see on the screen what has been drawn
    BUT not actually draw
    if true we will draw and see what has been drawn
    
    '''
    def draw(self,img,x,y):

        if self.start:
            self.xp = x
            self.yp=y
            self.start = False
        self.imgCanvas=cv2.line(self.imgCanvas,(self.xp,self.yp),(x,y),self.colour,self.thickness)
        self.xp=x
        self.yp=y
            
       

        
        return self.imgCanvas
                

    '''
    @brief
    grab our lips and put them onto the screen
    
    @param img
    image to put our lips on
    '''
    def drawLips(self,img):
        
        img = img.copy()
        
        img = self.faceDetector.findFaces(img,draw=False)
        lmList = self.faceDetector.findPosition(img)
        lips = self.faceDetector.getLips(img,self.colour)
        self.imgCanvas = cv2.bitwise_or(lips, self.imgCanvas)
        
        return self.imgCanvas









control =Controller()

def bfunc():
    print('button preesed')    
    control.cs=1             

            
    

if __name__ == "__main__":

    # cap = cv2.VideoCapture(0)
    # success, img = cap.read()
    # media = SimpleUI().MediaButtons(img = img)
    # bg = media.play_button()
    # bg = media.next_button()
    # bg, vol_bar= media.volume_bar()
    #
    # detector = hl.handDetector()
    # controller=Controller()
    #
    #
    # startScreen = Screen(ui_mode='transparent')
    # startScreen.add_button(vol_bar)
    # controller.add_screen(startScreen)
    # while True:
    #     success, img = cap.read()
    #     img = cv2.flip(img, 1)
    #
    #     img, lmListR, lmListL, handedness = detector.get_info(img)
    #
    #     if len(lmListR)!=0 or len(lmListL)!=0:
    #         hand, mask  = detector.isolateHand(img, handedness,bg=bg)
    #
    #
    #         try:x, y = lmListR[8][1], lmListR[8][2]
    #         except:x, y = lmListL[8][1], lmListL[8][2]
    #         args = x, y,
    #
    #         controller.run(args, detector =detector, x=x, y=y)
    #         cv2.imshow('hand', hand)
    #
    #
    #     if cv2.waitKey(1) & 0xFF==ord('q'):
    #         cap.release()
    #         cv2.imwrite('/home/yaron/PycharmProjects/SmartController/images/ges_images/swipe_up.jpg',hand)
    #         cv2.destroyAllWindows()
    #         break

    cap = cv2.VideoCapture(0)
    success, img = cap.read()

    cv2.imshow('bg', img)
    cv2.waitKey(0)


    
    
    
    
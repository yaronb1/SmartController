import cv2
import numpy as np

import SmartController as sc

import handLandmarks as hl

import pickle

from Tools import ColorEnhancer
from Tuya import Controller as tuya_controller



'''
the ui class aims to create a fun and interactive way of dealing with the smarthouse
we will have and image as the bacggorund which will have buttons spread across it
there will be a pointer that will allow us to click buttons and navigate betewwn screens
'''
class UI():

    def __init__(self,
                 #background_size = (600,450),
                 background_size=(1280, 720),
                 background_img= 'background.png',

                 cursor_size= (60,60),
                 cursor_img = 'pointer_t.png'

                 ):
        self.background_size = background_size
        self.background = cv2.imread(background_img)
        self.background = cv2.resize(self.background, self.background_size)
        self.background_original=self.background.copy()

        self.canvas = np.zeros_like(self.background)
        self.canvas = self.black_to_transparent(self.canvas)

        self.cursor_size = cursor_size
        self.cursor = cv2.imread(cursor_img,-1)
        self.cursor = cv2.resize(self.cursor, self.cursor_size)

        self.buttons={}

        self.n= 0





        #self.cap = cv2.VideoCapture(-1)

        # self.cap.set(3,1280)
        # self.cap.set(4,720)


    def run(self,x,y,controller):

        self.canvas = np.zeros_like(self.background)
        self.canvas = self.black_to_transparent(self.canvas)

        for button in controller.screen_dict[controller.csn].buttons:

            try:self.is_pressed(button)
            except:pass
            try:self.glimmer(button)
            except: pass


        self.add_cursor_to_canvas(x,y)
        screen = self.overlay(self.background,self.canvas)
        cv2.imshow('canvas', self.canvas)

        return screen



    def add_cursor_to_canvas(self,x,y):


        #add the cursor tto the background based on hands x,y values
        try:self.canvas[y-self.cursor_size[1]//2:y+self.cursor_size[1]//2,x-self.cursor_size[0]//2:x+self.cursor_size[0]//2]=self.cursor
        except: pass



    def add_button_ui(self,button,img=None):
        coordinates = [button.startX, button.startY, button.endX, button.endY]
        try: self.add_button_img(img,button)
        except Exception as e: print(e)
        else:print('image added')
        self.highlight_button(coordinates)
        self.shadow(coordinates)

        button_ui = self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]].copy()
        self.buttons[button.name]=button_ui



    def add_button_img(self,img,button):


        #img= cv2.imread('cold_b.png',-1)
        img = cv2.resize(img,(abs(button.endX-button.startX),abs(button.endY-button.startY)))
        #
        #img = self.white_to_transparent(img)
        cv2.imshow('trasnparentimage', img)
        #
        bg = self.background[button.startY:button.endY, button.startX:button.endX].copy()
        cv2.imshow('bg',bg)
        img = self.overlay(bg,img)
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        cv2.imshow('ready button', img)
        self.background[button.startY:button.endY, button.startX:button.endX]= img
        #cv2.imshow('canvas', self.canvas)


    def highlight_button(self,coordinates):

        #coordinates = [button.startX, button.startY,button.endX,button.endY]

        button = self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]].copy()

        highlighted_button = ColorEnhancer(img_path=button, r=40).enhanced_img



        self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]= highlighted_button

    def shadow(self,coordinates):

        #coordinates = [button.startX, button.startY,button.endX,button.endY]

        button = self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]].copy()

        shadow = button[button.shape[0] - 10:button.shape[0], :]
        effect = ColorEnhancer(img_path=shadow, hsv=True, v=100)
        button[button.shape[0] - 10:button.shape[0], :] = effect.enhanced_img
        self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]] = button
        #self.buttons['lights']=button



    def glimmer(self, button):

        self.n += 1
        if self.n == 99:
            self.n = 0

        n=self.n

        coordinates = [button.startX, button.startY,button.endX,button.endY]

        #glimmer = self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]].copy()
        glimmer = self.buttons[button.name]
        overlay = glimmer.copy()
        cv2.imshow('effect', overlay)
        cv2.rectangle(overlay,(3*n,0),(3*n+10, overlay.shape[0]),(255,255,255),-1)

        # Transparency value
        alpha = 0.50

        # Perform weighted addition of the input image and the overlay
        effect = cv2.addWeighted(overlay, alpha, glimmer, 1 - alpha, 0)

        effect = cv2.cvtColor(effect,cv2.COLOR_RGB2RGBA)

        #b= self.background.copy()

        self.canvas[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]] = effect
        #b[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]] = effect
        #cv2.imshow('ba', b)

    def is_pressed(self,button):
        if button.started:

            try: m= button.m
            except:
                button.m=0
                m=button.m


            cv2.rectangle(self.canvas,(button.startX,button.startY), (button.endX,button.endY), (0,255,0),10)

            cv2.line(self.canvas, (button.startX,button.endY), (button.endX - m, button.endY), (255,255,255),10)
            try:button.m+=(20 // button.button_time)
            except: pass

        else:
            button.m=0





    def overlay(self,img,pointer):
        bg_img = img

        # Extract the alpha mask of the RGBA image, convert to RGB
        b, g, r, a = cv2.split(pointer)
        overlay_color = cv2.merge((b, g, r))

        # Apply some simple filtering to remove edge noise
        mask = cv2.medianBlur(a, 5)

        img1_bg = cv2.bitwise_and(bg_img, bg_img, mask=cv2.bitwise_not(mask))

        final_img = cv2.add(img1_bg, overlay_color)

        return final_img

    def black_to_transparent(self,img):
        # read the image
        image_bgr = img
        # get the image dimensions (height, width and channels)
        h, w, c = image_bgr.shape
        # append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
        image_bgra = np.concatenate([image_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
        # create a mask where white pixels ([255, 255, 255]) are True
        white = np.all(image_bgr == [0, 0, 0], axis=-1)
        # change the values of Alpha to 0 for all the white pixels
        image_bgra[white, -1] = 0
        # save the image
        return image_bgra

    def white_to_transparent(self,img):
        # read the image
        image_bgr = img
        # get the image dimensions (height, width and channels)
        h, w, c = image_bgr.shape
        # append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
        image_bgra = np.concatenate([image_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
        # create a mask where white pixels ([255, 255, 255]) are True
        white = np.all(image_bgr == [255, 255, 255], axis=-1)
        # change the values of Alpha to 0 for all the white pixels
        image_bgra[white, -1] = 0
        # save the image
        return image_bgra





def hello(*args):
    tuya_controller().kitchen_toggle()


def open_lights(*args):
    tuya_controller().open_toggle()

def ac_funcs(*args):
    print('ac')


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = hl.handDetector()
    controller = sc.Controller()
    ui = UI()
    main_screen = sc.Screen(name = 'start')

    with open('/home/yaron/PycharmProjects/SmartController/button_variables/kitchen_lights.pkl',
              'rb') as f:  # Python 3: open(..., 'rb')
        coordinates = pickle.load(f)

    with open('/home/yaron/PycharmProjects/SmartController/button_variables/open_lights.pkl',
              'rb') as f:  # Python 3: open(..., 'rb')
        open_coordinates = pickle.load(f)

    with open('/home/yaron/PycharmProjects/SmartController/button_variables/ac_lights.pkl',
              'rb') as f:  # Python 3: open(..., 'rb')
        ac_coordinates = pickle.load(f)

    button  = sc.Button(func=hello, startX=coordinates[0], startY=coordinates[1], endX=coordinates[2], endY=coordinates[3], button_time=5)

    open_button = sc.Button(func=open_lights, startX=open_coordinates[0], startY=open_coordinates[1], endX=open_coordinates[2],
                       endY=open_coordinates[3], name ='open_lights')

    ac_button = sc.Button(func=ac_funcs, startX=ac_coordinates[0], startY=ac_coordinates[1], endX=ac_coordinates[2],
                       endY=ac_coordinates[3], name ='ac')

    ui.add_button_ui(button)
    main_screen.add_button(button)

    ui.add_button_ui(open_button)
    main_screen.add_button(open_button)


    ac_button_img =cv2.imread('cold_b.png',-1)
    cv2.imshow('ac', ac_button_img)
    ui.add_button_ui(ac_button, ac_button_img)
    main_screen.add_button(ac_button)

    controller.add_screen_dict(main_screen)
    while True:

        #get info about hand
        success, img = cap.read()
        img = cv2.flip(img, 1)

        img, lmListR, lmListL, handedness = detector.get_info(img)

        if len(lmListR) != 0 or len(lmListL) != 0:
            fingers = detector.fingerCounter()

            if handedness=='Right':
                x, y = lmListR[8][1], lmListR[8][2]

            elif handedness == 'Left':
                x, y = lmListL[8][1], lmListL[8][2]

            #screen = ui.run(x,y,controller)
            controller.run([],detector,x,y)

            #cv2.imshow('screen',screen)

        else:

            x,y=0,0


        screen = ui.run(x,y, controller)
        cv2.imshow('screen', screen)





        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    # #the pointer
    #cv2.circle(bg,)
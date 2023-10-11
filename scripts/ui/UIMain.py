import threading
import time
import math


import numpy as np
import cv2
from scripts.ui.Tools import ColorEnhancer

from scripts.detectors import handLandmarks as hl
import scripts.controllers.SmartController as sc
from scripts.detectors.Gestures import Gesture, Movement

import pickle
from deprecated.Tuya import Controller as tuya_controller


import alsaaudio
import os

#ROOTDIR = os.path.dirname(os.path.abspath(__file__))
from definitions.config import ROOTDIR
'''
this file will control the main UI for the smart house.
It will be designed for use with the smart controller

Elements:

Background - 
    a static image taht will be built befor the program starts
    contains buttons and images
    
canvas - 
    dynamic image with black background
    will be added to the background and have dynamic feaures such as glimmers and cursor
buttons-
    must work in tandam with the smartcontroller buttons but have different
'''

class SimpleUI:
    background = []

    def add_text(self,img, text, org=(50,50),scale=1,colour=(0,0,0), thickness=1):
        img = cv2.putText(img,text,org,cv2.FONT_HERSHEY_COMPLEX,scale,colour,thickness)
        return img

    def create_transparent_backround(self, size = (640,480)):
        transparent_img = np.zeros((size[0], size[1], 4), dtype='uint8')
        return transparent_img

    def transparent_image(self, image, size):
        img = cv2.resize(image, size)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA) # add alpha channel
        img[np.where(np.all(img[..., :3] == 0, -1))] = 0 # all black pixels will be transparent
        return img

    def add_image_to_background(self,image,ui_size,background_size, x=0, y=0):
        if len(self.background) ==0:
            self.background = self.create_transparent_backround(background_size)

        image = self.transparent_image(image,ui_size)
        #self.background = cv2.add(image, self.background)
        self.background[y:image.shape[0]+y, x:image.shape[1]+x] = image

        return self.background

    class MediaButtons():

        def __init__(self,
                     img=[]):

            if len(img)!=0:
                self.img = img
                self.width = img.shape[1]
                self.height = img.shape[0]

            else:
                self.img = np.zeros((480,640))
                self.width = 640
                self.height = 480

            self.background = np.zeros_like(self.img)

            self.audio = alsaaudio.Mixer()


        def play_button(self, size=10, offset=0):

            w,h = self.background.shape[1], self.background.shape[0]

            print(w,h)

            points = np.array([
                [w//2+offset, h-size],
                [w//2+offset, h-size*5],
                [w//2+size*4+offset, h-size*3]
            ])

            self.background = cv2.fillPoly(self.background, np.int32([points]), (255, 255, 255))

            return self.background

        def next_button(self, size=10, offset=50):
            w,h = self.background.shape[1], self.background.shape[0]

            print(w,h)

            points = np.array([
                [w//2+offset, h-size],
                [w//2+offset, h-size*5],
                [w//2+size*4+offset, h-size*3]
            ])

            self.background = cv2.fillPoly(self.background, np.int32([points]), (255, 255, 255))

            points= np.array([
                [w//2+size*4+offset,h-size],
                [w//2+size*4+offset, h-size*5]
            ])

            self.background = cv2.fillPoly(self.background, np.int32([points]), (255, 255, 255))
            return self.background

        def volume_bar(self, size=10, offset=0):
            #w,h = self.background.shape[1], self.background.shape[0]

            cv2.rectangle(self.background,(5,self.height-20), (50, 50), (255,255,255))

            vol = self.audio.getvolume()
            vol = int(vol[0])
            vol = np.interp(vol, [0, 100], [5, self.height-20])

            cv2.rectangle(self.background, (5, int(vol)), (50, self.height-20), (255, 255, 255), cv2.FILLED)

            vol_bar = Button(func=self.vol_func, startX=5,startY=50, endX=50, endY=self.height-20)


            return self.background, vol_bar


        def vol_func(self,*args):

            x1, y1 = args[0]

            length = 460-y1

            vol = np.interp(length, [5, 460], [0, 100])

            #m= alsaaudio.Mixer()
            self.audio.setvolume(int(vol))

            cv2.rectangle(self.background, (5, y1), (50, 50), (0, 0, 0), cv2.FILLED)
            cv2.rectangle(self.background, (5, self.height - 20), (50, 50), (255, 255, 255))
            cv2.rectangle(self.background, (5, self.height-20), (50, y1), (255, 255, 255), cv2.FILLED)






class Controller():

    screens = {}
    current_screen = ''

    def main(self,controllers):

        cTime, pTime = 1, 0,
        x, y = 0, 0
        img = []
        cv2.namedWindow('ui')
        while True:
            # print('working')

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            try:
                screen = self.get_screen()
                screen_img = screen.run(x, y, img)
                cv2.putText(screen_img, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 1)
                cv2.imshow('ui', screen_img)

                if cv2.waitKey(1):
                    pass
            except Exception as e:
                print(e)





    def add_screen(self,screen):

        if len(self.screens)==0:
            self.current_screen = screen.name
        self.screens[screen.name]=screen

    def move_to_screen(self,*args):
        screen_name = args[0]
        print(screen_name)

        try:self.previous_screen = self.current_screen
        except:pass
        self.current_screen = screen_name

    def get_screen(self):
        return self.screens[self.current_screen]

    def back(self):
        try: self.move_to_screen(self.previous_screen)
        except:pass

    def black_to_transparent(self,img,w_t_t=False):
        # read the image
        image_bgr = img
        # get the image dimensions (height, width and channels)
        h, w, c = image_bgr.shape
        # append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
        image_bgra = np.concatenate([image_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
        # create a mask where white pixels ([255, 255, 255]) are True
        if w_t_t: white = np.all(image_bgr == [255, 255, 255], axis=-1)
        else: white = np.all(image_bgr == [0, 0, 0], axis=-1)
        # change the values of Alpha to 0 for all the white pixels
        image_bgra[white, -1] = 0
        # save the image
        return image_bgra







class Screen():
    def __init__(
            self,
            background_size=(1280, 720),
            background_img='',
            cursor_size=(60, 60),
            cursor_img=os.path.join(ROOTDIR,'UI','images', 'cursor_images','pointer_t.png' ) ,
            webcam=False,
            cap=0,
            webobject='',
            name='',
            show_cursor = True,
            timeout=0,
            timeout_func=None
    ):

        self.show_cursor= show_cursor
        self.name=name
        self.webcam = webcam
        self.background_size = background_size

        # if len(webobject)>0:
        #     if webobject=='youtube':
        #         self.webobject = youTubeController(width= self.background_size[0],height=self.background_size[1] )
        #         # yt.openYoutube()
        #         y = threading.Thread(daemon=True, target=self.webobject.openYoutube)
        #
        #         y.start()
        #         y.join()
        #         self.background= self.webobject.getScreen()


        if self.webcam:

            success, self.background = cap.read()
            cv2.imshow('bg', self.background)
            cv2.waitKey(0)


        else:
            try:
                self.background = cv2.imread(background_img)
                self.background = cv2.resize(self.background, self.background_size)

            except:
                try:
                    self.background = background_img
                    self.background = cv2.resize(self.background, self.background_size)

                except:
                    self.background = np.zeros((self.background_size[1],self.background_size[0],3),dtype='uint8')
                    #self.background = cv2.cvtColor(self.background,cv2.COLOR2RGB)

        self.canvas_original=self.black_to_transparent(self.background)
        self.background_original=self.background.copy()


        self.buttons = {}
        self.button_uis={}
        self.canvas = np.zeros_like(self.background)
        #print(self.canvas.shape)

        self.cursor_size = cursor_size
        self.cursor = cv2.imread(cursor_img,-1)
        self.cursor = cv2.resize(self.cursor, self.cursor_size)

        self.n=0
        self.images_to_add = []

        self.timeout=timeout
        self.elapsed_time=0
        self.timeout_func=timeout_func
        self.idle=True




    #add button to the screen
    def add_button(self,button):
        try: drop_buttons = button.buttons
        except:pass
        else:
            for b in drop_buttons:
                self.add_button_ui(b)
                self.buttons[b.name]=b
        self.buttons[button.name] = button


    #provide the image and where to place them
    #the image must be tranparent
    #pass size to resize
    def add_image_to_canvas(self,img,coordinates, size=0):

        if size!=0:
            try:
                img = cv2.resize(img,size)
                img = self.black_to_transparent(img)
            except Exception as e: print(e)
        self.images_to_add.append((img,coordinates))

    #run the in the while loop
    def run(self,x,y,img):

        if self.webcam:
            self.background=img

        # elif self.inside_screen:
        #      if self.start:
        #          self.cui=self.web_object.getScreen(hand.shape[1],hand.shape[0])
        #          self.start=False
        #      img = cv2.addWeighted(self.cui, 0.5, hand, 1.0, 0.0)

        self.canvas = np.zeros_like(self.canvas_original)

        #self.canvas = self.black_to_transparent(self.canvas)

        for i in self.images_to_add:
            self.add_img_to_canvas(i)
            #except:pass


        for button in self.buttons.values():


            if button.button_sc.active:
                try:
                    self.add_button_img_to_canvas(button)
                except Exception as e: print(e)

            #button = self.buttons[button]
            try:self.is_pressed(button)
            except:print('pressing button error')
            #except Exception as e: print(e)
            if button.glimmer: self.glimmer(button)
            #except: pass


        if self.show_cursor:
            self.add_cursor_to_canvas(x,y)

        #cv2.imshow('canvas', self.canvas)
        screen = self.overlay(self.background,self.canvas)



        '''
        screen timeout option 
        '''
        if self.timeout > 0 and self.idle:

            if self.elapsed_time == 0:
                self.start_time = time.time()

            self.elapsed_time = time.time() - self.start_time

            if self.elapsed_time > self.timeout:
                self.elapsed_time=0
                try:
                    self.timeout_func()
                except:
                    #IF TIMEOUT FUNC WASNT PASSED THIS WILL JUST RERURN THE SAME SCREEN LIKE ALWAYS
                    print('screen timeout. moving to previous screen')
                    return screen

        else: self.elapsed_time=0





        #print(self.buttons)
        return screen


    #add cursor
    def add_cursor_to_canvas(self,x,y):


        #add the cursor tto the background based on hands x,y values
        try:self.canvas[y-self.cursor_size[1]//2:y+self.cursor_size[1]//2,x-self.cursor_size[0]//2:x+self.cursor_size[0]//2]=self.cursor
        except: pass

    def black_to_transparent(self,img,w_t_t=False):
        # read the image
        image_bgr = img
        # get the image dimensions (height, width and channels)
        h, w, c = image_bgr.shape
        # append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
        image_bgra = np.concatenate([image_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
        # create a mask where white pixels ([255, 255, 255]) are True
        if w_t_t: white = np.all(image_bgr == [255, 255, 255], axis=-1)
        else: white = np.all(image_bgr == [0, 0, 0], axis=-1)
        # change the values of Alpha to 0 for all the white pixels
        image_bgra[white, -1] = 0
        # save the image
        return image_bgra

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


    #completes the buttons image
    def add_button_ui(self,button):
        coordinates = [button.coordinates['startX'], button.coordinates['startY'], button.coordinates['endX'], button.coordinates['endY']]

        # try: self.add_button_img_to_canvas(button)
        # except Exception as e: print(e)
        # else:print('image added')
        # if button.highlight:self.highlight_button(coordinates)
        # if button.shadow:self.shadow(coordinates)

        #button_ui = self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]].copy()
        # try:self.background[button.coordinates['startY']:button.coordinates['endY'], button.coordinates['startX']:button.coordinates['endX']] = button.img[:,:,:3]
        # except Exception as e: print(e)
        #
        #
        # try:
        #     layer = np.zeros_like(self.canvas)
        #     layer[button.coordinates['startY']:button.coordinates['endY'],
        #     button.coordinates['startX']:button.coordinates['endX']] = button.img
        #     layer = self.black_to_transparent(layer)
        #     self.background = self.overlay(self.background,layer)
        #
        # except Exception as e : print(e)


        #self.button_uis[button.name] = button_ui

    #pass a tuple with the imga and where to place them
    def add_img_to_canvas(self,image):
        img= image[0]
        coordinates= image[1]
        try:self.canvas[coordinates[0]:coordinates[0]+img.shape[0],coordinates[1]:coordinates[1]+img.shape[1]] = img
        except Exception as e: print(e)


    def add_button_img_to_canvas(self,button):

        #image = cv2.resize(button.img,(abs(button.coordinates['endX']-button.coordinates['startX']),abs(button.coordinates['endY']-button.coordinates['startY'])))
        self.canvas[button.coordinates['startY']:button.coordinates['endY'], button.coordinates['startX']:button.coordinates['endX']]= button.img



    def highlight_button(self,coordinates):

        #coordinates = [button.startX, button.startY,button.endX,button.endY]

        button_h = self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]].copy()

        highlighted_button = ColorEnhancer(img_path=button_h, r=40).enhanced_img



        self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]= highlighted_button

    def shadow(self,coordinates):

        #coordinates = [button.startX, button.startY,button.endX,button.endY]

        button_s = self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]].copy()

        shadow = button_s[button_s.shape[0] - 10:button_s.shape[0], :]
        effect = ColorEnhancer(img_path=shadow, hsv=True, v=100)
        button_s[button_s.shape[0] - 10:button_s.shape[0], :] = effect.enhanced_img
        self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]] = button_s
        #self.buttons['lights']=button



    def glimmer(self, button):

        self.n += 1
        if self.n == 99:
            self.n = 0

        n=self.n

        coordinates = [button.coordinates['startX'], button.coordinates['startY'],button.coordinates['endX'],button.coordinates['endY']]

        #glimmer = self.background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]].copy()
        glimmer = self.button_uis[button.name]
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

    def is_pressed(self,button,circ=True):


        buttonsc = button.button_sc



        try: dropdown= button.buttons
        except:
            if buttonsc.started:

                try: m= buttonsc.m
                except:
                    buttonsc.m=0
                    m=buttonsc.m

                finally:
                    if m>=180:
                        color = (0,255,0)
                    else:
                        color=(0,100,0)


                if circ:
                    cv2.ellipse(self.canvas,
                                #(abs(button.coordinates['endY'] -button.coordinates['startY']), abs(button.coordinates['endX'] -button.coordinates['startX'])), #centre
                                (button.coordinates['startX'] + button.size[0]//2,  button.coordinates['startY'] +button.size[1]//2),
                                (button.size[0]//2,button.size[0]//2), #axis
                                0, 180, 360+m, #angle, startangle, endangle
                                color, 10) #color, thickness

                else:
                    cv2.rectangle(self.canvas,(buttonsc.startX,buttonsc.startY), (buttonsc.endX,buttonsc.endY), (0,255,0),10)
                    cv2.line(self.canvas, (buttonsc.startX,buttonsc.endY), (buttonsc.endX - m, buttonsc.endY), (255,255,255),10)

                try:
                    buttonsc.m+=(20 // buttonsc.button_time)
                    #print(m)
                except: pass



            else:
                buttonsc.m=0

        else:
            if buttonsc.pressed:
                for b in dropdown:
                    b.enable()

            else:
                for b in dropdown:
                    b.enable(enable=False)


class Button():
    def __init__(self,
                 button_sc,
                 img=None,
                 highlight = False,
                 shadow=False,
                 glimmer=False,
                 border = True
                 ):

        self.highlight=highlight
        self.shadow=shadow
        self.glimmer=glimmer
        self.border = border

        self.button_sc=button_sc
        self.coordinates = {
            'startX': button_sc.startX,
            'startY': button_sc.startY,
            'endX': button_sc.endX,
            'endY': button_sc.endY
        }

        self.size = (
            self.coordinates['endX'] - self.coordinates['startX']-2,
            self.coordinates['endY'] - self.coordinates['startY']-2,

                     )


        try: l = len(img)
        except: self.img= np.zeros((self.size[1],self.size[0],4))
        else:
            img = Controller().black_to_transparent(img)
            img = cv2.resize(img, self.size)
            self.img = img

        if border:
            self.img = cv2.copyMakeBorder(src=self.img, top=1,bottom=1,left=1,right=1,value=(255,255,255),borderType=cv2.BORDER_CONSTANT)

        #self.add_button_ui(img)
        self.name = self.button_sc.name
        self.active = self.button_sc.active
        self.m=0





    #idelly try to add a decorator here so that the function will be called when the logic button is dis/en abled
    def enable(self, enable=True):

        if enable:
            self.active=True
            self.button_sc.active = True
        else:
            self.active=False
            self.button_sc.active = False

    def add_text(self,text,color=(255,255,255),thickness=1,scale=1, align='mid'):


        try: l = len(self.img)
        except:self.img= np.zeros((self.size[1],self.size[0],4))

        SimpleUI().add_text(img=self.img, text=text, org=(self.size[0]+10, self.size[1]//2), scale=scale,
                     colour=color, thickness=thickness)


'''
since dropdown inherits from butto, it will be created in the same way and have the same funcs etc
in addition we will have a list of buttons that will apear and slide down once the dropdown ispressed

the buttons will remain as long as any part of the dropdown is being pressed
while the dropdown is not pressed, its buttons will be disabled

initialize the dropdown with the button that will trigger it
create buttons that the dropdown will have.
th sc must be added to the screen
the ui must be add to the dropdown
'''
class DropDown(Button):

    buttons = []

    def __init__(self,button,img=None,highlight=True,shadow=True):
        super(DropDown,self).__init__(button_sc=button,img=img,highlight=highlight,shadow=shadow)
        button.func = self.anim


    #creates a thread that will show all the buttons sliding down
    def anim(self,*args):
        x = threading.Thread(target=self.enable)
        x.start()

        # for b in self.buttons:
        #     a = threading.Thread(target=self.drop, args = (b,))
        #     a.start()

    def enable(self,*args):
        for b in self.buttons:
            b.enable()


    def add_button(self, button):
        self.buttons.append(button)
        button.button_sc.active=False

        #self.coordinates['endY']+=
        self.button_sc.endY += (button.coordinates['endY']- button.coordinates['startY'])

        # button.button_sc.active=False
        # button.active  = False


class Filter():


    def __init__(self,
                 img):

        self.img = img
        try:self.hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        except:pass

        self.func = {
            'BASIC_COLOR': self.basic_color,
            'GRADIENT_COLOR': self.gradient_color,
            'GRADIENT_COLOR_ENHANCE': self.gradient_color_enhance,
            'IMG_DILUTE': self.img_dilute,
            'COLOR_CONTRAST': self.color_contrast,
            'COLOR_BRIGHTEN': self.color_brighten
        }

        self.var ={
            'WHITE':(255,255,255,),
            'BLUE':(255,0,0)
        }


    def checkered(self,func,color,res=20):


        use = False
        for x in range(self.img.shape[1]-1):
            for y in range(self.img.shape[0]-1):

                if x%res==0:
                    use = not use
                try:self.func[func](x,y,use,self.var[color])
                except: self.func[func](x,y,use,color)


    def circular(self,func,color,radius_res=1,radius_range=(0,100,50),angle_res=5000):


        use = True
        for r in range(radius_range[0],radius_range[1],radius_range[2]):

            if r % radius_res == 0:
                use = not use

            if use:
            #for theta in range(0,5000,1):
                for theta in np.linspace(0,360,angle_res):
                    x,y = round(r*math.cos(math.degrees(theta))), round(r*math.sin(math.degrees(theta)))


                    try:self.func[func](x,y,use,self.var[color])
                    except:
                        try:self.func[func](x,y,use,color)
                        except:
                            self.img[x,y,0] = self.func[func](color[0],x+y)
                            self.img[x, y, 1] = self.func[func](color[1], x + y)
                            self.img[x, y, 2] = self.func[func](color[2], x + y)

    #draw full circles
    #each circle will have on whole colour
    #the color of each circle will brighten or contrast based on the var provided
    def circles(self, origin=(0,0), radius_range=(1,100,1),thickness=1,color=(255,0,0), b_func='COLOR_CONTRAST',g_func='COLOR_CONTRAST',r_func='COLOR_CONTRAST',var=2):

        c = list(color)
        for radius in range(radius_range[0],radius_range[1],radius_range[2]):
            b,g,r = self.func[b_func](c[0],radius/var), self.func[g_func](c[1],radius/var), self.func[r_func](c[2],radius/var)

            cv2.circle(self.img, origin,radius,(b,g,r),thickness)


    def color_contrast(self,color,var):
        return int(color *var)

    def color_brighten(self, color, var):
        return int(color + var)

   #will loop through some variable changing relevant colors each time to create agradient
    #options:
    #loop through radiuses
    #loop through angles
    #loop through centers
    def circle_pattern(self,centre, axis, angle,start_angle,end_angle, color, thickness, mode,range):

        options ={
            'centre': 'j'
        }

        for i in range(range[0], range[1], range[2]):
            cv2.ellipse(self.img,
                        centre,
                        axis,
                        angle, start_angle, end_angle,
                        color, thickness)

    def basic_color(self,x,y,use,color):
        if use:
            try:self.img[y,x]= color
            except: self.img[y,x]=color+(0,)

    def gradient_color(self,x,y,use,color):
        if use:
            b  = int((x+y) % 255)
            r = int((x*y) % 255)
            g=abs(r-b)
            try:self.img[y,x]=(b,g,r)
            except: self.img[y,x]=color+(0,)



    def gradient_color_enhance(self,x,y,use,color):
        if use:
            b  = int((x+y) % 255)
            r = int((x*y) % 255)
            g=abs(r-b)
            try:
                self.img[y,x,2]=self.img[y,x,2] *1.5

            except: self.img[y,x]=color+(0,)


    def img_dilute(self,x,y,use,col):
        if use:
            try:self.hsv_img[y,x,1]=self.img[y,x,1]+50
            except: self.hsv_img[y,x]=col+(0,)


def hello(*args):
    try:tuya_controller().kitchen_toggle()
    except:print('probably no internet')


def open_lights(*args):
    try:tuya_controller().open_toggle()
    except:print('probably no internet')


def ac_funcs(*args):

    try:
        print(args)
        tuya_controller().ac_remote(args[0])
    except:print('probably no internet')


def next_room(*args):
    print('hooray')

def recog(*args):
    print(args[0])
    time.sleep(2)
    args[0].csn='media'



if __name__ == '__main__':


    #cap = cv2.VideoCapture("/dev/video2")
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = hl.handDetector()
    controller = sc.Controller()


    ui_controller = Controller()

    #create ui screen
    ui = Screen()




    #create sc screen
    main_screen = sc.Screen(name = 'start')
    m_screen = sc.Screen(name='media')

    no_recognise= sc.Screen(name='no recognise')
    thumbs_up = sc.Gesture(gesture=[0,1,0,0,0], func=controller.move_to_screen, args='media')
    main_screen.add_gesture(thumbs_up)

    back= sc.Gesture(gesture=[1,1,1,1,1], func=ui_controller.back)
    m_screen.add_gesture(back)
    main_screen.add_gesture(back)

    with open('/home/yaron/PycharmProjects/SmartController/button_variables/kitchen_lights.pkl',
              'rb') as f:  # Python 3: open(..., 'rb')
        coordinates = pickle.load(f)

    with open('/home/yaron/PycharmProjects/SmartController/button_variables/open_lights.pkl',
              'rb') as f:  # Python 3: open(..., 'rb')
        open_coordinates = pickle.load(f)

    with open('/home/yaron/PycharmProjects/SmartController/button_variables/ac_lights.pkl',
              'rb') as f:  # Python 3: open(..., 'rb')
        ac_coordinates = pickle.load(f)


    fin_1=cv2.imread('/home/yaron/PycharmProjects/SmartController/images/ges_images/1.jpg')
    fin_1=ui.black_to_transparent(fin_1)

    im_start=(100,100)
    ui.add_image_to_canvas(fin_1,im_start,size=(100,100))

    face_img=cv2.imread('/home/yaron/PycharmProjects/SmartController/images/ges_images/gun.jpg')
    face_img=ui.black_to_transparent(face_img)

    face_start=(500,500)
    ui.add_image_to_canvas(face_img,face_start,size=(100,100))


    #create sc buttons
    button  = sc.Button(func=hello, startX=coordinates[0], startY=coordinates[1], endX=coordinates[2], endY=coordinates[3])


    open_button = sc.Button(func=open_lights, startX=open_coordinates[0], startY=open_coordinates[1], endX=open_coordinates[2],
                       endY=open_coordinates[3], name ='open_lights')


    ac_button = sc.Button(func=ac_funcs, startX=ac_coordinates[0], startY=ac_coordinates[1], endX=ac_coordinates[2],
                       endY=ac_coordinates[3], name ='ac')


    '''
    NOTICE:
    I have edited the size of the button by changing the coordiantes of the end x
    this will effect both the image size(if it exists) and the button size
    I must think of a way to better manipulate the size of the buttons and maybe even differenciate between the image
    size and logic size
    '''
    hot_ac_button = sc.Button(func=ac_funcs, startX=ac_coordinates[0], startY=ac_coordinates[1]+50, endX=ac_coordinates[2]-80,
                       endY=ac_coordinates[3]+50, name ='hot_ac')

    cold_ac_button = sc.Button(func=ac_funcs, startX=ac_coordinates[0], startY=ac_coordinates[1]+100, endX=ac_coordinates[2]-80,
                       endY=ac_coordinates[3]+100, name ='cold_ac', args='on_cold')

    off_ac_button = sc.Button(func=ac_funcs, startX=ac_coordinates[0], startY=ac_coordinates[1]+150, endX=ac_coordinates[2]-80,
                       endY=ac_coordinates[3]+150, name ='off_ac',args='off')


    start_ges_l= Gesture('all_off_start')

    start_ges_l.gesture_time=0
    end_ges_l= Gesture('all_off_end')

    end_ges_l.gesture_time=0

    all_off_ges = Movement(start_ges_l,end_ges_l,tuya_controller().all_off)
    main_screen.add_gesture(all_off_ges)


    start_ges_s= Gesture('swipe_left_start')

    start_ges_s.gesture_time=0
    end_ges_s= Gesture('swipe_left_end')

    end_ges_s.gesture_time=0

    swipe_left = Movement(start_ges_s,end_ges_s,func=ui_controller.move_to_screen,args='media')
    main_screen.add_gesture(swipe_left)
    #main_screen.add_gesture(start_ges_s)


    #add buttons to sc screen
    main_screen.add_button(button)
    main_screen.add_button(open_button)
    main_screen.add_button(ac_button)

    #create ui buttons using the ac buttons
    button_ui = Button(button,highlight=False,shadow=False)
    open_button_ui = Button(open_button,highlight=False,shadow=False)
    #ac_button_img =cv2.imread('cold_b.png',-1)
    #ac_button_ui = Button(ac_button)#, img = ac_button_img,highlight=False,shadow=False)

    cold_img = cv2.imread('cold_n_t.png')
    cold_img= ui.black_to_transparent(cold_img)
    #cv2.imshow('cold', cold_img)

    hot_img = cv2.imread('hot_n_t.png')
    hot_img= ui.black_to_transparent(hot_img)

    off_img = cv2.imread('off.png')
    off_img= ui.black_to_transparent(off_img)
    #cv2.imshow('cold', cold_img)

    drop_down= DropDown(ac_button,highlight=False,shadow=False)
    #drop_down.glimmer=False
    drop_down.button_sc.button_time=0
    hot_ac_ui = Button(hot_ac_button, img=hot_img,highlight=False,shadow=False,glimmer=False)
    cold_ac_ui = Button(cold_ac_button,img=cold_img,highlight=False,shadow=False, glimmer=False)
    off_ac_ui = Button(off_ac_button, img=off_img, highlight=False, shadow=False, glimmer=False)
    main_screen.add_button(cold_ac_button)
    main_screen.add_button(hot_ac_button)
    main_screen.add_button(off_ac_button)
    drop_down.add_button(hot_ac_ui)
    drop_down.add_button(cold_ac_ui)
    drop_down.add_button(off_ac_ui)


    #add the ui buttons to the ui screen
    ui.add_button(drop_down)
    ui.add_button(button_ui)
    ui.add_button(open_button_ui)
    #ui.add_button(ac_button_ui)


    media_screen = Screen()

    # music = sc.Gesture(gesture=[1,1,0,0,1], func = yt.voiceSearch)
    # m_screen.add_gesture(music)

    couch = sc.Gesture(gesture=[0,1,0,0,0],func=tuya_controller().couch_toggle)
    #m_screen.add_gesture(couch)

    open = sc.Gesture(gesture=[0,1,1,0,0],func=tuya_controller().open_toggle)
    m_screen.add_gesture(open)

    kitchen = sc.Gesture(gesture=[0,1,1,1,0],func=tuya_controller().kitchen_toggle)
    m_screen.add_gesture(kitchen)

    gun = Gesture('point_gun', func = next_room)
    m_screen.add_gesture(gun)

    kill_start = Gesture('kill', func = next_room)


    kill_end =Gesture('nope',func=next_room)
    kill_end.model = kill_end.load_model(file_path='/home/yaron/PycharmProjects/SmartController/datasets/kill_finalized_model.sav')

    kill = Movement(kill_start,kill_end,next_room)

    m_screen.add_gesture(kill)



    #add sc screen to controller
    controller.add_screen(main_screen)
    controller.add_screen(m_screen)

    ui_controller.add_screen(media_screen, )
    ui_controller.add_screen(ui,)



    cv2.namedWindow('screen', 0x00000000)



    while True:

        #get info about hand
        # success, img = cap.read()
        # img = cv2.flip(img, 1)

        # img, lmListR, lmListL, handedness = detector.get_info(img)
        #
        # if len(lmListR) != 0 or len(lmListL) != 0:
        #     cv2.circle(img,(400,400),50, (0,255,0),-1)
        #     fingers = detector.fingerCounter()
        #
        #     if handedness=='Right':
        #         x, y = lmListR[8][1], lmListR[8][2]
        #
        #     elif handedness == 'Left':
        #         x, y = lmListL[8][1], lmListL[8][2]

            #screen = ui.run(x,y,controller)
            #controller.run([],detector,x,y)
            #cv2.setWindowProperty('screen', 0, 1)

            #cv2.imshow('screen',screen)
        #
        # else:
        #     cv2.setWindowProperty('screen', 0, 0)
        #
        #     x,y=0,0


        screen = np.zeros((320,320))
        #screen = ui.run(x,y, controller)
        #screen = ui_controller.screens[ui_controller.current_screen].run(x,y,img)
        cv2.imshow('screen', screen)
        #cv2.imshow('img',img)



        #print(controller.csn)


        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cap.release()
        #     cv2.destroyAllWindows()
        #     break

        cv2.waitKey(1)
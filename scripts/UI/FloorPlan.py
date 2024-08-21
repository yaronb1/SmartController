'''
the cursor module will allow the user to use his fingers as a virtual pointer and click elements

It must work in sync with the smart controller . main and be added seemlessly

'''

import cv2
import numpy as np
import time

from scripts.detectors import handLandmarks as hl
from definitions.config import ROOTDIR
import os

from scripts.controllers import HAController as HA

import asyncio


#this func gets 2 images as input
# they do not have to be of the same size, the foreground must have an alpha chanel
#it will put the foreground on the bg with the x,y offset
def add_transparent_image(bg, foreground, x_offset=None, y_offset=None):
    background = bg.copy()
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
    assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

    # center by default
    if x_offset is None: x_offset = (bg_w - fg_w) // 2
    if y_offset is None: y_offset = (bg_h - fg_h) // 2

    w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
    h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

    if w < 1 or h < 1: return bg

    # clip foreground and background images to the overlapping regions
    bg_x = max(0, x_offset)
    bg_y = max(0, y_offset)
    fg_x = max(0, x_offset * -1)
    fg_y = max(0, y_offset * -1)
    foreground = foreground[fg_y:fg_y + h, fg_x:fg_x + w]
    background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

    # separate alpha and color channels from the foreground image
    foreground_colors = foreground[:, :, :3]
    alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

    # construct an alpha_mask that matches the image shape
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # combine the background with the overlay image weighted by alpha
    composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

    # overwrite the section of the background image that has been updated
    background[bg_y:bg_y + h, bg_x:bg_x + w] = composite


    return background

#the controller is intended to take care of all the ui
# ,must pass a hand detector
# images for the floor plan
# and a general bg
class Controller():


    def __init__(self,
                hand_detector= None,
                show_webcam=False,
                images = {},
                bg = None,

                ):


        self.bg_original = bg
        self.bg_icons=self.bg_original.copy()
        self.bg_floorplan = self.bg_original.copy()
        self.bg_final = self.bg_original.copy()
        self.images = images
        #self.aspect_ratio = aspect_ratio

        #self.cache = cache
        self.aspect_ratio = bg.shape[1] / bg.shape[0]

        if hand_detector is not None:
            self.hand_detector = hand_detector
        else:
            self.hand_detector = hl.handDetector()

        self.cap =cv2.VideoCapture(0)

        webcam_width = 340
        webcam_height = 340//self.aspect_ratio
        #webcam_height=124
        self.cap.set(3,webcam_width)
        self.cap.set(4,webcam_height)

        self.show_webcam=show_webcam

        self.pTime, self.cTime = 0,0


    #the run method must be part of a while loop
    #takes care of the handdetector logic, cv.imshow logic
    # and displays the bg_final
    def run(self):


        success, img = self.cap.read()
        img = cv2.flip(img, 1)

        self.img, self.lmListR, self.lmListL, self.handedness = self.hand_detector.get_info(img)


        try:cv2.imshow('bg',self.bg_final )
        except: print(self.bg_final)


        self.cTime = time.time()
        self.fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime
        cv2.putText(img, str(int(self.fps)), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (0, 0, 0), 1)


        if self.show_webcam:
            cv2.imshow('img', img)



    #this func will be called once when a light is turned on or off
    # to update the lights that must be displayed on the bg
    # name of the light and new state of that light must be passed
    # it will update the self.images dict and call the get Image with the new dict to update
    #the bg_floorplan image
    # def update_floorplan(self, name, state):
    #
    #     new_val = (self.images[name][0],state)
    #
    #
    #     self.images[name] = new_val
    #
    #
    #     return self.get_image()

    def update_img(self):
        self.bg_floorplan = self.bg_icons.copy()

        for img,state in self.cache.items():


            print(f'state of {img} is {state}')
            if state =='on':
                self.bg_floorplan = add_transparent_image(self.bg_floorplan,self.images[img])

        return self.bg_floorplan



    # get image starts by creatng a blank bg_icons
    # it then displays the images from the images dict if their respective light is on state
    # def get_image(self):
    #     self.bg_floorplan = self.bg_icons.copy()
    #
    #     for img,state in self.images.values():
    #
    #
    #
    #         if state:
    #             self.bg_floorplan = add_transparent_image(self.bg_floorplan,img)
    #
    #     return self.bg_floorplan

    #use this func to add button to floorplan ui
    #must return a button object to add to smartcontroller
    def add_button(self,x,y,size,func,icon ='light'):

        #create button object

        nx, ny = int(x /(self.aspect_ratio * 2)), int(y / (self.aspect_ratio * 2))
        sizea = size//(self.aspect_ratio*2)

        button = SmartController.Button(startX=nx, endX=nx+sizea, startY=ny,
                                        endY=ny+sizea, func=light_toggle, args='kitchen')

        #add ui
        self.add_icon(icon,x,y,size)

        return button


    # when adding a button this func will be called to add the icon to the bg_icons img
    def add_icon(self,icon,x,y,size):


        #bg = cv2.imread(os.path.join(ROOTDIR, 'images', 'Dark.png'))

        icon = cv2.imread(os.path.join(ROOTDIR, 'images','icons', str(icon) +'.png'),-1)

        icon = cv2.resize(icon,(size,size))

        self.bg_icons = add_transparent_image(self.bg_icons,icon,x,y)
        self.bg_final= self.bg_icons.copy()
        self.bg_floorplan = self.bg_icons.copy()



        return self.bg_icons


# honeycomb is a ui controller with hexagon style buttons displayed like honeycombs
class HoneyComb(Controller):

    def __init__(self,
                 hand_detector=None,
                 show_webcam=False,
                 images={},
                 bg=None,
                 ):
        super(HoneyComb, self).__init__(hand_detector=hand_detector,
                                        show_webcam=show_webcam,
                                        images=images,
                                        bg=bg)

        self.buttons = {}
        self.start = 0
        self.bg_buttons = self.bg_floorplan.copy()

    #
    # def run(self):
    #     super (HoneyComb,self).run()
    #
    #     # for b in self.buttons.values():
    #     #     but = b['object']
    #     #     if but.pressed:
    #     #         pressed = True
    #     #         break
    #     #
    #     #     else:
    #     #         pressed = False
    #     #
    #     # if not(pressed):
    #     #     self.start = 0
    #     #     self.floorplan = self.get_image()




    # call this func when adding a new button
    # it will cfeate the sc.button object and call button ui when the button is pressed
    #once the button is fully pressed the func will be called with the args
    def add_button(self,name,x,y,size,func,args,icon ='light', sub_menu = False):

        nx, ny = int(x /(self.aspect_ratio * 2)), int(y / (self.aspect_ratio * 2))
        sizea = size//(self.aspect_ratio*2)


        '''
        not complete
        '''
        if sub_menu:
            self.menu_start = False
            self.menu_timeout=1
            button = SmartController.Button(startX=nx-10, endX=nx+sizea-10, startY=ny-3,
                                        endY=ny+sizea-3, func=self.button_menu, args=(name,func,args), button_time=0)

        else:
            # create the button object such as that the function called is the ui handler
            # once the ui is done and the button is fully pressed, the func var passed will be called along with args
            button = SmartController.Button(startX=nx-10, endX=nx+sizea-10, startY=ny-3,
                                        endY=ny+sizea-3, func=self.button_ui, args=(name,func,args), button_time=0)


        self.buttons[name] = {}
        self.buttons[name]['object'] = button


        #add ui
        self.create_button(name,x+10,y-10,size-60,)
        self.add_icon(icon,x,y,size)



        return button


    # puts the button ui on the bg_icons
    def create_button(self,name,x=0,y=0,size=20):


        pts = np.array([
            [0+x,size+y], [size+x,int(0.5*size)+y], [2*size+x,size+y], [2*size+x,2*size+y], [size+x, int(2.5*size)+y], [0+x,2*size+y],
        ],
            np.int32

        )

        self.buttons[name]['points'] =pts

        #pts = pts.reshape((-1, 1, 2))

        isClosed = True

        # Green color in BGR
        color = (255, 255, 255)

        self.buttons[name]['color'] = color

        # Line thickness of 8 px
        thickness = 2

        # Using cv2.polylines() method
        # Draw a Green polygon with
        # thickness of 1 px
        self.bg_icons = cv2.polylines(self.bg_icons, [pts],
                              isClosed, color,
                              thickness)

        self.bg_final= self.bg_icons.copy()
        self.bg_floorplan = self.bg_icons.copy()



        return self.bg_icons


    # is called while the button is pressed
    # displays some way to show the user the buuton is intercated with
    # in bg_floorplan
    # if the button has been pressed for more than a certain period of time
    # call the func with the args
    def button_ui(self,args):
        name = args[0]
        func = args[1]
        arg = args[2]


        self.bg_floorplan = cv2.fillPoly(self.bg_floorplan,[self.buttons[name]['points']],(0,self.start+50,0))

        self.start +=10

        if self.start>=200:
            func(arg)
            self.start = 0

    '''
    not complete
    '''
    # while the sub menu is pressed the sub menu nedds to be displayed on bg_floorplan
    def button_menu(self):

        if not(self.menu_start):
            self.add_button(name='test', x=100,y=100,size=100,func = lambda: print('test'), args = None)
            self.menu_start = True
        self.menu_time = 0










#this class allows the usere to see his hand inside the ui
#with some ui image- cursor img
# the cursor will follow his hand based on the x, y value passed
class Cursor():

    def __init__(self,
                 bg=None,
                 cursor_img=None,
                 ):


        self.bg = bg

        #self.bg = cv2.imread(os.path.join(ROOTDIR, 'images', 'Dark.png'))

        self.aspect_ratio= self.bg.shape[1]/self.bg.shape[0]



        self.cursor = cursor_img

        self.smoother = 20


    #x,y the coordinate of the cursor
    # return set image for smartcontroller to display
    # must run part of the while loop
    def run(self,bg, x,y):



        img = bg.copy()
        nx,ny = self.normalise_xy(x,y)

        #need to find a way to create this logic for any variation of buttons
        if nx > 800:
            nx = 1200
        else:
            nx = 600
        if ny > 250:
            ny = 400
        else:
            ny = 100
        bg = add_transparent_image(img,self.cursor,nx,ny)
        return bg


    #this func is meant to return a relative xy value based on the bg
    #the webcam and bg should have the same aspect ratio which the controller will handle
    # and in this function we will scale th x y value of the hand taken from the webcam to match the bg value

    #@args x, y from the webcam,
    #return the scaled value of x,y for the bg
    def normalise_xy(self,x,y):
        nx, ny= int(x*self.aspect_ratio*2),int(y*self.aspect_ratio*2)
        #nx,ny = x,y
        nx,ny =  self.smoother * round(nx / self.smoother), self.smoother * round(ny / self.smoother)

        return nx,ny










if __name__ == '__main__':


    images = {

        'light.bar_bot_right':cv2.imread(os.path.join(ROOTDIR, 'images','floor_plan', 'kitchen_bulb.png'),-1),
        'light.bar_bot_left':cv2.imread(os.path.join(ROOTDIR, 'images','floor_plan', 'bathroom.png'), -1)
    }



    def light_toggle(light):

        print(f'toggle {light} light')
        state = not(controller.images[light][1])
        img = controller.update_floorplan(light,state)

    # the open menu func will display the respective menu of the button for a certaon period of time
    def open_menu():
        pass


    from scripts.controllers import SmartController
    from definitions.Secrets import docker_token as token
    bg = cv2.imread(os.path.join(ROOTDIR, 'images','floor_plan', 'Dark.png'))

    controller = HoneyComb(show_webcam=True,bg=bg,images=images)
    ha_controller = HA.HAController(host = "192.168.58.247", token = token, entities=['light.bar_bot_right', 'light.bar_bot_left'],event_func=controller.update_img)

    cursor = cv2.imread(os.path.join(ROOTDIR, 'images','floor_plan', 'cursor.png'),-1)


    # create the ui controller with honeycomb

    controller.cache = ha_controller.cache




    #logic controller
    #and a default screen
    lc = SmartController.Controller()
    ds = SmartController.Screen(name = 'default')

    # create a button using the honeycombs add_button method
    #whic will add the icon and return a sc.button object to add to the smartcontroller
    b1 = controller.add_button(name= 'b1',x=1200,y=400,size=100,func=lambda : print("ok"), args=('light.kitchen_bulb','toggle'))


    b2 = controller.add_button(name='b2',x=1200,y=100,size=100,func=lambda arg: print('success'),args='bathroom', sub_menu=True)
    #b3 = controller.add_button(name='b3' ,x=600, y=400, size=100, func=light_toggle, args='bathroom')
    b3 = controller.add_button(name='b3', x=600, y=400, size=100, func=lambda: print('hey'), args=('light.kitchen_bulb','toggle'))
    ds.add_button(b1)
    ds.add_button(b2)
    ds.add_button(b3)




    lc.add_screen(ds)




    # create the cursor object
    curs = Cursor(bg = bg, cursor_img = cursor)


    #toggle a light to init the first image
    ha_controller.light(('light.bar_bot_left','toggle'))
    ha_controller.light(('light.bar_bot_left', 'toggle'))


    # the while loop will run controller.run
    # grab the appropreate x,y, values from the detector
    # run the lc.run
    #update the controller.bg_final using cursor.run
    async def ui():

        await asyncio.sleep(2)
        # toggle a light to init the first image
        ha_controller.light(('light.bar_bot_left', 'toggle'))
        ha_controller.light(('light.bar_bot_left', 'toggle'))


        while True:

            #bg = fp.updated_b
            controller.run()

            # print(controller.cache)
            await asyncio.sleep(0.1)

            if len(controller.lmListR)!=0:
                x,y, = controller.lmListR[8][1],controller.lmListR[8][2]

                lc.run(args=[],detector=controller.hand_detector,x=x,y=y)
                controller.bg_final = curs.run(controller.bg_floorplan,x,y)

            else:
                controller.bg_final = controller.bg_floorplan

                #print(x,y)




            if cv2.waitKey(1) and 0xFF == ord('q'):
                break


    async def main():
        listen = asyncio.create_task(ha_controller.initSocket())
        #log = asyncio.create_task(HA.initLogger())
        cam= asyncio.create_task(ui())
        await listen
        # await log
        await cam
    #asyncio.run(HA.state_listener())
    asyncio.run(main())


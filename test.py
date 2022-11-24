import os
import SmartController as sc
import cv2
import dill as pickle
import handLandmarks as hl
import UIMain as UI
import time

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Start():

    def __init__(self,
                 width= 1280,
                 height = 720,
                 profile = 'default',
                 rootdir='/home/yaron/PycharmProjects/SmartController/custom_screens'
                 ):

        self.detector= hl.handDetector()

        self.width =width
        self.height = height

        profile = profile
        self.rootdir = rootdir


        try:
            with open('/home/yaron/PycharmProjects/SmartController/profiles/' + profile +  '/variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
                self.controller = pickle.load(f)
        except: self.controller = sc.Controller()
        self.controller.move_to_screen('home')
        self.cap = cv2.VideoCapture(-1)
        self.cap.set(3,self.width)
        self.cap.set(4,self.height)

    def run_main(self):


        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)

            img, lmListR, lmListL, handedness = self.detector.get_info(img)
            #screen = controller.screens[controller.cs]
            screen = self.controller.screen_dict[self.controller.csn]

            if len(lmListR)!=0 or len(lmListL)!=0:
                fingers = self.detector.fingerCounter()
                if fingers == [0, 1, 1, 0, 0]:  # selectmode
                    if handedness == 'Right':
                        x, y = lmListR[8][1], lmListR[8][2]
                    elif handedness == 'Left':
                        x, y = lmListL[8][1], lmListL[8][2]
                else:
                    x, y = 0, 0
                self.controller.run([], detector = self.detector, x=x, y=y)


            imgUI = self.controller.overlay_transparent(img,screen.ui[0],0,0)

            cv2.imshow('img', imgUI)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cap.release()
                cv2.destroyAllWindows()
                break


if __name__ =='__main__':


    #create webcam vars
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)


    #create hand detectctor, controller and ui objects
    detector = hl.handDetector()
    logic_controller = sc.Controller()
    ui_controller = UI.Controller()
    sui = UI.SimpleUI()

    recognise_uiscreen = UI.Screen(background_img='', name= 'recognise', show_cursor=False)
    recognise_scscreen = sc.Screen(name='recognise')

    filter = UI.Filter(img = recognise_uiscreen.background)

    filter.circular(func='COLOR_CONTRAST',color=(255,0,100),radius_res=50,radius_range=(0,500,10))

    trigger = sc.Gesture(gesture =[1,1,1,1,1], func = logic_controller.move_to_screen,args='start')

    recognise_scscreen.add_gesture(trigger)
    recognise_uiscreen.add_image_to_canvas(img = cv2.imread(ROOT_DIR + "/images/ges_images/5f.jpg"),
                                           coordinates=(recognise_uiscreen.background.shape[0]//2, recognise_uiscreen.background.shape[1]//2), size=(100,100))
    logic_controller.add_screen(recognise_scscreen)
    ui_controller.add_screen(recognise_uiscreen)



    #create start screen
    start_ui_screen =  UI.Screen(background_img='',name= 'start')
    start_sc_screen  = sc.Screen(name='start')

    #
    filter = UI.Filter(img = start_ui_screen.background)

    filter.circular(func='COLOR_CONTRAST',color=(255,0,0),radius_res=50,radius_range=(0,500,10))

    new_profile_scbutton = sc.Button(func = logic_controller.move_to_screen,startX=450,endX=700,startY=300,endY=600, args='new_profile')
    new_profile_uibutton = UI.Button(new_profile_scbutton,highlight=False,shadow=False,glimmer=False,border=False)



    filter.img = new_profile_uibutton.img
    #filter.circular(func='BASIC_COLOR',color=(255,0,0),radius_res=10,radius_range=(0,100,10))
    filter.circles(radius_range=(60,100,2),thickness=5,origin=(filter.img.shape[1]//2,filter.img.shape[0]//2),color=(255,0,0),var =0.2)


    cv2.putText(new_profile_uibutton.img, '+', (110, new_profile_uibutton.size[1] // 2),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 100, 0), 5)

    cv2.putText(new_profile_uibutton.img, 'Profile', (100, new_profile_uibutton.size[1] // 2+20),
                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 0), 2)



    start_ui_screen.add_button(new_profile_uibutton)
    start_sc_screen.add_button(new_profile_scbutton)

    logic_controller.add_screen(start_sc_screen)
    ui_controller.add_screen(start_ui_screen)



    #new profile screen
    new_profile_scscreen= sc.Screen(name='new_profile')
    new_profile_uiscreen= UI.Screen(name='new_profile',background_img='')
    #
    filter = UI.Filter(img = new_profile_uiscreen.background)
    #filter.circular(func='COLOR_CONTRAST', color=(255, 100, 10), radius_res=50, radius_range=(0, 700, 10))



    #room flow chart section
    cv2.putText(new_profile_uiscreen.background, 'Rooms Chart', (10,40), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1)

    add_room_scbutton = sc.Button(startX=450,endX=570,startY=30,endY=60)
    add_room_uibutton = UI.Button(add_room_scbutton,highlight=False,shadow=False,glimmer=False,border=False,)

    cv2.putText(add_room_uibutton.img, '+Add Room', (10, 17), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)

    gestures_scbutton = sc.Button(startX=450,endX=570,startY=100,endY=150)
    gesture_uibutton =UI.Button(gestures_scbutton, img=cv2.imread(ROOT_DIR + '/images/ges_images/gun.jpg'))
    ges_1_scbutton = sc.Button(startX=450,endX=570,startY=150,endY=200)
    ges_1_uibutton = UI.Button(ges_1_scbutton, img=cv2.imread(ROOT_DIR + '/images/ges_images/1.jpg'))
    ges_2_scbutton = sc.Button(startX=450,endX=570,startY=200,endY=250)
    ges_2_uibutton = UI.Button(ges_2_scbutton, img=cv2.imread(ROOT_DIR + '/images/ges_images/2.jpg'))


    gesture_options = UI.DropDown(gestures_scbutton,img=cv2.imread(ROOT_DIR + '/images/ges_images/gun.jpg'))#create the dropdown with the main sc button
    gesture_options.add_button(ges_1_uibutton)#add the ui button options to the dropdown
    gesture_options.add_button(ges_2_uibutton)

    new_profile_uiscreen.add_button(gesture_options)#add the dropdown to the ui screen
    new_profile_scscreen.add_button(ges_1_scbutton)#add the sc buttons to the sc screen
    new_profile_scscreen.add_button(ges_2_scbutton)
    new_profile_uiscreen.add_button(ges_2_uibutton)


    new_profile_scscreen.add_button(add_room_scbutton)
    new_profile_uiscreen.add_button(add_room_uibutton)


    logic_controller.add_screen(new_profile_scscreen)
    ui_controller.add_screen(new_profile_uiscreen)

    logic_controller.csn = 'new_profile'

    cv2.namedWindow('screen', 0x00000000)
    while True:

        success, img = cap.read()

        img = cv2.flip(img, 1)

        img, lmListR, lmListL, handedness = detector.get_info(img)

        if len(lmListR) != 0 or len(lmListL) != 0:
            cv2.circle(img,(400,400),50, (0,255,0),-1)
            fingers = detector.fingerCounter()

            if handedness=='Right':
                x, y = lmListR[8][1], lmListR[8][2]

            elif handedness == 'Left':
                x, y = lmListL[8][1], lmListL[8][2]


        else: x,y=0,0

        screen = ui_controller.screens[logic_controller.csn].run(x, y, img)
        logic_controller.run([], detector, x, y)

        cv2.imshow('screen', screen)
        #cv2.imshow('img',img)

        cv2.setWindowProperty('screen', 0, 1)

        #print(controller.csn)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


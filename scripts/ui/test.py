import os
import scripts.controllers.SmartController as sc
import cv2
import dill as pickle
import scripts.detectors.handLandmarks as hl
import UIMain as UI
import time
from deprecated.Tuya import Controller as tuya

from scripts.controllers.Spotify import Spotify



from scripts.controllers.SocketController import PiController
from scripts.detectors.Gestures import Movement

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


def open_spotify(*args):
    global spotify_controller
    spotify_controller = Spotify()
    spotify_controller.open_spotify()
    print('opened')

def play(*args):
    global spotify_controller
    spotify_controller.remote()
    print('play')

def test_func(*args):
    print('hooray')

if __name__ =='__main__':



    def start_variables():

        global cap
        global detector
        global logic_controller
        global ui_controller
        global sui

        global bar_controller

        global tuya_controller


        # create webcam vars
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        # create hand detectctor, controller and ui objects
        detector = hl.handDetector()
        logic_controller = sc.Controller()
        ui_controller = UI.Controller()
        sui = UI.SimpleUI()
        bar_controller = PiController(connect=False)
        try:tuya_controller = tuya()
        except Exception as e:
            print (e)
            tuya_controller=None


    def create_sc_screens():
        #recognise screen
        recognise_scscreen = sc.Screen(name='recognise')

        #start screen
        start_sc_screen = sc.Screen(name='start',timeout=2)

        # new profile screen
        new_profile_scscreen = sc.Screen(name='new_profile')

        #moods screen
        moods_scscreen = sc.Screen(name = 'moods')

        return {
            'recognise': recognise_scscreen,
            "start" : start_sc_screen,
            "new profile": new_profile_scscreen,
            "moods": moods_scscreen

        }



    def create_ui_screens():

        #recognise screen
        recognise_uiscreen = UI.Screen(background_img='', name='recognise', show_cursor=False)
        filter = UI.Filter(img=recognise_uiscreen.background)
        filter.circular(func='COLOR_CONTRAST', color=(255, 0, 100), radius_res=50, radius_range=(0, 500, 10))


        #start screen
        start_ui_screen = UI.Screen(background_img='', name='start',timeout=2)
        filter = UI.Filter(img=start_ui_screen.background)
        filter.circular(func='COLOR_CONTRAST', color=(255, 0, 0), radius_res=50, radius_range=(0, 500, 10))


        new_profile_uiscreen = UI.Screen(name='new_profile', background_img='')
        filter = UI.Filter(img=new_profile_uiscreen.background)
        # room flow chart section
        cv2.putText(new_profile_uiscreen.background, 'Rooms Chart', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0),1)

        moods_uiscreen = UI.Screen(background_img='', name='moods')

        return {
            "recognise": recognise_uiscreen,
            "start": start_ui_screen,
            "new profile": new_profile_uiscreen,
            "moods": moods_uiscreen
        }


    '''
    logic + ui
    add them to screens
    '''
    def create_gestures(sc_screens, ui_screens):
        #
        # # snap_ges = Movement(gesture=Gesture(name='snap'), func=lambda :print('snap'))
        # # sc_screens["recognise"].add_gesture(snap_ges)
        # #
        # # snap300_ges = Movement(gesture=Gesture(name='snap300'), func=lambda :print('snap300'))
        # # sc_screens["recognise"].add_gesture(snap300_ges)
        # #
        # # snap_start = Gesture(name = 'snap', func = lambda :print('start snap'))
        # # sc_screens["recognise"].add_gesture(snap_start)
        #
        # all_off_ges = Movement(start_ges=Gesture(name='all_off_start'),end_ges=Gesture(name='all_off_end'), func=lambda :print('all_off'))
        # sc_screens["recognise"].add_gesture(all_off_ges)
        #
        # trigger = sc.Gesture(gesture=[1, 1, 1, 1, 1], func=logic_controller.move_to_screen, args='start')
        # sc_screens["recognise"].add_gesture(trigger)
        #
        # open_spotify_ges = sc.Gesture(gesture=[0,1,0,0,0], func= open_spotify)
        # sc_screens["recognise"].add_gesture(open_spotify_ges)
        #
        # play_spot_ges = sc.Gesture(gesture=[0,1,1,0,0], func= play)
        # sc_screens["recognise"].add_gesture(play_spot_ges)
        # # recognise_uiscreen.add_image_to_canvas(img=cv2.imread(ROOT_DIR + "/images/ges_images/5f.jpg"),
        # #                                        coordinates=(recognise_uiscreen.background.shape[0] // 2,
        # #                                                     recognise_uiscreen.background.shape[1] // 2),
        # #                                        size=(100, 100))
        #
        # ui_screens['recognise'].add_image_to_canvas(img=cv2.imread(ROOT_DIR + "/images/ges_images/5f.jpg"),
        #                                        coordinates=(ui_screens['recognise'].background.shape[0] // 2,
        #                                                     ui_screens['recognise'].background.shape[1] // 2),
        #                                        size=(100, 100))
        #
        #
        #
        # #move to mood screen ges
        # moods_ges = sc.Gesture(gesture= [0,1,1,0,0], func = logic_controller.move_to_screen, args='moods')
        # sc_screens['start'].add_gesture(moods_ges)
        #
        # ui_screens['start'].add_image_to_canvas(img=cv2.imread(ROOT_DIR + "/images/ges_images/2.jpg"),
        #                                         coordinates=(10,10),
        #                                         size=(100, 100)
        #                                         )
        # cv2.putText(ui_screens['start'].background, 'MOODS', (20,120),
        #             cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 0), 2)
        #
        #
        #
        #
        # bar_purple_ges = sc.Gesture(gesture= [0,1,0,0,0], func = Moods.purple, args=(bar_controller,tuya_controller))
        # sc_screens['moods'].add_gesture(bar_purple_ges)
        #
        # ui_screens['moods'].add_image_to_canvas(img=cv2.imread(ROOT_DIR + "/images/ges_images/1.jpg"),
        #                                         coordinates=(10,10),
        #                                         size=(100, 100)
        #                                         )
        #
        #
        # bar_blue_ges = sc.Gesture(gesture= [0,1,1,0,0], func = Moods.blue, args=(bar_controller,tuya_controller))
        # sc_screens['moods'].add_gesture(bar_blue_ges)
        #
        # ui_screens['moods'].add_image_to_canvas(img=cv2.imread(ROOT_DIR + "/images/ges_images/2.jpg"),
        #                                         coordinates=(10,150),
        #                                         size=(100, 100)
        #                                         )

        ges = Movement(name='fan', func= lambda : print('fan'))
        sc_screens['recognise'].add_gesture(ges)









    """
    logic + ui
    add them to screens
    """
    def create_buttons(sc_screens,ui_screens):

        #start screen

        #new profile button
        new_profile_scbutton = sc.Button(func=logic_controller.move_to_screen, startX=450, endX=700, startY=300,
                                         endY=600, args='new_profile')
        sc_screens['start'].add_button(new_profile_scbutton)


        new_profile_uibutton = UI.Button(new_profile_scbutton, highlight=False, shadow=False, glimmer=False,
                                         border=False)
        filter = UI.Filter(img=ui_screens['start'].background)
        filter.img = new_profile_uibutton.img
        # filter.circular(func='BASIC_COLOR',color=(255,0,0),radius_res=10,radius_range=(0,100,10))
        filter.circles(radius_range=(60, 100, 2), thickness=5,
                       origin=(filter.img.shape[1] // 2, filter.img.shape[0] // 2), color=(255, 255, 0), var=0.2)
        cv2.putText(new_profile_uibutton.img, '+', (110, new_profile_uibutton.size[1] // 2),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 100, 0), 5)
        cv2.putText(new_profile_uibutton.img, 'Profile', (100, new_profile_uibutton.size[1] // 2+20),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 0), 2)
        ui_screens['start'].add_button(new_profile_uibutton)




        #new profile screen

        #add room button
        add_room_scbutton = sc.Button(startX=450,endX=570,startY=30,endY=60)
        sc_screens['new profile'].add_button(add_room_scbutton)

        add_room_uibutton = UI.Button(add_room_scbutton,highlight=False,shadow=False,glimmer=False,border=False,)
        cv2.putText(add_room_uibutton.img, '+Add Room', (10, 17), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
        ui_screens['new profile'].add_button(add_room_uibutton)


        # gestures_scbutton = sc.Button(startX=450,endX=570,startY=100,endY=150)
        # gesture_uibutton =UI.Button(gestures_scbutton, img=cv2.imread(ROOT_DIR + '/images/ges_images/gun.jpg'))
        # ges_1_scbutton = sc.Button(startX=450,endX=570,startY=150,endY=200)
        # ges_1_uibutton = UI.Button(ges_1_scbutton, img=cv2.imread(ROOT_DIR + '/images/ges_images/1.jpg'))
        # ges_2_scbutton = sc.Button(startX=450,endX=570,startY=200,endY=250)
        # ges_2_uibutton = UI.Button(ges_2_scbutton, img=cv2.imread(ROOT_DIR + '/images/ges_images/2.jpg'))
        #
        # new_profile_scscreen.add_button(ges_1_scbutton)#add the sc buttons to the sc screen
        # new_profile_scscreen.add_button(ges_2_scbutton)
        # new_profile_uiscreen.add_button(ges_2_uibutton)




    def add_screens_to_logic_ui_controllers(sc_screens,ui_screens):

        for scscreen in sc_screens.values():
            logic_controller.add_screen(scscreen)

        for uiscreen in ui_screens.values():
            ui_controller.add_screen(uiscreen)


    def bar_dim_blue(*args):
        bar_controller.send_commands(cmd= 'dim blue 100')


    def run_main():

        pTime, cTime   = 0,0

        cv2.namedWindow('screen', 0x00000000)

        start_variables()
        sc_screens = create_sc_screens()
        ui_screens = create_ui_screens()
        create_gestures(sc_screens,ui_screens)
        create_buttons(sc_screens,ui_screens)
        add_screens_to_logic_ui_controllers(sc_screens,ui_screens)
        #cv2.setWindowProperty('screen', 0, 1)
        while True:

            success, img = cap.read()

            img = cv2.flip(img, 1)

            img, lmListR, lmListL, handedness = detector.get_info(img)

            screen = ui_controller.screens[logic_controller.csn]

            if len(lmListR) != 0 or len(lmListL) != 0:
                screen.idle=False
                logic_controller.idle=False
                cv2.circle(img,(400,400),50, (0,255,0),-1)
                fingers = detector.fingerCounter()

                if handedness=='Right':
                    x, y = lmListR[8][1], lmListR[8][2]

                elif handedness == 'Left':
                    x, y = lmListL[8][1], lmListL[8][2]


            else:
                x,y=0,0
                screen.idle=True
                logic_controller.idle=True

            screen_img= screen.run(x, y, img)
            logic_controller.run([], detector, x, y)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(screen_img, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (255, 255, 255), 1)

            try:cv2.imshow('screen', screen_img)
            except: ui_controller.back()
            cv2.imshow('img',img)


            #print(controller.csn)
            #
            # #
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break



    def trying():
        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()

            cv2.imshow('img', img)



            if cv2.waitKey(1) & 0xFF==ord('q'):
                print('ended')
                break

        cap.release()
        cv2.destroyAllWindows()

    def cleanup():
        bar_controller.close_socket()
        print('socket lcosed')

    try:
        run_main()
        #trying()
    except Exception as e: print(e)
    finally:

        cleanup()


import threading


import cv2
import time

try:from win32api import GetSystemMetrics
except: pass

import scripts.controllers.SmartController as sc
from scripts.detectors.Gestures import Movement
from deprecated.Tuya import Controller as tuyacontroller
from scripts.controllers.youTube import youTubeController
import scripts.detectors.handLandmarks as hl
import numpy as np
import scripts.ui.UIMain as UI

import os

#ROOTDIR = os.path.dirname(os.path.abspath(__file__))
from definitions.config import ROOTDIR
screen_size= (1280,720)
print(ROOTDIR)
def move_to_screen(args):

    name = args[0]
    controllers = args[1]
    controllers['sc'].move_to_screen(name=name)
    controllers['ui'].move_to_screen(name)


def create_controllers(tuya=False, youtube=False, bar = False):


    logic_controller = sc.Controller()
    ui_controller = UI.Controller()
    detector = hl.handDetector()
    cap = cv2.VideoCapture(0)


    if tuya:
        tuya_controller = tuyacontroller()
    else: tuya_controller = None

    if youtube:
        yt = youTubeController()
    else:yt = None



    controllers = {
        'sc': logic_controller,
        'detector': detector,
        'ui': ui_controller,
        'cap': cap,
        'yt': yt,
        'tuya': tuya_controller

    }

    return controllers

def create_scscreens():



    living_room_screen = sc.Screen(name='living_room')
    appliances_screen = sc.Screen(name='appliances')


    canvas = sc.Screen(name='canvas')

    return {
        'appliances': appliances_screen,
        'living_room': living_room_screen,
        'canvas' : canvas
    }


def create_uiscreens():



    living_room_screen = UI.Screen(background_img=(os.path.join(ROOTDIR,'UI','images','background_images','background.jpg')),background_size=screen_size,name='living_room',show_cursor=False)
    fin2_img = cv2.imread(os.path.join(ROOTDIR,'UI','images','ges_images','2.jpg'))#ROOTDIR + '/images/ges_images/2.jpg')
    fin3_img = cv2.imread(os.path.join(ROOTDIR,'UI','images','ges_images','3.jpg'))
    fin1_img = cv2.imread(os.path.join(ROOTDIR,'UI','images','ges_images','1.jpg'))
    living_room_screen.add_image_to_canvas(fin2_img, (120,170), (100,100))
    living_room_screen.add_image_to_canvas(fin3_img, (200, 1000), (100, 100))
    living_room_screen.add_image_to_canvas(fin1_img, (600, 600), (100, 100))
    cv2.putText(living_room_screen.background, 'LIVING ROOM', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0),1)



    appliances_screen = UI.Screen(background_size=screen_size,name='appliances')
    ac_img = cv2.imread(os.path.join(ROOTDIR,'UI','images','ac_images','ac.jpg'))
    appliances_screen.add_image_to_canvas(ac_img,(10,600), (300,100))
    cv2.putText(appliances_screen.background, 'APPLIANCES', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)



    canvas = UI.Screen(name='canvas')

    return {
        'appliances': appliances_screen,
        'living_room': living_room_screen,
        'canvas' : canvas
    }


def create_gestures(scscreens, uiscreens, controllers):





    move_to_living_room = Movement(name='flash', func = move_to_screen, args=['living_room',controllers])
    move_to_appliances= sc.Gesture(gesture=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], func =move_to_screen, args = ['appliances', controllers])

    #scscreens['canvas'].add_gesture(move_to_living_room)
    scscreens['canvas'].add_gesture(move_to_appliances)


    air = Movement(name= 'air', func = lambda : print('air'))
    scscreens['canvas']. add_gesture(air)

    air2 = Movement(name= 'flash', func = lambda : print('flash pipe'))
    filename = os.path.join(ROOTDIR,'datasets','flash', 'flash_finalized_pipe_.sav')
    import pickle
    loaded_model = pickle.load(open(filename, 'rb'))
    air2.model = loaded_model
    print(f" our model is {air2.model}")

    scscreens['canvas'].add_gesture(air2)


    if controllers['tuya'] is not None:

        tuya_controller = controllers['tuya']
        #lights logic
        couch_toggle_ges = sc.Gesture(gesture=[0,1,0,0,0], func = tuya_controller.couch_toggle)
        scscreens['living_room'].add_gesture(couch_toggle_ges)

        open_toggle_ges = sc.Gesture(gesture=[0,1,1,0,0], func = tuya_controller.open_toggle)
        scscreens['living_room'].add_gesture(open_toggle_ges)

        kitchen_toggle_ges = sc.Gesture(gesture=[0,1,1,1,0], func = tuya_controller.kitchen_toggle)
        scscreens['living_room'].add_gesture(kitchen_toggle_ges)



        #appliance logic
        ac_on_ges = sc.Gesture(gesture=[0,1,0,0,0], func = tuya_controller.ac_remote, args='on_cold')
        ac_off_ges = sc.Gesture(gesture=[0, 1, 1, 0, 0], func=tuya_controller.ac_remote, args ='off')
        scscreens['appliances'].add_gesture(ac_on_ges)
        scscreens['appliances'].add_gesture(ac_off_ges)


def create_buttons(scscreens,uiscreens,):



    off_button_sc = sc.Button(func= lambda arg: print(arg), startX=500,startY =140,endX=600,endY=240,args='ac off', name='ac_off')
    scscreens['appliances'].add_button(off_button_sc)
    off_button_ui = UI.Button(off_button_sc,img= cv2.imread(os.path.join(ROOTDIR,'UI','images','ac_images','off.png')))
    uiscreens['appliances'].add_button(off_button_ui)

    cold_button_sc = sc.Button(func= lambda arg: print(arg), startX=700,startY =140,endX=800,endY=240,args='on cold', name='ac_cold')
    scscreens['appliances'].add_button(cold_button_sc)
    cold_button_ui = UI.Button(cold_button_sc,img= cv2.imread(os.path.join(ROOTDIR,'UI','images','ac_images','cold_n_t.png')))
    uiscreens['appliances'].add_button(cold_button_ui)

    hot_button_sc = sc.Button(func= lambda arg: print(arg), startX=700,startY =240,endX=800,endY=340,args='on hot', name='ac_hot')
    scscreens['appliances'].add_button(hot_button_sc)
    hot_button_ui = UI.Button(hot_button_sc,img= cv2.imread(os.path.join(ROOTDIR,'UI','images','ac_images','hot_n_t.png')))
    uiscreens['appliances'].add_button(hot_button_ui)


def add_screens_to_controllers(scscreens,uiscreens, controllers):

    logic_controller = controllers['sc']
    ui_controller = controllers['ui']

    for scscreen in scscreens.values():
        logic_controller.add_screen(scscreen)

    for uiscreen in uiscreens.values():
        ui_controller.add_screen(uiscreen)



def run_without_multiprocessing():


    cTime, pTime = 0,0
    bg=np.zeros((64, 64, 3))

    while True:

        # p1= threading.Thread(target = uiii, daemon = True)
        success, img = cap.read()

        img = cv2.flip(img, 1)
        img, lmListR, lmListL, handedness = detector.get_info(img)


        if len(lmListR) != 0 or len(lmListL) != 0:
            #cv2.circle(img, (400, 400), 50, (0, 255, 0), -1)
            #fingers = detector.fingerCounter()
            bg[:,:,1]=255
            bg[:,:,2]=0






            if handedness == 'Right':
                x, y = lmListR[8][1], lmListR[8][2]


            elif handedness == 'Left':
                x, y = lmListL[8][1], lmListL[8][2]

            else: x,y = 0,0


        else:
            x, y = 0, 0
            bg[:, :, 2] = 255
            bg[:, :, 1] = 0


        # p1 = multiprocessing.Process(target=uiii, daemon=True, args= [x,y,img])
        # p1.start()
        logic_controller.run([], detector, x, y)
        # process1 = multiprocessing.Process(target=logic_controller.run,args=[[],detector,x,y])
        # process1.start()

        screen = ui_controller.get_screen()

        screen_img = screen.run(x,y,img)

        cv2.imshow('screen', screen_img)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break


        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(bg, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1,
                   (0, 0, 0), 1)

        cv2.imshow('bg', bg)

if __name__ == '__main__':

    def ui_main(controllers,vars):

        cTime, pTime = 1, 0,
        x, y = 0, 0
        img = []
        cv2.namedWindow('ui')
        while True:
            #print('working')

            vars_lock.acquire()
            x,y = vars['hand coor']
            vars_lock.release()

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            try:
                screen = controllers['ui'].get_screen()
                screen_img = screen.run(x, y, img)
                cv2.putText(screen_img, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 1)
                cv2.imshow('ui', screen_img)

                if cv2.waitKey(1):
                    pass
            except Exception as e:
                print(e)


    def sc_main(controllers, vars):
        pTime, cTime = 0, 0

        bg = np.zeros((64, 64, 3))


        cap = controllers['cap']
        #detector = controllers['detector']

        detector = hl.handDetector()

        #cv2.namedWindow('bg')
        while True:

            # p1= threading.Thread(target = uiii, daemon = True)


            success, img = cap.read()
            img = cv2.flip(img, 1)

            img, lmListR, lmListL, handedness = detector.get_info(img)


            if len(lmListR) != 0 or len(lmListL) != 0:


                # cv2.circle(img, (400, 400), 50, (0, 255, 0), -1)
                # fingers = detector.fingerCounter()
                bg[:, :, 1] = 255
                bg[:, :, 2] = 0


                if handedness == 'Right':
                    x, y = lmListR[8][1], lmListR[8][2]


                elif handedness == 'Left':
                    x, y = lmListL[8][1], lmListL[8][2]

                else:
                    x, y = 0, 0

                vars_lock.acquire()
                vars['recognise'] = True
                vars['hand coor'] = x,y
                vars_lock.release()
            else:
                x, y = 0, 0
                bg[:, :, 2] = 255
                bg[:, :, 1] = 0
                vars_lock.acquire()
                vars['recognise'] = False
                vars['hand coor'] = (x,y)
                vars_lock.release()
            controllers['sc'].run([], detector, x, y)


            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     cap.release()
            #     cv2.destroyAllWindows()
            #     break

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            #print(fps)
            cv2.putText(bg, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (0, 0, 0), 1)


            #cv2.imshow('img', img)
            #cv2.imshow('bg', bg)


    def ui_main_proc(controllers, send, recv):

        bg=np.zeros((64, 64, 3))
        cTime, pTime = 1, 0,
        x, y = 0, 0
        img = []
        cv2.namedWindow('ui')
        bg = np.zeros((64, 64, 3))
        while True:
            #print('working')
            try:
                msg = recv.recv()
            except: pass

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            try:
                screen = controllers['ui'].get_screen()
                x,y = msg['hand coor']
                screen_img = screen.run(x, y, img)
                cv2.putText(screen_img, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (255, 255, 255), 1)
                cv2.imshow('ui', screen_img)


                if msg['recognise']:
                    bg[:, :, 1] = 255
                    bg[:, :, 2] = 0

                else:
                    bg[:, :, 2] = 255
                    bg[:, :, 1] = 0

                cv2.putText(bg, str(int(msg['lfps'])), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 0, 0), 1)

                cv2.imshow('bg', bg)

                if cv2.waitKey(1):
                    pass
            except Exception as e:
                print(e)


    def sc_main_proc(controllers,vars, send,recv):
        pTime, cTime = 0, 0



        cap = controllers['cap']
        #detector = controllers['detector']

        detector = hl.handDetector()

        #cv2.namedWindow('bg')
        while True:

            # p1= threading.Thread(target = uiii, daemon = True)


            success, img = cap.read()
            img = cv2.flip(img, 1)

            img, lmListR, lmListL, handedness = detector.get_info(img)


            if len(lmListR) != 0 or len(lmListL) != 0:



                if handedness == 'Right':
                    x, y = lmListR[8][1], lmListR[8][2]


                elif handedness == 'Left':
                    x, y = lmListL[8][1], lmListL[8][2]

                else:
                    x, y = 0, 0


                vars['recognise']= True
                vars['hand coor'] = (x,y)
            else:
                x, y = 0, 0
                vars['recognise']= False
                vars['hand coor'] = (x, y)
            controllers['sc'].run([], detector, x, y)


            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     cap.release()
            #     cv2.destroyAllWindows()
            #     break

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            vars['lfps']=fps

            send.send(vars)


            #cv2.imshow('img', img)
            #cv2.imshow('bg', bg)
    #cv2.namedWindow('bg')
    controllers = create_controllers()
    sc_screens = create_scscreens()
    ui_screens = create_uiscreens()

    create_gestures(sc_screens,ui_screens,controllers)
    create_buttons(sc_screens,ui_screens)

    add_screens_to_controllers(sc_screens,ui_screens,controllers)


    #detector = controllers['detector']
    cap = controllers['cap']
    logic_controller = controllers['sc']
    detector = hl.handDetector()
    ui_controller = controllers['ui']

    vars_lock = threading.Lock()



    vars = {
        'recognise': False,
        'hand coor': (0,0),
        'lfps': 0,
    }



    # lp = multiprocessing.Process(target=controllers['sc'].main, args = [controllers], daemon=True)
    # up = multiprocessing.Process(target=controllers['ui'].main, args = [controllers], daemon=True)


    #waitkey seems to crash the threads
    up = threading.Thread(target=ui_main, args=(controllers, vars,), daemon=True)
    lp = threading.Thread(target=sc_main, args = (controllers,vars,), daemon=True)




    #and imshow seems to crash the processes
    # send1, recv1 = multiprocessing.Pipe()
    # send2, recv2 = multiprocessing.Pipe()
    # up = multiprocessing.Process(target=ui_main_proc, args=(controllers, send1, recv2,), daemon=True)
    # lp = multiprocessing.Process(target=sc_main_proc, args = (controllers,vars,send2, recv1,), daemon=True)


    lp.start()
    up.start()


    up.join()


    #run_without_multiprocessing()




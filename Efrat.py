import datetime
import tkinter as tk
import threading


import cv2
import time
import handLandmarks as hl  # imports the module we have written
import youTube
import HA
import netflix
try:from win32api import GetSystemMetrics
except: pass

import SmartController as sc
from Gestures import Gesture, Movement
from Tuya import Controller as tuyacontroller
from youTube import youTubeController
import handLandmarks as hl
import numpy as np
import UIMain as UI

from SocketController import PiController as BarController
import Moods
import os
import Speech

ROOTDIR = os.path.dirname(os.path.abspath(__file__))

global display_active
global webcam_active
display_active = True
webcam_active = False
screen_size= (1280,720)

#used to collect data in gestures that are done and buttons preessed
#will be called everytime a gesture is done
#take a screen shot the the gesture
#collect angle info
def gesture_made(gesture):

    global img

    try:
        cv2.imwrite(ROOTDIR + '/datasets/' +str(gesture) + '/' + str(datetime.datetime.now()) + '.jpg', img )
    except Exception as e: print(e)


def view_options():
    print('view options')
    global display_active
    display_active = True

def view_webcam():
    global webcam_active
    webcam_active = True

def timeout():
    global webcam_active
    global display_active
    display_active = False
    webcam_active = False
    try:
        cv2.destroyWindow('screen')
    except:pass
    else: print('exiting display options')

def create_variables():
    global logic_controller
    global detector
    global ui_controller
    global cap
    global tuya_controller
    global yt
    #tuya_controller = tuyacontroller()

    logic_controller = sc.Controller()
    detector= hl.handDetector()
    ui_controller = UI.Controller()
    cap = cv2.VideoCapture(0)
    cap.set(3,screen_size[0])
    cap.set(4,screen_size[1])

    t1 = threading.Thread(target= bar, daemon=True)
    t1.start()

    yt = youTubeController()


def move_to_screen(name):
    global logic_controller
    global ui_controller

    logic_controller.move_to_screen(name=name)
    ui_controller.move_to_screen(name)

def bar():
    global bar_controller
    bar_controller= BarController()

def voice_search():
    global yt

    Speech.SpeakText('listening')

    txt = Speech.listen()

    yt.search(txt)

def vid_select():
    global yt
    yt.select()
    yt.waitForPageToLoad()
    yt.full_screen()


def sign_in(youtube=True):
    if youtube:
        global yt
        t1 = threading.Thread(target=yt.openYoutube, daemon=True)
        t1.start()

def create_scscreens():
    living_room_screen = sc.Screen(name='living_room')
    aplliances_screen = sc.Screen(name='appliances')
    bar_screen = sc.Screen(name='bar')
    youtube_screen = sc.Screen(name='youtube')

    canvas = sc.Screen(name='canvas')

    return {
        'living_room': living_room_screen,
        'appliances': aplliances_screen,
        'bar' : bar_screen,
        'youtube': youtube_screen,
        'canvas' : canvas
    }

def create_uiscreens():
    living_room_screen = UI.Screen(background_img='background.png',background_size=screen_size,name='living_room', timeout=120, timeout_func=timeout,show_cursor=False)
    fin2_img = cv2.imread(ROOTDIR + '/images/ges_images/2.jpg')
    fin3_img = cv2.imread(ROOTDIR + '/images/ges_images/3.jpg')
    fin1_img = cv2.imread(ROOTDIR + '/images/ges_images/1.jpg')
    living_room_screen.add_image_to_canvas(fin2_img, (120,170), (100,100))
    living_room_screen.add_image_to_canvas(fin3_img, (200, 1000), (100, 100))
    living_room_screen.add_image_to_canvas(fin1_img, (600, 600), (100, 100))
    cv2.putText(living_room_screen.background, 'LIVING ROOM', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0),1)



    appliances_screen = UI.Screen(background_size=screen_size,name='appliances', timeout=120, timeout_func=timeout)
    ac_img = cv2.imread(ROOTDIR + '/images/ac_images/ac.jpg')
    appliances_screen.add_image_to_canvas(ac_img,(10,600), (300,100))
    cv2.putText(appliances_screen.background, 'APPLIANCES', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

    bar_screen = UI.Screen(background_size=screen_size,name='bar', timeout=120, timeout_func=timeout)
    cv2.putText(bar_screen.background, 'BAR', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

    youtube_screen = UI.Screen(background_size=screen_size,name='youtube', timeout=120, timeout_func=timeout)
    cv2.putText(youtube_screen.background, 'YOUTUBE', (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

    canvas = UI.Screen(name='canvas')

    return {
        'living_room': living_room_screen,
        'appliances': appliances_screen,
        'bar' : bar_screen,
        'youtube': youtube_screen,
        'canvas' : canvas
    }


def create_gestures(scscreens, uiscreens):


    # test = Movement(name= 'test' , func = lambda : print('test'))
    # scscreens['bar'].add_gesture(test)


    move_to_living_room = Movement(name='flash', func = move_to_screen, args='living_room')
    move_to_youtube = Movement(name='music', func = move_to_screen, args = 'youtube')
    move_to_bar = Gesture(name='drink', func = move_to_screen, args = 'bar')
    #move_to_appliances = Movement(name='screw', func = move_to_screen, args = 'appliances')
    display_options = sc.Gesture(gesture=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], func =view_options)
    open_camera = sc.Gesture(gesture = [0,1,1,0,0,  0,1,1,0,0], func = view_webcam)
    scscreens['canvas'].add_gesture(move_to_living_room)
    scscreens['canvas'].add_gesture(move_to_youtube)
    scscreens['canvas'].add_gesture(move_to_bar)
    #scscreens['canvas'].add_gesture(move_to_appliances)
    scscreens['canvas'].add_gesture(display_options)
    scscreens['canvas'].add_gesture(open_camera)

    test = Movement(name='test', func=gesture_made, args='test')
    scscreens['canvas'].add_gesture(test)

    try:
        global tuya_controller

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
    except:pass

    #bar logic
    try:
        blue_ges = sc.Gesture(gesture=[0,1,0,0,0], func = Moods.blue, args= [bar_controller, tuya_controller])
        purple_ges = sc.Gesture(gesture=[0,1,1,0,0], func=Moods.purple, args=[bar_controller, tuya_controller])
    except:
        blue_ges = sc.Gesture(gesture=[0,1,0,0,0], func = lambda : print('blue - couldnt connect to bar'))
        purple_ges = sc.Gesture(gesture=[0,1,1,0,0], func=lambda :print('purple - couldnt connect to bar'))
    scscreens['bar'].add_gesture(blue_ges)
    scscreens['bar'].add_gesture(purple_ges)


    #youtube options
    global yt
    voice_search_ges = Movement(name='talk', func= voice_search)
    scscreens['youtube'].add_gesture(voice_search_ges)

    full_screen_ges = Movement(name = 'gun', func = vid_select)
    scscreens['youtube'].add_gesture(full_screen_ges)

def create_buttons(scscreens,uiscreens):
    off_button_sc = sc.Button(func= lambda arg: print(arg), startX=500,startY =140,endX=600,endY=240,args='ac off', name='ac_off')
    scscreens['appliances'].add_button(off_button_sc)
    off_button_ui = UI.Button(off_button_sc,img= cv2.imread(ROOTDIR + '/images/ac_images/off.png'))
    uiscreens['appliances'].add_button(off_button_ui)

    cold_button_sc = sc.Button(func= lambda arg: print(arg), startX=700,startY =140,endX=800,endY=240,args='on cold', name='ac_cold')
    scscreens['appliances'].add_button(cold_button_sc)
    cold_button_ui = UI.Button(cold_button_sc,img= cv2.imread(ROOTDIR + '/images/ac_images/cold_n_t.png'))
    uiscreens['appliances'].add_button(cold_button_ui)

    hot_button_sc = sc.Button(func= lambda arg: print(arg), startX=700,startY =240,endX=800,endY=340,args='on hot', name='ac_hot')
    scscreens['appliances'].add_button(hot_button_sc)
    hot_button_ui = UI.Button(hot_button_sc,img= cv2.imread(ROOTDIR + '/images/ac_images/hot_n_t.png'))
    uiscreens['appliances'].add_button(hot_button_ui)



def add_screens_to_controllers(scscreens,uiscreens):
    for scscreen in scscreens.values():
        logic_controller.add_screen(scscreen)

    for uiscreen in uiscreens.values():
        ui_controller.add_screen(uiscreen)


# def screenshot_tester(scscreens):
#
#     for screen in scscreens.values():
#         print(screen)
#         for gesture in screen.gestures:
#
#             try:
#                 ges = Movement(name=gesture.name, func= gesture_made, args=gesture)
#                 screen.add_gesture(ges)
#             except Exception as e: print(e)



print('started')
create_variables()
print('vars created')

sign_in()
scscreens=create_scscreens()
print('sc screens created')
uiscreens=create_uiscreens()
print('ui screens created')
create_gestures(scscreens,uiscreens)
print('gesture created' )
create_buttons(scscreens,uiscreens)
print('buttons created')
#screenshot_tester(scscreens)
add_screens_to_controllers(scscreens,uiscreens)
print('screens added')

bg= np.zeros((64,64,3))
ui_controller.current_screen='appliances'
logic_controller.csn = 'appliances'
pTime,cTime = 0,0

print('running...')
global img
while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    img, lmListR, lmListL, handedness = detector.get_info(img)

    screen = ui_controller.get_screen()

    if len(lmListR) != 0 or len(lmListL) != 0:
        #cv2.circle(img, (400, 400), 50, (0, 255, 0), -1)
        #fingers = detector.fingerCounter()
        bg[:,:,1]=255
        bg[:,:,2]=0

        screen.idle = False




        if handedness == 'Right':
            x, y = lmListR[8][1], lmListR[8][2]

        elif handedness == 'Left':
            x, y = lmListL[8][1], lmListL[8][2]


    else:
        x, y = 0, 0
        bg[:, :, 2] = 255
        bg[:, :, 1] = 0
        screen.idle = True

    logic_controller.run([], detector, x, y)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(bg, str(int(fps)), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 1,
                (0, 0, 0), 1)
    cv2.imshow('bg', bg)


    if display_active:
        screen_img = screen.run(x,y,img)
        cv2.imshow('screen', screen_img)

    if webcam_active:
        cv2.imshow('webcam', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 22:55:03 2022

@author: yaron
"""

import tkinter as tk

import numpy as np

import cv2
# import mediapipe as mp
import time
import handLandmarks as hl  # imports the module we have written
import youTube
import HA
import netflix
import ScreenDraw as sd
# import systemFunctions as system

import sys

# import math

# from win32api import GetSystemMetrics
import subprocess
import os

import SmartController as sc
from SmartController import SimpleUI
from Gestures import Gesture, Movement

import Tuya

import Calendar

controller = sc.Controller()
detector = hl.handDetector()
brush = sc.Drawer()
tc = Tuya.Controller()

global canvas

global yt
# yt=youTube.youTubeController()

# width, height = controller.get_screen_resolution()
width, height = 1280, 720
size = (width, height)

# startScreen = sc.Screen(ui_mode='transparent')
# lightScreen = sc.Screen(ui_mode='transparent')
# homeScreen = sc.Screen(ui_mode='transparent')
# drawScreenMain = sc.Screen(ui_mode='crop')
# drawScreenBrush = sc.Screen(ui_mode='crop', draw=True)
# drawScreenLips = sc.Screen(ui_mode='crop', draw=True)
# youtubeScreen = sc.Screen(ui_mode='inside_screen')

startScreen = sc.Screen(ui_mode='transparent', name='start')
lightScreen = sc.Screen(ui_mode='transparent', name = 'lights')
homeScreen = sc.Screen(ui_mode='transparent', name = 'home')
drawScreenMain = sc.Screen(ui_mode='crop', name = 'draw_main')
drawScreenBrush = sc.Screen(ui_mode='crop', draw=True, name = 'draw_brush')
drawScreenLips = sc.Screen(ui_mode='crop', draw=True, name= 'draw_lips')
youtubeScreen = sc.Screen(ui_mode='inside_screen', name= 'youtube')


def fistG(*args):
    #controller.cs = 1
    controller.csn = 'home'


def fin1G(*args):
    controller.csn = 'lights'


def fin2G(*args):
    # print("you")
    # controller.cs = 5

    controller.csn = 'youtube'
    youtubeScreen.start = True


def fin3G(*args):
    #controller.cs = 2

    controller.csn = 'draw_main'


def fin4G(*args):
    print('net  ')


def colour_pallatte(*args):
    # controller.cs = 3
    # print('darw')
    controller.csn = 'draw_brush'


def lip(*args):
    #controller.cs = 4

    controller.csn = 'draw_lips'


def red_brush(*args):
    drawScreenBrush.cui = 3
    brush.colour = (0, 0, 255)
    brush.thickness = 15


def green_brush(*args):
    drawScreenBrush.cui = 2
    brush.colour = (0, 255, 0)
    brush.thickness = 15


def blue_brush(*args):
    drawScreenBrush.cui = 1
    brush.colour = (255, 0, 0)
    brush.thickness = 15


def eraser(*args):
    drawScreenBrush.cui = 4
    brush.colour = (0, 0, 0)
    brush.thickness = 100


def draw_brush(*args):
    print(args)
    canvas = brush.draw(args[0], args[1], args[2])
    #canvas = brush.draw(args[0], args[1], args[2])
    #print(args[0][0])


def stop_drawing(*args):
    brush.start = True


def blue_lips(*args):
    drawScreenLips.cui = 0
    brush.colour = (255, 0, 0)
    brush.thickness = 15


def green_lips(*args):
    drawScreenLips.cui = 1
    brush.colour = (0, 255, 0)
    brush.thickness = 15


def red_lips(*args):
    drawScreenLips.cui = 2
    brush.colour = (0, 0, 255)
    brush.thickness = 15


def default_lips(*args):
    drawScreenLips.cui = 3
    brush.colour = (255, 255, 255)
    brush.thickness = 15


def draw_lips(*args):
    canvas = brush.drawLips(args[0])
    print('lips')


def back_func(*args):
    #controller.cs = 1
    controller.csn = 'home'


def youtube_func(*args):
    x = args[0]
    y = args[1]

    print(args)
    yt.posClick(x, y)
    yt.waitForPageToLoad(width, height)
    youtubeScreen.start = True


def swipe(*args):
    yt.scroll()
    yt.waitForPageToLoad(width, height)
    youtubeScreen.start = True


def f():
    print('hooray')

def open_toggle():
    tc.open_toggle()
    print('toggled')




def main():
    print("started")

    cv2.namedWindow('image',0x00000000)
    cv2.resizeWindow('image', 200, 100)

    args = []
    pTime, cTime = 0, 0
    hand = None

    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    success, img = cap.read()

    back = sc.Gesture(gesture=[1, 1, 1, 1, 1], func=back_func)

    # cs  =  0
    startScreen.add_images('start', size)
    fist = sc.Gesture(gesture=[0, 0, 0, 0, 0], func=fistG)

    horn = Gesture( 'devil horn', f)
    startScreen.add_gesture(horn)
    startScreen.add_gesture(fist)

    if use_cal.get()==1:
        pass
        cal = Calendar.Calendar(img=img)
        cal.create_cal()
        for i in cal.dates:
            startScreen.add_button(i.button)

    # cs = 1

    homeScreen.add_images('main', size)
    fin_1 = sc.Gesture(gesture=[0, 1, 0, 0, 0], func=fin1G)
    fin_2 = sc.Gesture(gesture=[0, 1, 1, 0, 0], func=fin2G)
    fin_3 = sc.Gesture(gesture=[0, 1, 1, 1, 0], func=fin3G)
    fin_4 = sc.Gesture(gesture=[0, 1, 1, 1, 1], func=fin4G)
    homeScreen.add_gesture(fin_1)
    homeScreen.add_gesture(fin_2)
    homeScreen.add_gesture(fin_3)
    homeScreen.add_gesture(fin_4)

    # cs = 2

    # drawScreenMain.add_images('headers',(width,height))
    drawScreenMain.add_images('draw_screen_main', size)
    colour_pallatte_button = sc.Button(func=colour_pallatte, startX=100, startY=100, endX=150, endY=150)
    lipAdd = sc.Button(func=lip, startX=570, startY=70, endX=690, endY=120)
    drawScreenMain.add_button(colour_pallatte_button)
    drawScreenMain.add_button(lipAdd)
    drawScreenMain.add_gesture(back)

    # cs= 3

    drawScreenBrush.add_images('draw_screen_brush', (width, height))
    painterRed = sc.Button(func=red_brush, startX=450, startY=50, endX=580, endY=90)
    painterBlue = sc.Button(func=blue_brush, startX=90, startY=50, endX=220, endY=90)
    painterGreen = sc.Button(func=green_brush, startX=270, startY=50, endX=400, endY=90)
    eraserB = sc.Button(func=eraser, startX=1100, startY=50, endX=1200, endY=90)
    drawBG = sc.Gesture(gesture=[0, 1, 0, 0, 0], gestureTime=0.1, func=draw_brush)
    stopDrawing = sc.Gesture(gesture=[0, 1, 1, 0, 0], gestureTime=0.1, func=stop_drawing)
    drawScreenBrush.add_button(painterRed)
    drawScreenBrush.add_button(painterBlue)
    drawScreenBrush.add_button(painterGreen)
    drawScreenBrush.add_button(eraserB)
    drawScreenBrush.add_gesture(drawBG)
    drawScreenBrush.add_gesture(stopDrawing)
    drawScreenBrush.add_gesture(back)

    # cs= 4
    drawScreenLips.add_images("draw_screen_lips", size)
    blueLips = sc.Button(func=blue_lips, startX=100, startY=60, endX=170, endY=120)
    greenLips = sc.Button(func=green_lips, startX=430, startY=60, endX=550, endY=120)
    redLips = sc.Button(func=red_lips, startX=780, startY=60, endX=900, endY=120)
    defaultLips = sc.Button(func=default_lips, startX=1160, startY=60, endX=1270, endY=120)
    drawG = sc.Gesture(gesture=[0, 1, 0, 0, 0], func=draw_lips)
    drawScreenLips.add_button(blueLips)
    drawScreenLips.add_button(redLips)
    drawScreenLips.add_button(greenLips)
    drawScreenLips.add_button(defaultLips)
    drawScreenLips.add_gesture(drawG)
    drawScreenLips.add_gesture(back)

    # cs= 5
    # youtubeScreen.add_images('optionsY', size)


    media = SimpleUI().MediaButtons(img = img)
    bg = media.play_button()
    bg = media.next_button()
    bg, vol_bar= media.volume_bar()



    try:
        yt.UI=bg
        youtubeScreen.web_object = yt
        print('youtube fine')

    except:
        print('you error')
    you_select = sc.Gesture(gesture=[0, 1, 1, 0, 0], func=youtube_func)
    #you_swipe = sc.Gesture(single_gesture=False, func=swipe)

    # create the constructor
    ges = Gesture('swipe_down_start')
    model = ges.load_model()
    ges.gesture_time=0

    end = Gesture('swipe_down_end')
    model_end = end.load_model()
    end.gesture_time=0

    you_swipe = Movement(ges, end,swipe)

    youtubeScreen.add_gesture(you_select)
    youtubeScreen.add_gesture(you_swipe)

    lightScreen.add_images('optionsL', (width, height))
    couch_ges = sc.Gesture(gesture=[0, 1, 0, 0, 0], func=tc.couch_toggle)
    open_ges = sc.Gesture(gesture=[0, 1, 1, 0, 0], func=open_toggle)
    kitchen_ges = sc.Gesture(gesture=[0, 1, 1, 1, 0], func=tc.kitchen_toggle)
    lightScreen.add_gesture(couch_ges)
    lightScreen.add_gesture(open_ges)
    lightScreen.add_gesture(kitchen_ges)
    lightScreen.add_gesture(back)


    start_ges_l= Gesture('all_off_start')
    model = start_ges_l.load_model()
    start_ges_l.gesture_time=0
    end_ges_l= Gesture('all_off_end')
    model = start_ges_l.load_model()
    end_ges_l.gesture_time=0

    all_off_ges = Movement(start_ges_l,end_ges_l,tc.all_off)
    lightScreen.add_gesture(all_off_ges)



    controller.add_screen_dict(startScreen)
    controller.add_screen_dict(homeScreen)
    controller.add_screen_dict(drawScreenMain)
    controller.add_screen_dict(drawScreenBrush)
    controller.add_screen_dict(drawScreenLips)
    controller.add_screen_dict(youtubeScreen)
    controller.add_screen_dict(lightScreen)

    #cap = cv2.VideoCapture(-1)

    start_ges, end_ges = False, False




    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        imgUI = img.copy()

        # img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)

        # c


        img = detector.findHands(img)
        handedness = detector.handedness()
        right, left = detector.findPosition(img)  # returns a list with the positions of all the landmarks
        fingers = detector.fingerCounter()
        angle = detector.fingerAngle(1, handedness)

        #cv2.imshow('i', img)

        if handedness == 'Right':
            lmList = right
        elif handedness == 'Left':
            lmList = left
        else:
            lmList = []



        #screen = controller.screens[controller.cs]

        screen = controller.screen_dict[controller.csn]

        # ui = screen.ui[screen.cui]
        # cv2.imshow("UI",ui)

        if len(lmList) != 0:
            # args dict
            args_dict = {
                'start': [img],
                'draw_brush': [imgUI, lmList[8][1], lmList[8][2]],
                'draw_lips': [imgUI],
                'youtube': [lmList[8][1], lmList[8][2]]

            }

            if fingers == [0, 1, 1, 0, 0]:  # selectmode
                x, y = lmList[8][1], lmList[8][2]
                hover = False


            elif fingers==[0,1,0,0,0]: # hover mode
                x,y = lmList[8][1], lmList[8][2]
                hover = True

            else:
                x,y=0,0
                hover = False

            # if controller.cs == 3:
            #     args = imgUI, lmList[8][1], lmList[8][2]
            #
            # if controller.cs == 4:
            #     args = imgUI
            #
            # if controller.cs == 5:


                hand, mask = detector.isolateHand(img, handedness)
                x, y = lmList[8][1], lmList[8][2]
                args = x, y

            cv2.setWindowProperty('image', 0,1)
            #print(cv2.getWindowProperty('image', 0x00000000))


            try: args = args_dict[controller.csn]
            except:args = []
            #print(args)
            controller.run(args, detector =detector, x=x, y=y, hover=hover)

            # displays the frames per second

        else:
            cv2.setWindowProperty('image', 0, 0)



        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3,
                    (255, 0, 255), 3)

        try:
            finalI = screen.ui_handler(img, brush.imgCanvas, hand)
        except:
            print("display error")
            cv2.imshow("image", img)
            try:cv2.imshow('ui', screen.ui[screen.cui])
            except:
                i = screen.ui_handler(img,hand=hand)
                cv2.imshow('image', i)
        else:

            try:finalI = cv2.bitwise_or(finalI,cal.background)
            except:pass
            cv2.imshow("image", finalI)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

    # cv2.imshow("iumg", homeScreen.ui[0])


def checkButtons():
    if HAvar.get() == 1:
        pass
        # print("checked")

    if HAvar.get() == 0:
        pass
        # print ("unchecked")


def signIn():
    global home
    global yt
    global nf
    if HAvar.get() == 1:
        if HAuser.get() == 'Username' and HApassword.get() == 'Password':
            home = HA.HAController()

        else:
            home = HA.HAController(username=HAuser.get(), password=HApassword.get())
        home.openHA()

    if YTvar.get() == 1:
        if YTuser.get() == 'Username' and YTpassword.get() == 'Password':
            yt = youTube.youTubeController()
        else:
            yt = youTube.youTubeController(username=YTuser.get(), password=YTpassword.get())

        yt.openYoutube()
        # print(yt.ping())

    if NFvar.get() == 1:
        if NFuser.get() == 'Username' and NFpassword.get() == 'Password':
            nf = netflix.netflixController()
        else:
            nf = netflix.netflixController(username=NFuser.get(), password=NFpassword.get())
        nf.openNetflix()
    # print ("s")


def signed():
    s = 'youtube'
    YTsigned = tk.Label(root, bg="green", text="Signed in", width=10)
    YT_not_signed = tk.Label(root, bg="red", text="NOT signed in", width=10)

    try:
        if s in yt.ping():
            YTsigned.grid(row=5, column=1)
            YT_not_signed.grid_remove()
            # print("yes")
        else:
            YT_not_signed.grid(row=5, column=1)
            YTsigned.grid_remove()
            # print("no")

    except Exception as e:
        # print(e)
        YT_not_signed.grid(row=5, column=1)
        YTsigned.grid_remove()
        # print("hell no")

    h = 'homeassistant'
    HAsigned = tk.Label(root, bg="green", text="Signed in", width=10)
    HA_not_signed = tk.Label(root, bg="red", text="NOT signed in", width=10)

    try:
        if h in home.ping():
            HAsigned.grid(row=2, column=1)
            HA_not_signed.grid_remove()
        else:
            HA_not_signed.grid(row=2, column=1)
            HAsigned.grid_remove()


    except:
        HA_not_signed.grid(row=2, column=1)
        HAsigned.grid_remove()

    n = 'netflix'
    NFsigned = tk.Label(root, bg="green", text="Signed in", width=10)
    NF_not_signed = tk.Label(root, bg="red", text="NOT signed in", width=10)

    try:
        if n in nf.ping():
            NFsigned.grid(row=8, column=1)
            NF_not_signed.grid_remove()
        else:
            NF_not_signed.grid(row=8, column=1)
            NFsigned.grid_remove()

    except:
        NF_not_signed.grid(row=8, column=1)
        NFsigned.grid_remove()
    root.after(500, signed)


def new_gesture(name):
    cap = cv2.VideoCapture(0)
    detector = hl.handDetector()
    done = 1
    ges = Gesture(detector, name)
    print(name)

    while True:
        success, img = cap.read()

        img = cv2.flip(img, 1)

        img, lmListR, lmListL, handedness = detector.get_info(img)

        # if cv2.waitKey(33) & 0xFF == ord('a'):
        if len(lmListR) != 0:
            '''
            train the model
            '''

            if done == 0:
                img = SimpleUI().add_text(img, "Present the Gesture")
                done = ges.create_gesture()
                print('positive sampling')

            if done == -1:
                done = ges.create_gesture()
                img = SimpleUI().add_text(img, "do different gestures")
                print('negative sampling')

            # the process is finished, and gesture is created
            if done == 1:
                img = SimpleUI().add_text(img, 'lets try the gesture')
                if ges.check_ges():
                    success, img = cap.read()
                    img = cv2.flip(img, 1)
                    img = SimpleUI().add_text(img, 'gesture added succecfully')
                    img = SimpleUI().add_text(img, org=(50, 100), text='press any key to continue')
                    cv2.imshow('img', img)
                    print('hooray')
                    cv2.waitKey(0)
                    cv2.destroyWindow('img')
                    break

                # else: print ('nope')

        cv2.imshow('img', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow('img')
            break


root = tk.Tk()  # create the base window / widget

HAvar = tk.IntVar()
NFvar = tk.IntVar()
YTvar = tk.IntVar()
ytsigned = tk.IntVar()

use_cal = tk.IntVar()
# ges_name = tk.StringVar()
ytsigned = 0
welcome = tk.Label(root, text="Welcome")

ges_name_input = tk.Entry(root, width=20)

# HAL = tk.Label(root, text = "Use Home Assistant")

HAL = tk.Checkbutton(root, text='Use Home Assistant', variable=HAvar, onvalue=1, offvalue=0, command=checkButtons)
HAuser = tk.Entry(root, width=20)
HAuser.insert(0, "Username")  # insert default text
HApassword = tk.Entry(root, width=20)
HApassword.insert(0, "Password")  # insert default text
# HAsign =  tk.Label(root,bg = "red", text = "NOT signed in")


# YTL = tk.Label(root, text = "Use Youtube")
YTL = tk.Checkbutton(root, text='Use Youtube', variable=YTvar, onvalue=1, offvalue=0, command=checkButtons)
YTuser = tk.Entry(root, width=20)
YTuser.insert(0, "Username")  # insert default text
YTpassword = tk.Entry(root, width=20)
YTpassword.insert(0, "Password")  # insert default text

# YTsign =  tk.Label(root,bg = "red", text = "NOT signed in")


NFL = tk.Checkbutton(root, text='Use Netflix', variable=NFvar, onvalue=1, offvalue=0, command=checkButtons)
NFuser = tk.Entry(root, width=20)
NFuser.insert(0, "Username")  # insert default text
NFpassword = tk.Entry(root, width=20)
NFpassword.insert(0, "Password")  # insert default text
# NFsign =  tk.Label(root,bg = "red", text = "NOT signed in")

CAL = tk.Checkbutton(root, text='Use Calendar', variable=use_cal, onvalue=1, offvalue=0, command=checkButtons)

signIn = tk.Button(root, text="Sign In", padx=10, pady=10,  # change size
                   command=signIn)

startButton = tk.Button(root, text="Start", padx=10, pady=10,  # change size
                        command=main)

create_new_gesture = tk.Button(root, text='Create Gesture', padx=10, pady=10,
                               command=lambda: new_gesture(ges_name_input.get()))

welcome.grid(row=0, column=0)

HAL.grid(row=1, column=0)
HAuser.grid(row=2, column=0)
HApassword.grid(row=3, column=0)
# HAsign.grid (row= 2, column = 1)

YTL.grid(row=4, column=0)
YTuser.grid(row=5, column=0)
YTpassword.grid(row=6, column=0)
# YTsign.grid (row= 5, column = 1)

NFL.grid(row=7, column=0)
NFuser.grid(row=8, column=0)
NFpassword.grid(row=9, column=0)
# NFsign.grid (row= 8, column = 1)


signIn.grid(row=10, column=0)
startButton.grid(row=11, column=0)

ges_name_input.grid(row=12, column=0)
create_new_gesture.grid(row=13, column=0)

CAL.grid(row=14, column = 0)

signed()
# cb = Checkbutton(window, text='Python',variable=var1, onvalue=1, offvalue=0, command=print_selection)


root.mainloop()  # loops the code til window exited
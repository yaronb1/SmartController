import tkinter as tk


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
import handLandmarks as hl
import numpy as np



logic_controller = sc.Controller()
detector= hl.handDetector()

living_room_screen = sc.Screen(name='living room')

couch_toggle_ges = sc.Gesture(gesture=[0,1,0,0,0], func = tuyacontroller().couch_toggle)
open_toggle_ges = sc.Gesture(gesture=[0,1,1,0,0], func = tuyacontroller().open_toggle)
kitchen_toggle_ges = sc.Gesture(gesture=[0,1,1,1,0], func = tuyacontroller().kitchen_toggle)

all_off_start = Gesture(name = 'all_off_start')
all_off_end = Gesture(name = 'all_off_end')

all_off_ges = Movement(all_off_start,all_off_end, func = tuyacontroller().all_off)




living_room_screen.add_gesture(couch_toggle_ges)
living_room_screen.add_gesture(open_toggle_ges)
living_room_screen.add_gesture(kitchen_toggle_ges)
living_room_screen.add_gesture(all_off_ges)

logic_controller.add_screen(living_room_screen)

cap = cv2.VideoCapture(0)

bg= np.zeros((64,64,3))

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)

    img, lmListR, lmListL, handedness = detector.get_info(img)

    if len(lmListR) != 0 or len(lmListL) != 0:
        #cv2.circle(img, (400, 400), 50, (0, 255, 0), -1)
        fingers = detector.fingerCounter()
        bg[:,:,1]=255
        bg[:,:,2]=0




        if handedness == 'Right':
            x, y = lmListR[8][1], lmListR[8][2]

        elif handedness == 'Left':
            x, y = lmListL[8][1], lmListL[8][2]


    else:
        x, y = 0, 0
        bg[:, :, 2] = 255
        bg[:, :, 1] = 0

    logic_controller.run([], detector, x, y)
    cv2.imshow('bg', bg)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
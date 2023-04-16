from scripts.controllers import SmartController as sc
from scripts.ui import UIMain as UI
from scripts.detectors import handLandmarks as hl
from scripts.detectors.Gestures import Gesture, Movement
import cv2


'strings of the  screens you want to create'
SCREENS= ['one', 'two']


GESTURES = [
            ]

MOVEMENTS =[
        ('flash', lambda : print('flash'), 'one'),
        ('snap', lambda : print('snap'), 'one'),
        ('one', lambda: print('one'), 'one'),
            ]



'''
create the controller - handdetector
                        logic controller
                        ui controller
                        videocapture
                        
                        media
                         options- socket, youtube, netflix, spotify
'''
def create_controllers():

    logic_controller = sc.Controller()
    detector= hl.handDetector()
    ui_controller = UI.Controller()
    cap = cv2.VideoCapture(0)


    controllers = {
        'sc': logic_controller,
        'detector': detector,
        'ui': ui_controller,
        'cap': cap,

    }

    return controllers

def create_screens():

    sc_screens = {}
    ui_screens = {}

    for name in SCREENS:
        screen = sc.Screen(name = name)
        u = {name:screen}
        sc_screens.update(u)



    return sc_screens



def create_gestures(sc_screens):

    for ges in GESTURES:
        g = Gesture(name = ges[0], func = ges[1])
        sc_screens[ges[2]].add_gesture(g)

    for m in MOVEMENTS:
        g = Movement(name = m[0], func = m[1])
        sc_screens[m[2]].add_gesture(g)


def add_screens_to_controllers(sc_screens,controllers):
    for scscreen in sc_screens.values():
        controllers['sc'].add_screen(scscreen)


def setup():
    controllers = create_controllers()
    screens = create_screens()
    create_gestures(screens)
    add_screens_to_controllers(screens,controllers)

    return controllers

def start(controllers):

    controllers['sc'].main(controllers)




if __name__ == '__main__':
    controllers = setup()
    start(controllers)

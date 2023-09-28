from scripts.controllers import SmartController as sc
from scripts.ui import UIMain as UI
from scripts.detectors import handLandmarks as hl
from scripts.detectors.Gestures import Gesture, Movement
import cv2


'strings of the  screens you want to create'
SCREENS= ['one', 'two']

#gestures and movement ar given as lists in the following format
#('name of gesture', func, screen to add to)

#if the func is move to a string- func should be given as a string - 'move 'name of screen''
GESTURES = [
    ('thumbs up', 'move two', 'one')
            ]

MOVEMENTS =[
        ('gun', lambda : print('gun'), 'two'),

            ]


def move_to_screen(controller,screen_name):
    controller.move_to_screen(screen_name)


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



def create_gestures(sc_screens, controllers):

    for ges in GESTURES:
        if ges[1][:4] == 'move':
            screen_name = ges[1][5:]
            g = Gesture(name=ges[0], func=lambda : controllers['sc'].move_to_screen(screen_name))
            sc_screens[ges[2]].add_gesture(g)
        else:
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
    create_gestures(screens, controllers)
    add_screens_to_controllers(screens,controllers)

    return controllers

def start(controllers):

    controllers['sc'].main(controllers)




if __name__ == '__main__':
    controllers = setup()
    start(controllers)

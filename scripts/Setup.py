from scripts.controllers import SmartController as sc
from scripts.ui import UIMain as UI
from scripts.detectors import handLandmarks as hl
from scripts.detectors.Gestures import Gesture, Movement
import cv2



from scripts.methods import TuyaMethods


'strings of the  screens you want to create'
SCREENS= ['one', 'two']

#gestures and movement ar given as lists in the following format
#('name of gesture', func args1 arg2 , screen to add to)
from scripts.methods import Methods

#funcs should be given as string
#and will be taken from the Methods module
#just name the function you have declared in the Methods module and pass anyargument each seperated by spaces
#the mmenthods in methods module must get a list as argument or no argument at all
# test arg1 arg2

#if you are taking methods from the TuyaMethods modlue start the string with - tuya : 'tuya func args'
GESTURES = [
    ('thumbs up', 'test hello yes', 'one')
            ]

MOVEMENTS =[


    #('gun', 'tuya test hello', 'one')
        #('fan_right', lambda : print('snap'), 'one'),
        ('right_fan','tuya turn off','one', 'reverse'), #all off
        ('right_fan', 'tuya turn on', 'one'),#all on
        ('gun', 'tuya brightness 10', 'one'),# dim all the lights
        ('gun', 'tuya brightness 1000', 'one','reverse'),#brihgtnes all lights
        ('flash', 'tuya mode colour', 'one'),#switch to colour mode
        ('snap', 'tuya mode white', 'one'), #switch to white mode



            ]


def move_to_screen(controller,screen_name):
    controller.move_to_screen(screen_name)


#functions will be derived from the methods module
# there you can type up your methods to be called with lists as argumetns or no arguments

def funcs(func_txt, controllers):
    if func_txt[:4] == 'move':
        screen_name = func_txt[5:]
        func=lambda: controllers['sc'].move_to_screen(screen_name)
        return func






    else:
        x = func_txt.split()

        if x[0]=='tuya':
            func = getattr(TuyaMethods, x[1])
            try:
                args = x[2:]
            except:
                return lambda : func()
            else:
                return lambda : func(args)

        else:

            func = getattr(Methods, x[0])
            try:
                args = x[1:]
            except:
                return lambda : func()
            else:
                return lambda : func(args)




'''
create the controller - handdetector
                        logic controller
                        ui controller
                        videocapture
                        
                        media
                         options- socket, youtube, netflix, spotify
'''
def create_controllers():

    logic_controller = sc.Controller(view_webcam=True)
    detector= hl.handDetector()
    ui_controller = UI.Controller()
    #tuya_remote = Remote.Remote(devices=tuya_devices)

    #tuya_remote.select_device('ALL')

    cap = cv2.VideoCapture(0)


    controllers = {
        'sc': logic_controller,
        'detector': detector,
        'ui': ui_controller,
        'cap': cap,
        #'tuya':tuya_remote,

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
        if isinstance(ges[1], str):
            func = funcs(ges[1], controllers)
        else:
            func = ges[1]


        g = Gesture(name = ges[0], func = func)
        sc_screens[ges[2]].add_gesture(g)

    for m in MOVEMENTS:
        if isinstance(m[1], str):
            func = funcs(m[1], controllers)
        else:
            func = m[1]

        try:
            if isinstance(m[3],str):
                reverse = True
        except:reverse=False


        mvnt = Movement(name=m[0], func=func, reverse=reverse)
        mvnt.timer=1
        sc_screens[m[2]].add_gesture(mvnt)



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


'''
UI

CONNECT TO DEVICES

have a checklist of available devices to connect to
divided into rooms
connect button

green/red symbol to show connection


SCREENS

number of screens 
names of each screen

GESTURES/ MOVEMENT

eache ges must be named(preferably dropdown) func and screen (preferably all scrolldowns)
'''
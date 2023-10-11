from scripts.controllers import SmartController as sc
from scripts.ui import UIMain as UI
from scripts.detectors import handLandmarks as hl
from scripts.detectors.Gestures import Gesture, Movement
import cv2
from scripts.controllers import Tuya
from scripts.controllers import Remote

#from definitions.TuyaDevices import LOCAL_DEVICES


tuya_devices = {'LIVING ROOM':{}}
#tuya_devices = LOCAL_DEVICES

'strings of the  screens you want to create'
SCREENS= ['one', 'two']

#gestures and movement ar given as lists in the following format
#('name of gesture', func, screen to add to)

#if the func is move to a string- func should be given as a string - 'move 'name of screen''
# func is power format - 'tuya power {mode}' turn on , turn off, toggle
#func is change work mode - 'tuya mode {mode}' white, colour
GESTURES = [
    ('thumbs up', 'move two', 'one')
            ]

MOVEMENTS =[
        ('fan_right', lambda : print('snap'), 'one'),
        # ('right_fan','tuya power turn off','one', 'reverse'), #all off
        # ('right_fan', 'tuya power turn on', 'one'),#all on
        # ('gun', 'tuya brightness 10', 'one'),# dim all the lights
        # ('gun', 'tuya brightness 1000', 'one','reverse'),#brihgtnes all lights
        # ('flash', 'tuya mode colour', 'one'),#switch to colour mode
        # ('snap', 'tuya mode white', 'one'), #switch to white mode



            ]


def move_to_screen(controller,screen_name):
    controller.move_to_screen(screen_name)


# used to create the relveant functions based on the text func passed
#the text must be given as the second item in the ges/move list

#options -
#           move to screen = 'move {name of screen}'
#           power options = 'tuya power {option}' - turn on, turn on, toggle
#           switch mode   = 'tuya mode {mode}' - white, colour
#           set brightness= 'tuya brightness {brightness}' 10<brightness<1000
#           set hue(colour)= 'tuya colour {hue}' 10<hue<1000
#           set temp(white)= 'tuya white {temp}' 10<temp<1000
def funcs(func_txt, controllers):
    if func_txt[:4] == 'move':
        screen_name = func_txt[5:]
        func=lambda: controllers['sc'].move_to_screen(screen_name)
        return func



    # using text for tuya commands taken from remote class and tuya class
    elif func_txt[:4] == 'tuya':

        # power options
        if func_txt[5:10] == 'power':
            if func_txt[11:] == 'turn off':
                func=controllers['tuya'].turn_off
                return func

            elif func_txt[11:] == 'turn on':
                func=controllers['tuya'].turn_on
                return func

            elif func_txt[11:] == 'toggle':
                func=controllers['tuya'].toggle
                return func

        elif func_txt[5:9] == 'mode':
            mode = func_txt[10:]
            func=lambda: controllers['tuya'].work_mode(mode)
            return func

        elif func_txt[5:15]=='brightness':
            brightness = int(func_txt[16:])
            func = lambda :controllers['tuya'].set_brightness(brightness)
            return func

        elif func_txt[5:11]=='colour':
            hue = int(func_txt[12:])
            func = lambda: controllers['tuya'].set_colour(hue)
            return func

        elif func_txt[5:10]=='white':
            temp = int(func_txt[11:])
            func = lambda : controllers['tuya'].set_white(temp)
            return func



def tuya_control():
    pass




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
    tuya_remote = Remote.Remote(devices=tuya_devices)

    tuya_remote.select_device('ALL')

    cap = cv2.VideoCapture(0)


    controllers = {
        'sc': logic_controller,
        'detector': detector,
        'ui': ui_controller,
        'cap': cap,
        'tuya':tuya_remote,

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
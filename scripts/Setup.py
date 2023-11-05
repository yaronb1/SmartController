import os

from scripts.controllers import SmartController as sc

from scripts.detectors import handLandmarks as hl
from scripts.detectors.Gestures import Gesture, Movement
import cv2

from definitions.config import ROOTDIR


from scripts.methods import Methods
from scripts.methods import TuyaMethods


TuyaCommander = TuyaMethods.Commander()
CustomCommander = Methods.Commander()

'strings of the  screens you want to create'
SCREENS= ['one', 'two']

#gestures and movement ar given as lists in the following format
#('name of gesture', func args1 arg2 , screen to add to)


#funcs should be given as string
#and will be taken from the Methods module
#just name the function you have declared in the Methods module and pass anyargument each seperated by spaces
#the mmenthods in methods module must get a list as argument or no argument at all
# test arg1 arg2

#if you are taking methods from the TuyaMethods modlue start the string with - tuya : 'tuya func args'
GESTURES = [
    ('thumbs_up2', 'tuya test hello', 'one')
            ]

MOVEMENTS =[


    ('gun2', 'tuya test hello', 'one'),
    #('flash2', 'tuya test hello', 'one'),
    #     #('fan_right', lambda : print('snap'), 'one'),
    #     ('right_fan','tuya turn_off','one', 'reverse'), #all off
    #     ('right_fan', 'tuya turn_on', 'one'),#all on
    #     ('gun', 'tuya brightness 10', 'one'),# dim all the lights
    #     ('gun', 'tuya brightness 1000', 'one','reverse'),#brihgtnes all lights
    #     ('flash', 'tuya mode colour', 'one'),#switch to colour mode
    #     ('snap', 'tuya mode white', 'one'), #switch to white mode



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
        print(x)

        if x[0]=='tuya':

            try:
                args = x[2]
            except:
                return lambda : TuyaCommander.__getattribute__(x[1])()
            else:
                return lambda : TuyaCommander.__getattribute__(x[1])(args)

        elif x[0]=='custom':


            try:
                args = x[2]
            except:
                return lambda : CustomCommander.__getattribute__(x[1])()
            else:
                return lambda : CustomCommander.__getattribute__(x[1])(args)




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



    cap = cv2.VideoCapture(0)


    controllers = {
        'sc': logic_controller,
        'detector': detector,
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
        sc_screens['one'].add_gesture(mvnt)



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
    #controllers = setup()
    #start(controllers)


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


    from tkinter import *
    from definitions.TuyaDevices import LOCAL_DEVICES



    def submit():
        Label(text=f'gesture - {ges_clicked.get()}').pack()
        Label(text= f'function - {func_clicked.get()}').pack()
        Label(text = f'args - {args.get()}').pack()

        if os.path.exists(os.path.join(ROOTDIR,'datasets', ges_clicked.get(), 'end_img.jpg')):
            MOVEMENTS.append((ges_clicked.get(), command_type.get() + ' ' +func_clicked.get() + ' ' +  args.get(), 'one'))

        else:
            GESTURES.append((ges_clicked.get(), command_type.get() + ' ' +func_clicked.get() + ' ' +  args.get(), 'one'))

        print(f'gesture : {GESTURES}')
        print(f'movements - {MOVEMENTS}')


    def run():
        controllers = setup()
        start(controllers)


    def change_options(*args):
        if command_type.get()=='tuya':
            tuya_drop.pack()
            func_drop.pack_forget()

        elif command_type.get()== 'custom':
            func_drop.pack()
            tuya_drop.pack_forget()


    def add_device():
        for i in devices_to_connect:
            print(i.get())

    def connect_devices():
        devices_dict = {}


        for room in LOCAL_DEVICES:
            devices_dict[room] = {}
            for d in devices_to_connect:

                if d.get() in LOCAL_DEVICES[room]:

                    devices_dict[room][d.get()] = LOCAL_DEVICES[room][d.get()]

        connect_devices = TuyaCommander.connect_local_devices(devices_dict)






    root = Tk()

    devices_to_connect = []
    # tuya devices checkbox and connect

    for room, devices_dict in LOCAL_DEVICES.items():
        Label(text = room).pack()

        for name, device_info in devices_dict.items():
            var = Variable()
            c1 = Checkbutton(root, text=name, variable=var, onvalue=name, offvalue='', command=add_device)
            c1.pack()
            devices_to_connect.append(var)

    connect = Button(root,text='CONNECT DEVICES', command=connect_devices)
    connect.pack()

    #SELECT YOUR GESTURE
    ges_options = os.listdir(os.path.join(ROOTDIR, 'datasets'))
    ges_options.remove('negatives')
    ges_options.remove('old')
    ges_options.remove('screenshots')

    # datatype of menu text
    ges_clicked = StringVar()
    args= StringVar()

    # initial menu text
    ges_clicked.set("Slect Your Gesture")

    # Create Dropdown menu
    ges_drop = OptionMenu(root, ges_clicked, *ges_options)
    ges_drop.pack()


    #SELECT YOUR FUNCTIONS

    func_options = [method for method in dir(Methods.Commander) if method.startswith('__') is False]
    tuya_options = [method for method in dir(TuyaMethods.Commander) if method.startswith('__')is False]

    command_options = ['tuya', 'custom']
    command_type=StringVar()
    command_drop = OptionMenu(root,command_type,*command_options,command=change_options)
    command_drop.pack()

    func_clicked = StringVar()
    func_clicked.set('Select you Function')

    func_drop = OptionMenu(root, func_clicked, *func_options)
    tuya_drop = OptionMenu(root,func_clicked,*tuya_options)
    func_drop.pack()

    Label(root, text='enter your arguments').pack()
    args_box = Entry(root, textvariable=args)
    args_box.pack()


    #ADD gesture
    add = Button(text = 'ADD GESTURE', command=submit).pack()


    start_button = Button(text='START', command=run)
    start_button.pack()

    root.mainloop()





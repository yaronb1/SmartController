import os
import scripts.controllers.SmartController as sc
from test import Start

import dill as pickle

import cv2
import numpy as np
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config

from scripts.detectors.Gestures import Gesture
import scripts.detectors.handLandmarks as hl

from UIMain import SimpleUI



ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


Config.set('graphics', 'resizable', True)
Builder.load_file('UIApp.kv')

project_folder = '/home/yaron/PycharmProjects/SmartController/'

ges_images_folder = '/home/yaron/PycharmProjects/SmartController/images/ges_images'
ges_images = os.listdir(ges_images_folder)
global screenM
w,h = 1280,720

profile = 'default'
try:
    with open('/home/yaron/PycharmProjects/SmartController/profiles/' + profile +  '/variables.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
        controller = pickle.load(f)

except:
    print('new controller created')
    controller = sc.Controller()

class Main(Screen):


    def start_main(self):
        start = Start()

        start.run_main()

    def new_gesture(self,name,new=True):
        cap = cv2.VideoCapture(0)
        detector = hl.handDetector()
        done = 0
        ges = Gesture(name=name, new=new)
        ges.create_directory()
        print(name)

        while True:
            success, img = cap.read()

            img = cv2.flip(img, 1)

            img, lmListR, lmListL, handedness = detector.get_info(img)

            # if cv2.waitKey(33) & 0xFF == ord('a'):
            if len(lmListR) != 0 or len(lmListL)!=0:
                '''
                train the model
                '''

                if done == 0:
                    #img = SimpleUI().add_text(img, "Present the Gesture")
                    cv2.putText(img, 'Present the Gesture', (20, 120),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 0), 2)
                    done = ges.create_gesture(detector)
                    print('positive sampling')

                if done == -1:
                    ges.copy_negatives()
                    ges.train_model()
                    done=1
                    # done = ges.create_gesture(detector)
                    # #img = SimpleUI().add_text(img, "do different gestures")
                    # cv2.putText(img, 'Do diffeernet gestures', (20, 120),
                    #             cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 100, 0), 2)
                    # print('negative sampling')

                # the process is finished, and gesture is created
                if done == 1:
                    cv2.imwrite(ROOT_DIR + '/datasets' + str(name) + '.jpg', img)
                    print('gesture added succesfully')

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


    def new_screen(self):

        cam =  CamApp()
        s = cam.build()
        self.add_widget(s)


        print('yes')

class NewScreen(Screen):
    profile = 'default'
    ges_ui = 'fdfd'
    btn_ui = ''
    background = []
    x_ = 0
    y_ = 0
    gestures = {}
    args=[]

    def build(self):

        self.add_image()
        self.create_ges_menu()
        self.create_button_menu()
        self.image_creator = SimpleUI()
        self.screen = sc.Screen()
        #self.create_menu('Button')

    def add_image(self):
        cam = CamApp()
        lay = cam.build()
        self.ids['image'].add_widget(lay)
        #

    def create_ges_menu(self):
        ges_dropdown = UIModeSelect()
        ges_mainbutton = Button(text='Gesture', size_hint=(None, None))
        ges_mainbutton.bind(on_release=ges_dropdown.open)
        ges_dropdown.bind(on_select=lambda instance, x: setattr(ges_mainbutton, 'background_normal', x))
        ges_dropdown.bind(on_select=lambda instance, x: setattr(ges_mainbutton, 'text', ''))
        for index in ges_images:
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            btn = Button(#text='Value %d' % index,
                 background_normal= ges_images_folder + '/' +str(index),  size_hint_y=None, height=74)

            #print(index)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            #btn.bind(on_release=lambda btn: ges_dropdown.select(btn.text))
            btn.bind(on_release=lambda btn: ges_dropdown.select(btn.background_normal))
            print(btn.background_normal)
            btn.bind(on_release=lambda btn: self.ges_bind(btn.background_normal))

            # then add the button inside the dropdown
            ges_dropdown.add_widget(btn)


        ges_dropdown.dismiss()

        func_dropdown = UIModeSelect()
        func_mainbutton = Button(text='func', size_hint=(None, None))
        func_mainbutton.bind(on_release=func_dropdown.open)
        func_dropdown.bind(on_select=lambda instance, x: setattr(func_mainbutton, 'text', x))


        #for each index add a function to bind to a gesture using the add_function method
        #functions can have arguments through one of two ways

        #first passed through info text by the user. each update will update the gesture args
        # or passed directly when binding the button
        #in this case we should notice that the args are a LIST and must be treated as such to avoid erros
        for index in range(10):
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.
            if index == 0:
                btn = Button(text='Next Screen', size_hint_y=None, height=44)
                btn.bind(on_release=lambda instance:self.add_function(check))
            elif index==1:

                #the args will be updated through the info text therefore no args passed to add_function
                func = controller.move_to_screen
                btn = Button(text='move to screen', size_hint_y=None, height=44)
                btn.bind(on_release=lambda instance:self.add_function(func))
                btn.bind(on_release = lambda instance: self.change_ges_info_text('screen to move to'))
            elif index==2:
                func = controller.move_to_screen
                btn = Button(text='move', size_hint_y=None, height=44)
                btn.bind(on_release=lambda instance:self.add_function(func,'home'))
                btn.bind(on_release = lambda instance: self.change_ges_info_text('screen to move to'))



            else:
                btn = Button(text='Value %d' % index, size_hint_y=None, height=44)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: func_dropdown.select(btn.text))

            # then add the button inside the dropdown
            func_dropdown.add_widget(btn)
        func_dropdown.dismiss()


        self.ids['ges_menu'].add_widget(ges_dropdown)
        self.ids['ges_menu'].add_widget(ges_mainbutton)

        self.ids['ges_menu'].add_widget(func_dropdown)
        self.ids['ges_menu'].add_widget(func_mainbutton)

    def create_button_menu(self):
        ges_dropdown = UIModeSelect()
        ges_mainbutton = Button(text='Button', size_hint=(None, None))
        ges_mainbutton.bind(on_release=ges_dropdown.open)
        ges_dropdown.bind(on_select=lambda instance, x: setattr(ges_mainbutton, 'background_normal', x))
        ges_dropdown.bind(on_select=lambda instance, x: setattr(ges_mainbutton, 'text', ''))
        for index in ges_images:
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            btn = Button(#text='Value %d' % index,
                 background_normal= project_folder + '/images/button_images/' +str(index),  size_hint_y=None, height=74)

            #print(index)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            #btn.bind(on_release=lambda btn: ges_dropdown.select(btn.text))
            btn.bind(on_release=lambda btn: ges_dropdown.select(btn.background_normal))
            print(btn.background_normal)
            btn.bind(on_release=lambda btn: self.btn_bind(btn))

            # then add the button inside the dropdown
            ges_dropdown.add_widget(btn)


        ges_dropdown.dismiss()

        func_dropdown = UIModeSelect()
        func_mainbutton = Button(text='func', size_hint=(None, None))
        func_mainbutton.bind(on_release=func_dropdown.open)
        func_dropdown.bind(on_select=lambda instance, x: setattr(func_mainbutton, 'text', x))


        #for each index add a function to bind to a gesture using the add_function method
        #functions can have arguments through one of two ways

        #first passed through info text by the user. each update will update the gesture args
        # or passed directly when binding the button
        #in this case we should notice that the args are a LIST and must be treated as such to avoid erros
        for index in range(10):
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.
            if index == 0:
                btn = Button(text='Next Screen', size_hint_y=None, height=44)
                btn.bind(on_release=lambda instance:self.add_function(check))
            elif index==1:

                #the args will be updated through the info text therefore no args passed to add_function
                func = controller.move_to_screen
                btn = Button(text='move to screen', size_hint_y=None, height=44)
                btn.bind(on_release=lambda instance:self.add_function(func))
                btn.bind(on_release = lambda instance: self.change_button_info_text('screen to move to'))
            elif index==2:
                func = controller.move_to_screen
                btn = Button(text='move', size_hint_y=None, height=44)
                btn.bind(on_release=lambda instance:self.add_function(func,'home'))
                btn.bind(on_release = lambda instance: self.change_button_info_text('screen to move to'))



            else:
                btn = Button(text='Value %d' % index, size_hint_y=None, height=44)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: func_dropdown.select(btn.text))

            # then add the button inside the dropdown
            func_dropdown.add_widget(btn)
        func_dropdown.dismiss()


        self.ids['button_menu'].add_widget(ges_dropdown)
        self.ids['button_menu'].add_widget(ges_mainbutton)

        self.ids['button_menu'].add_widget(func_dropdown)
        self.ids['button_menu'].add_widget(func_mainbutton)

    def add_ges(self):
        self.add_ui()

        try:i = int(self.ges_to_add)
        except:
            gesture = Gesture(name=self.ges_to_add, func=self.func_to_add,args=self.args)
        else:
            if i == 1:
                ges = [0,1,0,0,0]
            elif i == 2:
                ges=[0,1,1,0,0]
            elif i == 3:
                ges=[0,1,1,1,0]
            elif i == 4:
                ges = [0,1,1,1,1]

            else:
                print('error getting gesture')
                return

        try:gesture = sc.Gesture(gesture= ges,func=self.func_to_add,args=self.args)
        except: print('custom gesture added')
        self.screen.add_gesture(gesture)

    def add_button(self):

        bw = self.button_to_add.size[0]
        bh = self.button_to_add.size[1]

        button = sc.Button(func=self.func_to_add, startX=self.x_*300, startY=self.y_ *200, endX=self.x_*300+300 , endY=self.y_*200 +200, args = self.args)
        self.screen.add_button(button)

        self.add_ui()
        print(self.x_,self.y_)
        print(self.x_ + bw, self.y_+bh)



    def add_function(self,func,*args):
        self.func_to_add=func
        self.args = args
        print('function added')
        print(args)

    def add_ui(self):
        print(self.ges_ui)
        img = cv2.imread(self.ges_ui)

        try:self.background = self.image_creator.add_image_to_background(img,(300,200),(h,w), x= self.x_*300, y=self.y_*200)
        except:
            self.x_=0
            self.y_ +=1
            try:self.background = self.image_creator.add_image_to_background(img,(300,200),(h,w), x= self.x_*300, y=self.y_*200)
            except Exception as e:
                print('screen out of room')
                print(e)
            else: self.x_+=1
        else:
            self.x_+=1

    def ges_bind(self, text):
        self.ges_ui= text

        self.ges_to_add = text[62:len(text)-4]
        print('ges' + self.ges_to_add)
        #print(text[62])
        #self.ges_to_add = text[62]

    def btn_bind(self,btn):
        self.ges_ui = btn.background_normal
        print('size' + str(btn.size))
        self.button_to_add = btn


    def save_screen(self):
        screen_name = self.ids['screen_name'].text
        #path = self.create_folder(screen_name)
        path = project_folder + 'profiles/' + self.profile
        self.screen.add_ui(self.background)
        controller.add_screen_dict(self.screen)

        with open(path + '/variables.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump(controller, f)

        self.clear()

    def clear(self):
        self.screen = sc.Screen()
        self.gestures = {}
        self.args=[]
        self.background=[]
        self.image_creator.background=[]
        self.x_ = 0
        self.y_ = 0


    def change_ges_info_text(self, text):
        self.ids['ges_info'].text = text
    def change_button_info_text(self, text):
        self.ids['button_info'].text = text




class UIModeSelect(DropDown):
    pass

class TestApp(App):
    def build(self):
        global screenM
        screenM = ScreenManager()

        screenM.add_widget(Main(name='Main'))
        screenM.add_widget(NewScreen(name= 'NewScreen'))
        return screenM


class CamApp(Widget):

    start = True
    def build(self):
        self.img1=Image()

        self.image_creator = SimpleUI()
        #self.tranparent_background = self.image_creator.create_transparent_backround(size=self.img1.size)

        layout = BoxLayout()
        layout.add_widget(self.img1)
        #print('image added')
        #opencv2 stuffs
        self.capture = cv2.VideoCapture(0)
        self.capture.set(3,w)
        self.capture.set(4,h)
        #cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0/33.0)


        #print(self.img1.size)

        return layout

    def add_ui_image(self, img_path):
        img = cv2.imread(img_path)
        self.tranparent_background =  self.image_creator.add_image_to_background(img, (320,200), None)



    def update(self, dt):
        # display image from cam in opencv window
        ret, frame = self.capture.read()


        frame1 = self.cv_funcs(frame)
        #cv2.imshow("CV2 Image", frame1)
        #cv2.waitKey(1)
        # convert it to texture
        buf1 = cv2.flip(frame1, 0)
        buf = buf1.tobytes()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer.
        #texture1.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')# for grayscale
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte') # for color
        # display image from the texture
        self.img1.texture = texture1

    def cv_funcs(self, frames):

        #print(screenM.children[0].ui_images)
        background = screenM.children[0].background
        try:final = sc.Controller().overlay_transparent(frames, background, 0, 0)
        except Exception as e:
            return frames
        else:return final



def check(*args):
    print('hoorrrayy')





if __name__ == "__main__":

    TestApp().run()

    # dict = NewScreen().get_variables('again_screen')
    #
    # for key,value in dict.items():
    #     print(key)
    #     value()





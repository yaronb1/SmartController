import cv2
import numpy as np

import AI
import handLandmarks as hl

import pickle

import csv

import time

import collections


class Gesture():
    '''
    This class aims to capture a gesture made by the user, save it and then compare gestures captured from the webcam
    to the saved gesture.

    In this fasion we can create a any gesture and store it and use it to interact with our smart house


    create gesture:
        Step 1:
        create several angle lists of the gesture and store them in a csv file

        step 2:
        create several angle lists of something that is NOT the gesture and store them in a csv file

        step 3:
        send the csv file to the logistic regression AI model and save and name the model


    Chech gesture:
        step 1:
        create angle list of the gesture displayed through the webcam

        step 2:
        send the angle list through the model we have built




    '''

    def __init__(self,
                 #detector,
                 name,
                 func=None,
                 path = '/home/yaron/PycharmProjects/SmartController/datasets/',
                 gesture_time = 1,
                 args=[]
                 ):

        #self.detector = detector
        self.name = name
        self.path = path
        self.func = func
        self.start = False
        self.count = 0
        self.args=args


        self.started = False
        self.elapsed = 0
        self.start_time = 0
        self.gesture_time = gesture_time

        try: self.model = self.load_model()
        except: print('no model')

    #creates a list defining each angle between the point of the hand
    #list type will describe if the list is of the gesture, Not of the gesture, a list from the webcam which will be checked
    # list type = 1
                # the gesture

    #list type = 0:
                # NOT the gesture

    #list type = -1:
                #list to pass through the built model

    # returns angle list
    def create_angle_list(self,detector, list_type):

        angle_list = []

        if detector.hand == 'no hand':
            pass

        else:

            for i in range(20):
                if i == 0:
                    pass
                else:
                    angle = detector.pointAngle(i, i+1)  #
                    if angle == -1:
                        raise ValueError('angle error')

                    else:
                        angle_list.append(angle)

        if list_type==1:
            angle_list.append(self.name)
        elif list_type == 0:
            angle_list.append('nope')
        elif list_type == -1:
            pass


        return angle_list


    #store a single angle list the the given file
    # the variable angle list must be created using the above function
    # this function appends to an existing angle list with relevant headers
    def save_angle_list(self, angle_list):
        data_file = self.path + str(self.name) + '.csv'

        #store angle list in csv file
        with open(data_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(angle_list)


    #creates a new file with the appropreate headers
    def create_new_file(self, headers = []):
        default_headers = ['thumb 1-2', 'thumb 2-3', 'thumb 3-4', 'thumb_fore 4-5', 'fore 5-6', 'fore 6-7', 'fore 7-8',
                  'fore_middle 8-9', 'middle 9-10', 'middle 10-11', 'middle 11-12', 'middle_ring 12-13', 'ring 13 -14',
                  'ring 14-15', 'ring 15-16', 'ring_pinky 16-17', 'pinky 17-18', 'pinky 18-19', 'pinky 19-20', 'gesture']

        data_file = self.path + str(self.name) + '.csv'
        with open(data_file, 'w') as f:
            writer = csv.writer(f)
            if len(headers) == 0:
                writer.writerow(default_headers)
            else:
                writer.writerrow(headers)


    def train_model(self):
        data_file = self.path +str(self.name)

        AI.create_model(data_file)

    def load_model(self, file_path=''):
        try:
            filename = self.path + str(self.name) + '_finalized_model.sav'
            loaded_model = pickle.load(open(filename, 'rb'))

        except:
            try:
                loaded_model = pickle.load(open(file_path, 'rb'))
            except:return None

        return loaded_model

    def create_gesture(self,detector, n =5, num_of_samples =100):
        '''
        collects as many angle list as possible,
        collects NOT angle lists

        trains the module

        @param  n - take angle list every n'th frame

        :return: done when all values have been stored and the module has been created
        '''

        if self.start == False:
            self.create_new_file()
            self.start = True
            self.samples = 0
            self.status = 1
            print('started')

        elif self.start:

            self.count += 1

            if self.count == n:
                self.count = 0
                try: angles = self.create_angle_list(detector,self.status)
                except Exception as e: print(e)
                else:
                    print(angles)
                    self.save_angle_list(angles)
                    self.samples +=1
                    print(self.samples)

            if self.samples == num_of_samples:
                self.samples = 0
                self.status = self.status - 1
                print('do negative samples')
                time.sleep(3)

        #done when returns 1
        if self.status == -1:
            self.train_model()
            self.model = self.load_model()
            return 1

        #negative sampling is done when returns -1
        elif self.status==0:
            return -1

        #positive sampling done when returns 0
        else: return 0


    def check_ges(self,detector):

        angles = self.create_angle_list(detector,-1)


        result = self.model.predict(np.array([angles]))[0]

        if str(result) == self.name:
            if self.started:
                now = time.time()
                self.elapsed = now - self.start_time
                # print(int(elapsed))
                if self.elapsed > self.gesture_time:
                    self.started = False
                    self.elapsed =0
                    return True
            else:
                self.started = True
                self.start_time = time.time()

        else:
            self.started = False
            self.elapsed = 0

        return False



'''
the movemnet gesture requirse 2 gestures (created with the above class)
start ges - to trigger the movemnet
end ges to complete it

(we can consider doing an in between gesture as well)

this can be passed nin 2 fors
either create 2 seperate gestures with their respective positive and negative images 
which will be passed as start and end ges 

or 

create one gestuder where the positive is start and negative is end 
passed as one variable- gesture 
'''
class Movement:

    def __init__(self,
             gesture=None,
             start_ges=None,
             end_ges=None,
             func=None,
             args=[],
             timer = 0.5):

        if gesture is None:
            self.start_ges = start_ges
            self.end_ges = end_ges

        else:
            self.start_ges = gesture
            self.end_ges = gesture
            self.end_ges.name = 'nope'


        self.start_ges.gesture_time = 0
        self.end_ges.gesture_time=0
        self.timer=timer

        self.started = False
        self.start_time = 0

        self.func=func
        self.args=args


    def check_ges(self, detector):

        if self.start_ges.check_ges(detector):
            self.started = True
            self.start_time = time.time()

        if self.started:
            now = time.time()
            self.elapsed = now - self.start_time
            if self.elapsed < self.timer and self.end_ges.check_ges(detector):
                self.started = False
                self.elapsed = 0
                return True

            if self.elapsed > self.timer:
                self.started = False
                self.elapsed = 0

        return False








def all_off(*args):
    print('alloff')


def kill(*args):
    print('kill')



if __name__ == '__main__':

    import SmartController as sm


    # the model will be an array consisiting of three values
    # the first is a model for the start of gesture, second is a model for the end of the gesture
    # and third is an int for the timeout inbetween

    #CRETATING THE MODEL

    #step 1 the user will tarin the model with only how the gesture looks in the beginnig

    cap = cv2.VideoCapture(0)
    detector = hl.handDetector()

    # create the constructor
    all_off_start = Gesture('all_off_start')
    all_off_end = Gesture('all_off_end')
    all_off_movement = Movement(start_ges=all_off_start, end_ges=all_off_end,func=all_off)

    kill_gesture = Gesture('kill')
    kill_movement = Movement(gesture=kill_gesture, func=kill)

    controller = sm.Controller()

    home = sm.Screen(name = 'home')
    #home.add_gesture(end)
    #home.add_gesture(ges)
    home.add_gesture(all_off_movement)
    home.add_gesture(kill_movement)

    controller.add_screen(home)





    while True:
        success, img = cap.read()

        img = cv2.flip(img,1)

        img, lmListR, lmListL, handedness = detector.get_info(img)


        cv2.imshow('img', img)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if len(lmListR)!=0 or len(lmListL)!=0:

            controller.run([],detector =detector, x=0, y=0)




    # step 2  the user will tarin the model with only how the gesture looks in the end



    # step 3 the user will do the entire gesture to time the timeout

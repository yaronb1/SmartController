import cv2
import numpy as np

import AI
import handLandmarks as hl

import pickle

import csv

import time

import collections
import os
import datetime
ROOTDIR = os.path.dirname(os.path.abspath(__file__))


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
                 args=[],
                 new = False
                 ):

        #self.detector = detector
        self.name = name
        self.path = path + str(name) +'/'
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

        self.new=new

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

        elif list_type==2:
            angle_list.append(self.name+'_start')
        elif list_type==3:
            angle_list.append(self.name+'_end')


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

        try:data_file = self.path + str(self.name) + '.csv'
        except:
            print(type(self.path))
            data_file=self.path + str(self.name) + '/' + str(self.name) + '.csv'
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

    def create_gesture(self,detector, n =5, num_of_samples =200):
        '''
        collects as many angle list as possible,
        collects NOT angle lists

        trains the module

        @param  n - take angle list every n'th frame

        :return: done when all values have been stored and the module has been created
        '''

        if self.start == False:
            if self.new:self.create_new_file()
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

    def create_negatives(self,detector, n =5, num_of_samples =1000):
        '''


        @param  n - take angle list every n'th frame

        :return: done when all values have been stored and the module has been created
        '''

        if self.start == False:
            self.create_new_file()
            self.start = True
            self.samples = 0
            print('started')

        elif self.start:

            self.count += 1

            if self.count == n:
                self.count = 0
                try: angles = self.create_angle_list(detector,0)
                except Exception as e: print(e)
                else:
                    print(angles)
                    self.save_angle_list(angles)
                    self.samples +=1
                    print(self.samples)

            if self.samples == num_of_samples:
                return 1
            else: return 0





    def check_ges(self,detector):

        angles = self.create_angle_list(detector,-1)


        result = self.model.predict(np.array([angles]))[0]
        #print(result)
        #print(self.name)

        if str(result) == self.name:
            if self.started:
                now = time.time()
                self.elapsed = now - self.start_time
                # print(int(elapsed))
                if self.elapsed > self.gesture_time:
                    self.started = False
                    self.elapsed =0
                    try:
                        # func to save angle list and collect data
                        file = ROOTDIR + '/datasets/' + str(self.name) + '/' + str(datetime.datetime.now()) + '.csv'
                        with open(file, 'w') as f:
                            f.write(str(angles))
                    except Exception as e:
                        print(e)

                    return True
            else:
                self.started = True
                self.start_time = time.time()

        else:
            self.started = False
            self.elapsed = 0

        return False

    def create_directory(self):

        #create folder
        directory = '/datasets/' + str(self.name)
        path = os.path.join(ROOTDIR,directory)
        try:os.mkdir(ROOTDIR + directory)
        except: print('dir already exist')
        print("Directory '% s' created" % directory)

    def copy_negatives(self):
        file = ROOTDIR + "/datasets/nope.csv"
        nf =  ROOTDIR +  "/datasets/" + str(self.name) + '/' + str(self.name) + ".csv"


        with open(file, 'r') as origFile:
            with open(nf, 'a') as newFile:
                lineList = []
                headers = True
                for line in origFile:
                    #strippedLine = line.strip()
                    #lineList = strippedLine.split(',')

                    #
                    # lineStr = str(lineList)
                    # lineStr = lineStr.replace("'", "")

                    #newFile.write(lineStr)
                    if headers:
                        headers = False
                    else:
                        newFile.write(line)
                    # newFile.write('\n')  # Insert a new line
                    # i += 1



        origFile.close()
        newFile.close()



'''
for movemnet we will have 2 gestures.
one start and one end

they will be stored in the same csv filke.

the idea is the model will recogbise start then end
the negatives will be the same but the model will also differentiate between start and end

inherits from Gesture
check ges is overiden

args

func to run when recognised
args for func if needed
timer - MAXIMUM time between start and end to be considered the movemnet
name - name the gesture, the older where the model and the csv file are store

'''
class Movement(Gesture):

    def __init__(self,

             func=None,
             args=[],
             timer = 0.5,
             name='',
                 ):

        super(Movement, self).__init__(name=name)

        self.timer=timer

        self.started = False
        self.start_time = 0

        self.func=func
        self.args=args
        self.name = name

    def create_movement(self, detector, n=5, num_of_samples=200):
        '''


        @param  n - take angle list every n'th frame
                num of samples- will take this number of start samples and end samples

        :return: 1  when all values have been stored and the module has been created
        '''

        if self.start == False:
            self.create_new_file()
            self.start = True
            self.samples = 0
            self.status = 2  # start ges
            print('started')

        elif self.start:

            self.count += 1

            if self.count == n:
                self.count = 0
                try:
                    angles = self.create_angle_list(detector, self.status)
                except Exception as e:
                    print(e)
                else:
                    print(angles)
                    self.save_angle_list(angles)
                    self.samples += 1
                    print(self.samples)

            if self.samples == num_of_samples:

                if self.status == 2:
                    self.status = 3  # end ges
                    print('do end gesture')
                    time.sleep(2)
                    self.samples = 0
                    return 0

                if self.status == 3:
                    self.copy_negatives()
                    self.train_model()
                    return 1  # done

            else:
                return 0


    def check_ges(self, detector):

        angles = self.create_angle_list(detector,-1)


        result = self.model.predict(np.array([angles]))[0]

        #print(self.end_ges.name)
        if result == self.name +'_start':
            self.started = True
            self.start_time = time.time()

        if self.started:
            now = time.time()
            self.elapsed = now - self.start_time
            if self.elapsed < self.timer and result == self.name+'_end':
                self.started = False
                self.elapsed = 0
                try:
                    # func to save angle list and collect data
                    file = ROOTDIR + '/datasets/' + str(self.name) + '/' + str(datetime.datetime.now()) + '.csv'
                    with open(file, 'w') as f:
                        f.write(str(angles))
                except Exception as e: print(e)
                return True

            if self.elapsed > self.timer:
                self.started = False
                self.elapsed = 0

        return False









def create_movement(name):


    ges = Movement(name = name)
    ges.create_directory()
    Movement.status = 2

    cap = cv2.VideoCapture(0)
    detector = hl.handDetector()
    done = 0

    while True:
        success, img = cap.read()

        img = cv2.flip(img, 1)

        img, lmListR, lmListL, handedness = detector.get_info(img)

        if len(lmListR) !=0 or len(lmListL)!=0:
            if ges.start == False:
                time.sleep(0.5)
                cv2.imwrite(ROOTDIR + '/datasets/' + name + '/start_img.jpg', img)

            done = ges.create_movement(detector)



        cv2.imshow('img', img)

        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
        if done==1:
            cv2.imwrite(ROOTDIR + '/datasets/' + name + '/end_img.jpg', img)
            break

if __name__ == '__main__':

    create_movement('gun')
    # ges = Movement(name='screw')
    # ges.copy_negatives()
    # ges.train_model()







    # step 2  the user will tarin the model with only how the gesture looks in the end



    # step 3 the user will do the entire gesture to time the timeout

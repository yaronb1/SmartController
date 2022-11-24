'''
Calendar the parent class will contain all the methods and all the var

'''

import cv2
import datetime
import calendar
import numpy as np

from SmartController import Button
import os
import random

class Calendar:


    length_per = 250
    height_per = 150

    def __init__(self,
                 size = (1200, 1980,3),
                 img= None,
                 img_dir = '/home/yaron/Desktop/image_processing_tools/mosaic_effect/us_pics',
                 use_images = False
                 ):
        self.today = datetime.datetime.today()
        self.size=size


        self.img=img
        #self.size= size
        self.month = self.today.month

        try:
            sizes = len(self.img)
            self.background = np.zeros_like(self.img)
            self.full_cal = np.zeros_like(self.img)
            self.ind_date = np.zeros_like(self.img)
        except:
            self.background=np.zeros(self.size, dtype='uint8')
            self.full_cal = np.zeros(self.size, dtype='uint8')
            self.ind_date = np.zeros(self.size, dtype='uint8')

        if use_images:
            self.date_images = self.load_images(img_dir)




        self.dates =[]

        self.create_cal()
        self.create_individual_date()



    def load_images(self,images_directory):
        files = os.listdir(images_directory)
        images = []
        n = 0
        #for file in files:
        for i in range(30):
            file = files[i]
            filePath = os.path.abspath(os.path.join(images_directory, file))
            try:
                im = cv2.imread(filePath)
                w = im.shape[1]
                h = im.shape[0]
                # im = cv2.resize(im,(w//10,h//10))
                im = cv2.resize(im, (120, 64))
                images.append(im)
                # cv2.imshow('image',im)
                # cv2.waitKey(0)

            except Exception as e:
                print("Invalid image: %s" % (filePath,))
                print(e)
            else:
                print("image added: %s" % (filePath,))

        return images


    def create_cal(self):
        '''
        creates the cakendar by creating a grid on the screen
        loops through the dates
        creates datecards and uses their var to draw the calendar
        :return:
        '''

        # if len(self.img)!=0:
        #     self.background = np.zeros_like(self.img)
        # else:self.background=np.zeros(self.size)
        month = self.today.strftime('%B')
        year = self.today.strftime('%Y')

        cv2.putText(self.background, month, (150, 40), cv2.FONT_HERSHEY_COMPLEX, 2,
                    (255, 255, 255), 2)


        the_first = datetime.datetime(self.today.year,self.today.month, 1)

        #print(the_first.day)

        n=0
        for i in Labels.days.keys():
            #print(i)

            cv2.putText(self.background, i, (16+n*self.length_per, 100), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (255, 255, 255), 1)
            n+=1
        num_of_days = calendar.monthrange(self.today.year, self.today.month)[1]
        #dx= 0
        dy = 0
        d= the_first

        try:date_img = self.date_images[random.randint(0,len(self.date_images)-1)]
        except: date_img = None

        for i in range(num_of_days):
            try:
                date_img = self.date_images[random.randint(0, len(self.date_images) - 1)]
            except:
                date_img = None
            dx= Labels.days[d.strftime('%a')]

            date = DateCard(date=d,
                                 startx= 10+dx*self.length_per,
                                 starty= 110+dy*self.height_per,
                                 cal=self,
                                 img = date_img
                            )
            #print(date.date)
            try:
                im_size = date.img.shape

                self.background[date.starty:date.starty+self.height_per,date.startx:date.startx+self.length_per] = date.img
                #cv2.imshow('im',im)


            except Exception as e : print(e)
            cv2.rectangle(self.background, (date.startx, date.starty), (date.startx+self.length_per, date.starty+self.height_per), (0, 0, 0), 3)
            cv2.putText(self.background, str(date.date.day), (date.startx +10, date.starty+25),cv2.FONT_HERSHEY_COMPLEX, 1,
                    (0, 0, 0), 2)

            d += datetime.timedelta(days=1)


            #if i%7 == 0 and i!=0:
            if dx==6:
                dy+=1
                #dx=0

            #else:dx+=1

            self.dates.append(date)


        self.full_cal=self.background
        #cv2.imshow('cal', self.background)


    def create_individual_date(self):

        cv2.rectangle(self.ind_date, (10, 10),
                      (10 + self.length_per*5, 10 + self.height_per*5), (255, 255, 255), 3)

        cv2.imshow('date',self.ind_date)


class DateCard(Calendar):
    def __init__(self,
                 date,
                 startx,
                 starty,
                 cal,
                 img=None
                 ):
        self.date = date
        self.startx = startx
        self.starty = starty
        self.cal=cal
        self.length = super().length_per
        self.height = super().height_per

        self.times =[]

        self.button = Button(func=self.func, startX=startx, startY=starty, endX=startx+self.length, endY=starty+self.height)

        self.img=img

        try: self.img = cv2.resize(img, (self.length, self.height), interpolation=cv2.INTER_AREA)
        #try: self.img = self.image_resize(img,height = self.height)
        except: print('no image')

    def func(self, *args):
        print(self.date)
        self.cal.background = self.cal.ind_date

        self.activate_date_buttons(active=False)


        cv2.putText(self.cal.ind_date, str(self.date.day), ( 50,  100), cv2.FONT_HERSHEY_COMPLEX,
                    0.5,
                    (255, 255, 255), 1)

    def image_resize(self,image, width=None, height=None, inter=cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation=inter)

        # return the resized image
        return resized

    def activate_date_buttons(self,active=True):
        for d in self.cal.dates:
            d.button.active=active

    def activate_time_buttons(self,active=True):
        for t in self.times:
            t.button.active=active

    # def button_press(self):


    # def build_time(self):
    #     for time in range(24):
    #         print(time)



class TimeSlots(DateCard):

    def __init__(self,
                 time,
                 events = {}):

        self.time = time
        self.events = events

class Labels(Calendar):
    days={'Sun': 0,
          'Mon': 1,
          'Tue': 2,
          'Wed': 3,
          'Thu': 4,
          'Fri': 5,
          'Sat': 6,

    }


def create_calendar():
    cal = Calendar()
    cv2.imshow('cal',cal.background)


if __name__ == '__main__':


    #create_calendar()
    cal = Calendar(use_images=True)
    cv2.imshow('cal',cal.background)

    print(cal.background.shape)




    cv2.waitKey(0)

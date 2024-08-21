import cv2
import numpy as np
from definitions.config import ROOTDIR
import os
import asyncio


'''
the class aims to segregate an image into different section and allow a user to select a section
a selected section will be highlighted and the highlighted section can be interacted with
'''
class Section():


    def __init__(self,
                 bg_image =[],
                 size= (1980,720)
                 ):

        bg_image = cv2.resize(bg_image,size)
        self.bg_image = bg_image
        self.final = self.bg_image.copy()

        self.selection = -1

        self.segregate()

    #seperate the image into its different sections

    def segregate(self):

        # self.section0 = self.bg_image[:,:self.bg_image.shape[1]//3]
        # self.section1 = self.bg_image[:, self.bg_image.shape[1] // 3:int(self.bg_image.shape[1] * (2/3))]
        # self.section2 = self.bg_image[:, int(self.bg_image.shape[1] * (2/3)):]
        #
        # self.sections = [self.section0, self.section1, self.section2]

        self.section0 = self.bg_image[377:607, 131:609]
        self.section1 = self.bg_image[28:602, 884:1535]

        self.sections = [self.section0,self.section1]


    def conc(self):
        #self.final = cv2.hconcat(self.sections)

        self.final[377:607, 131:609] = self.sections[0]
        self.final[28:602, 884:1535] = self.sections[1]


    def dim_section(self, section, dimmer =0.7):

        hsv = cv2.cvtColor(section, cv2.COLOR_BGR2HSV).astype('float32')
        (h, s, v) = cv2.split(hsv)
        s= s*dimmer
        v = v * dimmer
        v = np.clip(v, 0, 255)
        s = np.clip(s, 0, 255)
        imghsv = cv2.merge([h, s, v])

        dimmed = cv2.cvtColor(imghsv.astype('uint8'), cv2.COLOR_HSV2BGR)

        return dimmed

    def highlight_section(self, section, highlighter=1.7):

        hsv = cv2.cvtColor(section, cv2.COLOR_BGR2HSV).astype('float32')
        (h, s, v) = cv2.split(hsv)
        s = s * highlighter
        v = v * highlighter
        v = np.clip(v, 0, 255)
        s = np.clip(s, 0, 255)
        imghsv = cv2.merge([h, s, v])

        highlighted = cv2.cvtColor(imghsv.astype('uint8'), cv2.COLOR_HSV2BGR)

        return highlighted

    # the select function will be the main function used to select
    #provide a number for the section to select and the other sections will be dimmed
    #the final concancatd image will be returned
    def select(self, section =1):

        if self.selection != section:
            for i,n in enumerate(self.sections):
                print (i)
                if i == section:
                    self.sections[i] = self.highlight_section(n)
                else:
                    self.sections[i] = self.dim_section(n)

            self.selection =section
            self.conc()







    async def main(self):


        while True:
            cv2.imshow('bg', self.final)
            await asyncio.sleep(0.1)

            if cv2.waitKey(1) and 0xFF  == ord('q'):
                break

if __name__ == '__main__':

    from scripts.detectors import handLandmarks

    detector = handLandmarks.handDetector()
    section = Section(cv2.imread(os.path.join(ROOTDIR,'images','floor_plan', 'Dark.png')))
    async def finger_counter():
        cap = cv2.VideoCapture(0)
        while True:
            success,img = cap.read()

            img, lmListR, lmListL, handedness = detector.get_info(img)
            no_of_fin = detector.fingerCounter()

            if no_of_fin==[0,1,0,0,0]:
                section.select(section=0)
            elif no_of_fin==[0,1,1,0,0]:
                section.select(1)
            elif no_of_fin==[0,1,1,1,0]:
                section.select(2)
            print(no_of_fin)
            await asyncio.sleep(0.1)


    async def run():
        fing = asyncio.create_task(finger_counter())
        view = asyncio.create_task(section.main())
        await fing
        await view

    asyncio.run(run())



    #section.main()



import cv2
import numpy as np
import time

import handLandmarks

import pickle

#import UIMain


class CircleCropper():

    #c\\draws a white circle
    # butwise _nad with image
    #params image


    def __init__(self,
                 img=[],
                 controller_size=(640,480)):

        self.img= img
        self.cx=self.img.shape[1]//2
        self.cy=self.img.shape[0]//2
        self.controller_size = controller_size
        self.cropped_image = []

    def create_controller(self):

        cv2.namedWindow('controller')
        cv2.resizeWindow('controller', self.controller_size)


        endx = self.img.shape[1]
        cx = endx// 2
        endy= self.img.shape[0]
        cy = endy// 2


        cv2.createTrackbar('size', 'controller', 1, 500, self.crop)
        cv2.createTrackbar('centerx', 'controller', cx, endx, self.crop)
        cv2.createTrackbar('centery', 'controller', cy, endy, self.crop)

    def crop(self, radius):
        bg = np.zeros_like(self.img)


        r = cv2.getTrackbarPos('size', 'controller')
        cx = cv2.getTrackbarPos('centerx', 'controller')
        cy = cv2.getTrackbarPos('centery', 'controller')

        mask = cv2.circle(bg, (cx,cy), r,(255,255,255), -1)
        #cv2.imshow('mask', mask)
        cropped_image = cv2.bitwise_and(self.img, mask)

        cv2.imshow('cropped', cropped_image)
        self.cropped_image=cropped_image\




class Cartoonizer:
	"""Cartoonizer effect
		A class that applies a cartoon effect to an image.
		The class uses a bilateral filter and adaptive thresholding to create
		a cartoon effect.
	"""
	def __init__(self):
		pass

	def render(self, img_rgb):
		#img_rgb = cv2.imread(img_rgb)
		#img_rgb = cv2.resize(img_rgb, (1366,768))
		numDownSamples = 2	 # number of downscaling steps
		numBilateralFilters = 100 # number of bilateral filtering steps

		# -- STEP 1 --

		# downsample image using Gaussian pyramid
		img_color = img_rgb
		for _ in range(numDownSamples):
			img_color = cv2.pyrDown(img_color)

		cv2.imshow("downcolor",img_color)
		#cv2.waitKey(0)
		# repeatedly apply small bilateral filter instead of applying
		# one large filter
		for _ in range(numBilateralFilters):
			img_color = cv2.bilateralFilter(img_color, 9, 9, 7)

		#cv2.imshow("bilateral filter",img_color)
		#cv2.waitKey(0)
		# upsample image to original size
		for _ in range(numDownSamples):
			img_color = cv2.pyrUp(img_color)
		cv2.imshow("upscaling",img_color)
		#cv2.waitKey(0)

		# -- STEPS 2 and 3 --
		# convert to grayscale and apply median blur
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
		img_blur = cv2.medianBlur(img_gray, 15)
		cv2.imshow("grayscale+median blur",img_color)
		#cv2.waitKey(0)

		# -- STEP 4 --
		# detect and enhance edges
		img_edge = cv2.adaptiveThreshold(img_blur, 255,
										cv2.ADAPTIVE_THRESH_MEAN_C,
										cv2.THRESH_BINARY, 9, 2)
		cv2.imshow("edge",img_edge)
		#cv2.waitKey(0)

		# -- STEP 5 --
		# convert back to color so that it can be bit-ANDed with color image
		(x,y,z) = img_color.shape
		img_edge = cv2.resize(img_edge,(y,x))
		img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
		#cv2.imwrite("edge.png",img_edge)
		cv2.imshow("step 5", img_edge)
		#cv2.waitKey(0)
		#img_edge = cv2.resize(img_edge,(i for i in img_color.shape[:2]))
		#print img_edge.shape, img_color.shape
		return cv2.bitwise_and(img_color, img_edge)



'''
handcropper allows the user to crop an image based on where his right forefinger is
use your right hand to move the black dot to the starting position
then raise one finger on your left hand to start creating a rect from the strating posion to where you right 
forfinger is
raise 2 fingers on the left hand to complete the crop
'''
class HandCropper():

    def __init__(self,
                 img_path='background.png',
                 save = False):

        self.img = cv2.imread(img_path)
        self.img=cv2.resize(self.img,(1280,720))

        self.save =True

    def save_coordinates(self, coordinates):

        with open('/home/yaron/PycharmProjects/SmartController/button_variables/ac_lights.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump(coordinates, f)


    def main(self):
        detector = handLandmarks.handDetector()
        cap = cv2.VideoCapture(0)
        cap.set(3,self.img.shape[1])
        cap.set(4,self.img.shape[0])

        start = True
        end = False
        x=0
        y=0
        cropped =0
        #while True:
        fingers = None
        while True:


            bg = self.img.copy()
            # get info about hand
            success, img = cap.read()
            img = cv2.flip(img, 1)

            img, lmListR, lmListL, handedness = detector.get_info(img)

            if len(lmListR) != 0 or len(lmListL) != 0:
                fingers = detector.fingerCounter(hand = 'Left')

                if handedness == 'Right':
                    x, y = lmListR[8][1], lmListR[8][2]

                elif handedness == 'Left':
                    x, y = lmListL[8][1], lmListL[8][2]

                print(x,y)







            if fingers == [0,1,0,0,0]:

                if start:
                    startx, starty = x,y
                    start=False
                # cap.release()
                # cv2.destroyAllWindows()
                # break
                cropping = cv2.rectangle(bg,(startx,starty),(x,y),(0,0,0),3)
                cv2.imshow('cropping',cropping)

                cropped = cropping[starty:y,startx:x]
                try:cv2.imshow('cropped',cropped)
                except:pass




            else:

                cv2.circle(bg,(x,y),3,(0,0,0),-1)
                cv2.imshow('start',bg)

                if fingers ==[0,1,1,0,0]:
                    coordinates = [startx, starty, x, y]

                    if self.save:
                        self.save_coordinates(coordinates)
                    return cropped, coordinates

                # if end:
                #     cap.release()
                #     cv2.destroyAllWindows()
                #     break
                #
            cv2.waitKey(1)






class IsolateColor:

    def __init__(self,
                 img
                 ):


        self.img_result= []

        self.img= img
        self.hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    # get values from trackbars
    # add them to lower and upper arrays
    # create mask with lower and upper
    def mask(self,value):




        h_min = cv2.getTrackbarPos("hue min", "trackbars")
        h_max = cv2.getTrackbarPos("hue max", "trackbars")
        s_min = cv2.getTrackbarPos("sat min", "trackbars")
        s_max = cv2.getTrackbarPos("sat max", "trackbars")
        v_min = cv2.getTrackbarPos("value min", "trackbars")
        v_max = cv2.getTrackbarPos("value max", "trackbars")
        blur = cv2.getTrackbarPos("blur", "trackbars")

        print(v_max)
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        blurredImg = cv2.blur(self.hsv, (blur, blur))
        cv2.imshow('hsv', blurredImg)
        mask = cv2.inRange(blurredImg, lower, upper)  # create a mask white are values in the range, black outside range
        cv2.imshow("mask", mask)
        self.img_result = cv2.bitwise_and(self.img, self.img,
                                    mask=mask)  # and with mask and original. if the mask is black- final will apear black. if mask is white final will have color
        cv2.imshow("final", self.img_result)
        number = cv2.countNonZero(mask)
        print(number)

    def create_trackbars(self):
        # create trackbars to control values
        # each trackbar has a min and max value to be controleed and calls a function on change
        cv2.namedWindow("trackbars")
        cv2.resizeWindow("trackbars", 640, 440)
        cv2.createTrackbar("hue min", "trackbars", 0, 179, self.mask)
        cv2.createTrackbar("hue max", "trackbars", 179, 179, self.mask)
        cv2.createTrackbar("sat min", "trackbars", 0, 255, self.mask)
        cv2.createTrackbar("sat max", "trackbars", 255, 255, self.mask)
        cv2.createTrackbar("value min", "trackbars", 0, 255, self.mask)
        cv2.createTrackbar("value max", "trackbars", 255, 255, self.mask)
        cv2.createTrackbar("blur", "trackbars", 1, 255, self.mask)

        cv2.createTrackbar("save", "trackbars", 0, 1, self.save_image)

    def save_image(self,value):
        cv2.imshow("savedFile", self.img_result)
        cv2.imwrite("img.jpg", self.img_result)
        cv2.setTrackbarPos("save", "trackbars", 0)
        print("saved")


class ColorEnhancer():
    def __init__(self,
                 img_path = 'background.png',
                 hsv= False,
                 coordinates=[],
                 r=0,
                 g=0,
                 b=0,
                 h=0,
                 s=0,
                 v=0):


        try: self.img= cv2.imread(img_path)
        except:self.img = img_path

        if len(coordinates)!=0:
            self.cropped = self.img[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]
            self.crop = True
        else: self.crop =False
        self.coordinates = coordinates
        self.enhanced_img = self.img.copy()


        self.hsv=hsv

        self.r,self.g,self.b = cv2.split(self.img)



        if hsv:
            if h == 0 and s == 0 and v == 0:
                self.create_trackbars()

            else:
                self.hsv_mask(None, h, s, v)

        else:
            if r==0 and g==0 and b==0:
                self.create_trackbars()

            else:self.rgb(None,r,g,b)



    def create_trackbars(self):
        cv2.namedWindow("trackbars")
        cv2.resizeWindow("trackbars", 640, 440)

        if self.hsv:
            cv2.createTrackbar("Hue", "trackbars", 0, 255, self.hsv_mask)
            cv2.createTrackbar("Sat", "trackbars", 0, 255, self.hsv_mask)
            cv2.createTrackbar("Value", "trackbars", 0, 255, self.hsv_mask)

        else:
            cv2.createTrackbar("Red", "trackbars", 0, 255, self.rgb)
            cv2.createTrackbar("Green", "trackbars", 0, 255, self.rgb)
            cv2.createTrackbar("Blue", "trackbars", 0, 255, self.rgb)


    def rgb(self,value,red=0,green=0,blue=0):

        if self.crop:
            img = self.cropped
        else: img = self.img
        r,g,b =cv2.split(img)

        try:
            r = r + cv2.getTrackbarPos('Red', 'trackbars')
            g = g + cv2.getTrackbarPos('Green', 'trackbars')
            b = b+cv2.getTrackbarPos('Blue','trackbars')
        except:
            r= r+red
            g= g+green
            b= b+blue


        enhanced_img = cv2.merge((r,g,b))

        if self.crop:
            unchanged = self.img.copy()
            unchanged[self.coordinates[1]:self.coordinates[3], self.coordinates[0]:self.coordinates[2]]= enhanced_img
            self.enhanced_img = unchanged
        else: self.enhanced_img = enhanced_img
        cv2.imshow('enhnced', self.enhanced_img)

    def hsv_mask(self,value,hue=0,sat=0,val=0):

        if self.crop:
            img = self.cropped
        else: img = self.img

        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        h,s,v =cv2.split(hsv)


        try:
            h = h + cv2.getTrackbarPos('Hue', 'trackbars')
            s = s + cv2.getTrackbarPos('Sat', 'trackbars')
            v = v+cv2.getTrackbarPos('Value','trackbars')

        except:
            h= h+hue
            s= s+sat
            v=v+val




        hsv = cv2.merge((h,s,v))
        enhanced_img=cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        cv2.imshow('enhnced', enhanced_img)

        if self.crop:
            unchanged = self.img.copy()
            unchanged[self.coordinates[1]:self.coordinates[3], self.coordinates[0]:self.coordinates[2]]= enhanced_img
            self.enhanced_img = unchanged
        else: self.enhanced_img = enhanced_img
        cv2.imshow('enhnced', self.enhanced_img)


    def lab(self):

        if self.crop:
            img = self.cropped
        else: img = self.img


        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8,8))

        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
        l, a, b = cv2.split(lab)  # split on 3 different channels

        l2 = clahe.apply(l)  # apply CLAHE to the L-channel

        lab = cv2.merge((l2,a,b))  # merge channels
        enhanced_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR

        if self.crop:
            unchanged = self.img.copy()
            unchanged[self.coordinates[1]:self.coordinates[3], self.coordinates[0]:self.coordinates[2]]= enhanced_img
            self.enhanced_img = unchanged
        else: self.enhanced_img = enhanced_img
        cv2.imshow('Increased contrast', self.enhanced_img)






def white_to_transparent(img,name):
    # read the image
    #image_bgr = cv2.imread('pointer.png')
    image_bgr =img
    # get the image dimensions (height, width and channels)
    h, w, c = image_bgr.shape
    # append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
    image_bgra = np.concatenate([image_bgr, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
    # create a mask where white pixels ([255, 255, 255]) are True
    white = np.all(image_bgr == [255, 255, 255], axis=-1)
    # change the values of Alpha to 0 for all the white pixels
    image_bgra[white, -1] = 0
    # save the image
    cv2.imwrite(f'{name}.png', image_bgra)

'''
finds an optimal value for whatever based on some variable
@params
func - function to run
        must accept one variable (the optimal var we are trying to find) 
        and must return a value where the best value is known and considered optimal
best - best case scenario for the func to return
range- range of variables to check
step - chnage in the variable on each iterartions

@:return
results : {

best variable found
highest value achieved
lowest value achieved
}

'''



class Optimiser():
    def __init__(self,
                 func,
                 best,
                 worst,
                 range,
                 step):
        self.func = func
        self.best = best
        self.worst= worst
        self.range =range
        self.step = step

        self.results = {}

    def optimise(self, start):

        best = self.worst

        for i in range(self.range):
            var = start +i*self.step
            temp = self.func(var)

            if temp!=-1:


                if i ==0:
                    worst = temp
                    self.results['lowestt value achieved'] = temp

                elif temp<worst:
                    self.results['lowest value achieved'] = temp

                if temp > best:
                    best =temp
                    self.results['best_var_found'] =var
                    self.results['highest value achieved'] =best


        return self.results



#best var will be 100
#worst will be 0
def test_func(var):
    return var

def camera_var(var):
    detector = handLandmarks.handDetector()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_SATURATION, var)
    success, img = cap.read()

    img = cv2.flip(img, 1)

    img, lmListR, lmListL, handedness = detector.get_info(img)
    cv2.imshow('img', img)
    cv2.waitKey(1)


    try:
        for handType in detector.results.multi_handedness:
            print(handType.classification[0].score)
            score = handType.classification[0].score
        return score


    except Exception as e:
        print(e)
        return -1




if __name__ == '__main__':

    # cap = cv2.VideoCapture("/dev/video2")
    # cap.set(3, 1280)
    # cap.set(4, 720)
    # cap.set(cv2.CAP_PROP_CONTRAST, 10000)
    # success, imgB = cap.read()
    #
    # cv2.imshow('image before', imgB)
    #
    # cap.release()
    #
    # cap = cv2.VideoCapture("/dev/video2")
    # cap.set(3, 1280)
    # cap.set(4, 720)
    # cap.set(cv2.CAP_PROP_CONTRAST, 10000)
    # cap.set(cv2.CAP_PROP_GAIN,1000)
    #
    #
    #
    #
    # success, imgA = cap.read()
    #
    # cv2.imshow('image after', imgA)
    #
    # cv2.waitKey(0)


    # detector = handLandmarks.handDetector()
    # cap = cv2.VideoCapture(0)
    #
    # while True:
    #     success,img = cap.read()
    #
    #     img = cv2.flip(img, 1)
    #
    #     img, lmListR, lmListL, handedness = detector.get_info(img)
    #
    #     cv2.imshow('img',img)
    #
    #
    #     try:
    #         for handType in detector.results.multi_handedness:
    #             print(handType.classification[0].score)
    #
    #     except Exception as e: print(e)
    #
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         cap.release()
    #         cv2.destroyAllWindows()
    #         break


    # test = Optimiser(camera_var,1,0,10,10)
    #
    # #print(cap.get(cv2.CAP_PROP_CONTRAST))
    # results = test.optimise(0)
    # #
    # print(results)


    img = cv2.imread('/home/yaron/Downloads/IMG_20220519_012918.jpg')
    img = cv2.resize(img,(1280,720))
    cv2.imshow('or',img)



    filter = UIMain.Filter(img = img)

    filter.circular(func='GRADIENT_COLOR_ENHANCE', color= (0,0,255), radius_res=10, radius_range=(0,720,1),angle_res=700)


    new = cv2.cvtColor(filter.hsv_img, cv2.COLOR_HSV2RGB)
    cv2.imshow('dil', filter.hsv_img)
    cv2.imshow('new', filter.img)
    cv2.waitKey(0)



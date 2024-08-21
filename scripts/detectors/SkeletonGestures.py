#instaed of creating numerical data with angle lists we will attemot to simplify the images of the gestures
#and pass those to a neaural network to try determine the gestures
import numpy as np
from datetime import datetime
import cv2
from scripts.detectors import handLandmarks as hl
import os
from definitions.config import ROOTDIR
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras import layers

from tensorflow.keras.callbacks import TensorBoard


class SkeltonGesture():

    def __init__(self,
                 name= 'default',):
        self.img = np.zeros((180,180))
        self.name = name
        self.img = None
        self.cap = cv2.VideoCapture(0)
        self.detector = hl.handDetector()
        self.thresh = 0.9

        try: self.model = self.load_model()
        except: print('no model')


    def run(self):


        while True:
            success, img = self.cap.read()


            img = cv2.flip(img, 1)

            img, lmListR, lmListL, handedness = self.detector.get_info(img)

            if len(lmListR) != 0:
                # skeleton.view_skeleton(img,lmListR)
                # print(lmListR)
                points = self.get_skelton_points(lmListR)
                self.view_skeleton(img, points)

                test_img = cv2.resize(skeleton.img, (180, 180))
                test_img = test_img.reshape(-1, 180, 180, 3)
                # print(model.predict(test_img))
                predictions = self.model.predict(test_img)
                classIndex = np.argmax(predictions, axis=-1)
                # classIndex = model.predict_classes(img)
                probabilityValue = np.amax(predictions)  # the highest value in predictions is the most likely class
                # of the given image
                if probabilityValue>self.thresh:
                    ges = skeleton.getCalssName(classIndex)
                else:
                    ges = 'None'
                cv2.putText(img, str(classIndex) + " " + ges, (120, 35),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                            (0, 0, 255), 2, cv2.LINE_AA)
                cv2.putText(img, str(round(probabilityValue * 100, 2)) + "%", (180, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                            (0, 0, 255),
                            2, cv2.LINE_AA)
                #
            #
            cv2.imshow('org', img)

            if cv2.waitKey(1) and 0xFF == ord('q'):
                break

    def gather_data(self, name):

        n=0
        while True:
            success, img = self.cap.read()


            img = cv2.flip(img, 1)

            img, lmListR, lmListL, handedness = self.detector.get_info(img)


            if len(lmListR) != 0:
                points = self.get_skelton_points(lmListR)
                self.view_skeleton(img, points)
                if n%10==0:
                    self.save_features(name)

                n+=1

            cv2.imshow('org', img)



            if cv2.waitKey(1) and 0xFF == ord('q'):
                break




    def get_skelton_points(self,lmList):
        points = []
        for i in lmList:
            x,y = i[1], i[2]

            points.append((x,y))
        return points




    def view_skeleton(self,img,lmList):

        lmList = lmList[:-1]
        bg = np.zeros_like(img)

        skel = cv2.fillPoly(bg, np.int32([lmList]), (255,255,255))
        self.img = skel


        cv2.imshow('skeleton',skel )


    def save_features(self, name):
        cv2.imwrite(os.path.join(ROOTDIR,'datasets','img_datasets',str(name) ,datetime.now().strftime('%c') + '.jpg') , self.img)
        print(f'image saved as {name}')

    def load_datasets(self,path='datasets/img_datasets'):
        batch_size = 10
        img_height = 32
        img_width = 32
        #data_dir = os.path.abspath('/home/yaron/PycharmProjects/SmartController/datasets/img_datasets/')
        data_dir = os.path.join(ROOTDIR,path)

        train_ds = tf.keras.utils.image_dataset_from_directory(
          data_dir,
          validation_split=0.2,
          subset="training",
          seed=123,
          image_size=(img_height, img_width),
          batch_size=batch_size)

        val_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)


        AUTOTUNE = tf.data.AUTOTUNE

        train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

        self.train_ds, self.val_ds = train_ds, val_ds

        return train_ds, val_ds
    def train_model(self):

        train_ds, val_ds = self.load_datasets()

        num_classes = 4

        model = tf.keras.Sequential([
            tf.keras.layers.Rescaling(1. / 255),
            #tf.keras.layers.RandomFlip("horizontal_and_vertical"),
            #tf.keras.layers.RandomRotation(0.2),
            tf.keras.layers.RandomTranslation(0.2,0.2),
            tf.keras.layers.Conv2D(32, 3, activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(num_classes,activation='softmax') #this layer will return probabilities
        ])
        #
        model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            metrics=['accuracy'])
        #

        #tensorboard for evaluating model
        log_dir = 'log/fit/ ' + datetime.now().strftime('%Y%m%d-%H%M%S')
        callbacks = [TensorBoard(log_dir=log_dir,
                                 histogram_freq=1,
                                 write_graph=True,
                                 #write_images=True,
                                 update_freq='epoch',
                                 profile_batch=2,
                                 embeddings_freq=1
                                 )]

        model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=10,
            callbacks=callbacks
        )
        #
        model.save(os.path.join(ROOTDIR,'models','gesmodel'))
        model.save_weights(os.path.join(ROOTDIR,'models','modelweights.h5'))

        # outputfile = 'ges_module.p'
        # with open(outputfile, 'wb') as out:
        #     pickle.dump(model,out)
        return model
    def getCalssName(self,classNo):
        #if   classNo == 0: return 'Speed Limit 20 km/h'
        if   classNo == 0: return 'flash end'
        elif classNo == 1: return 'flash start'
        elif classNo == 2: return 'gun end'
        elif classNo == 3: return 'gun start'
        # elif classNo == 4: return '4 fingers'
        # elif classNo == 5: return '5 fingers'

    def load_model(self, name = 'gesmodel', weights='modelweights.h5'):
        self.model = load_model(os.path.join(ROOTDIR,'models',name))
        self.model.load_weights(os.path.join(ROOTDIR,'models',weights))
        return self.model


if __name__ == '__main__':


    skeleton = SkeltonGesture()


    #skeleton.run()

    #skeleton.gather_data(name= 'gun_start')
    skeleton.train_model()





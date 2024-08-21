'''
This script communicates with home assistant via request module
'''

from requests import get, post
import time
import asyncws
import asyncio
import threading
import json

import cv2
import numpy as np

#this is the python_access token created on the docker ha running on this laptop
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxOGE1YWEzZjA2YzA0YTliOWE5NTA0NTU1YmJlZjMyYyIsImlhdCI6MTcxODU1NTIxNSwiZXhwIjoyMDMzOTE1MjE1fQ.5QsqNlY55sJvoTEe30v62t4rBctDnRUAaE7j0OaTpgY"

class HAController():

    def __init__(self,
                 host,
                 token,
                 port = 8123,
                 entities=[],
                 fp =None,
                 event_func=None,

                 ):

        self.host = host
        self.port = port
        self.TOKEN = token # get the token form home assistant profile page
        #self.url = url # url of homeassistant
        self.url = 'http://{}:{}'.format(self.host, self.port)
        self.headers ={
            "Authorization": "Bearer " + str(self.TOKEN),
            "content-type": "application/json",
        }


        self.entities = entities
        self.cache = {}

        try:response = get(self.url, headers=self.headers)
        except Exception as e: print(f"failed to connect to home assistant with {e}")
        else: print("connected to home assistant successfully")

        self.fp = fp


        self.init_states()

        self.start = True

        self.event_func=event_func



    #enter the entity id in plain test eg light.kitchen_bulb
    #return its state
    def get_entity_state(self, entity_id):

        url = self.url + "/api/states/" + entity_id
        response = get(url, headers=self.headers)
        return response.text


    #control an entity in ha by proving snetit in plain text
    # the data should be given as a dict which corrosponds to a relavant option in entity stae
    #eg '{"state":"on"}'
    # args shoulfd be given as (entity_id, data)
    def set_entity(self, args):


        entity_id = args[0]
        data = args[1]
        url = self.url + "/api/states/" + entity_id
        response = post(url, headers=self.headers, data=data)
        return response.text

    #control lihjt
    #provide the id as string
    #serive can br turn_off, toggle etc
    #args should be given as (entity_id, service)
    def light(self, args):
        entity_id = args[0]
        service = args[1]
        data = {"entity_id": str(entity_id)}
        url = self.url + "/api/services/light/" + str(service)
        response = post(url, headers=self.headers, json=data)
        return response.text

    def init_states(self):

        for entity_id in self.entities:
            text = self.get_entity_state(entity_id)
            index = text.find('"state"',)
            state = text[index+10]
            if state == 'n':
                state = "on"
            elif state == 'f':
                state = "off"

            self.cache[entity_id] = state

        #self.build_floorplan_image()

    def build_floorplan_image(self):

        bg = self.fp.bg
        for key, value in self.cache.items():
            if value == 'on':
                image_name = key[key.find(".") + 1:]
                bg = fp.add_transparent_image(bg, self.fp.images[image_name])
                self.fp.final = bg


    #the following is used to monitor home assisatnt for state changes

    #listens to changes
    async def initSocket(self):

        websocket = await asyncws.connect('ws://{}:{}/api/websocket'.format(self.host, self.port))

        await websocket.send(json.dumps({'type': 'auth', 'access_token': self.TOKEN}))
        await websocket.send(json.dumps({'id': 1, 'type': 'subscribe_events', 'event_type': 'state_changed'}))

        #self.build_floorplan_image()
        print("Start socket...")


        while True:
            message = await websocket.recv()
            if message is None:
                break

            try:

                data = json.loads(message)['event']['data']
                entity_id = data['entity_id']

                if entity_id in self.entities:

                    print("writing {} to cache".format(entity_id))

                    if 'unit_of_measurement' in data['new_state']['attributes']:
                        self.cache[entity_id] = "{} {}".format(data['new_state']['state'],
                                                          data['new_state']['attributes']['unit_of_measurement'])
                    else:
                        self.cache[entity_id] = data['new_state']['state']

                    print(f'chach is  {self.cache}')
                    try:self.event_func()
                    except Exception as e: print(e)
                    #self.build_floorplan_image()





            except Exception as e:
                pass
            #cv2.imshow('bg', self.fp.final)
            #cv2.waitKey(1)
            #await asyncio.sleep(0.1)








    #logs the changes
    async def initLogger(self):


        print("Start logger...")

        await asyncio.sleep(1)


        while True:
            if len(self.cache) == 0:
                await asyncio.sleep(2)

            else:
                try:
                    #bg = fp.bg
                    # for key,data in self.cache.items():
                    #     # Do something here:
                    #
                    #     print(f"{key} is {data} ")

                    cv2.imshow('bg', self.fp.final)
                    cv2.waitKey(1)


                    await asyncio.sleep(0.1)

                except Exception as e:
                    print(e)

    #runs the change listener asychronously
    async def state_listener(self):
        listen = asyncio.create_task(self.initSocket())
        log = asyncio.create_task(self.initLogger())
        await listen
        await log


class FloorPlan():

    def __init__(self,
                 bg_image, # pass name of image 'Dark' or a cv2image
                 images, # pass list with names ['Bathhrom', etc] or dict { 'name' : cv2.image }
                 ):

        try: self.bg = cv2.imread(os.path.join(ROOTDIR, 'images','floor_plan', str(bg_image) + '.png'))
        except:self.bg_image = bg_image,

        self.images = {}
        try:
            for i in images:
                im= os.path.join(ROOTDIR, 'images','floor_plan', str(i)+ '.png')
                if im is None:
                    print(f' the image named {i} could not be loaded')
                self.images[i] = cv2.imread(im,-1)

        except: self.images = images

        self.final = self.bg

    def add_transparent_image(self, bg, foreground, x_offset=None, y_offset=None):
        background = bg.copy()
        bg_h, bg_w, bg_channels = background.shape
        fg_h, fg_w, fg_channels = foreground.shape

        assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
        assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

        # center by default
        if x_offset is None: x_offset = (bg_w - fg_w) // 2
        if y_offset is None: y_offset = (bg_h - fg_h) // 2

        w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
        h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

        if w < 1 or h < 1: return

        # clip foreground and background images to the overlapping regions
        bg_x = max(0, x_offset)
        bg_y = max(0, y_offset)
        fg_x = max(0, x_offset * -1)
        fg_y = max(0, y_offset * -1)
        foreground = foreground[fg_y:fg_y + h, fg_x:fg_x + w]
        background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

        # separate alpha and color channels from the foreground image
        foreground_colors = foreground[:, :, :3]
        alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

        # construct an alpha_mask that matches the image shape
        alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

        # combine the background with the overlay image weighted by alpha
        composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

        # overwrite the section of the background image that has been updated
        background[bg_y:bg_y + h, bg_x:bg_x + w] = composite

        return background


# if __name__ == "__main__":
#     asyncio.run(main())

if __name__ == "__main__":

    from definitions.config import ROOTDIR
    import os

    from scripts.UI.FloorPlan import Controller as fp_c

    bg_image = 'Dark'

    images = ['bathroom', 'living_room_open_b', 'kitchen_bulb']

    fp = FloorPlan(bg_image, images)

    #fp = fp_c(images= images, bg = bg_image)

    #
    # bg = fp.bg
    # for name, value in fp.images.items():
    #
    #     # if value is None:
    #     #     print(name)
    #     bg = fp.add_transparent_image(bg, value)
    #
    #
    # cv2.imshow('bg', bg)
    # cv2.waitKey(0)


    from definitions.Secrets import docker_token as token

    from scripts.UI.FloorPlan import Cursor
    from scripts.detectors import handLandmarks


    hand = handLandmarks.handDetector()

    cursor = cv2.imread(os.path.join(ROOTDIR, 'images', 'floor_plan', 'cursor.png'), -1)


    curs = Cursor(bg = fp.bg, cursor_img=cursor)

    HA = HAController(host = "192.168.58.243", token = token, entities=['light.living_room_open_b', 'light.kitchen_bulb', 'light.bathroom'], fp=fp)



    async def webcam():
        cap = cv2.VideoCapture(0)

        while True:
            success,img = cap.read()

            img, lmListR, lmListL, handedness = hand.get_info(img)

            print(img.shape)

            if len(lmListL)!=0:
                x = lmListL[8][1]
                if x<215:
                    x=372
                elif 215<x< 400:
                    x= 724
                elif 400<x:
                    x =1225
                y = 500
                test = curs.run(fp.final,x,y)
                cv2.imshow('test', test)

            cv2.imshow('webacm', img)
            cv2.waitKey(1)
            print(HA.cache)
            await asyncio.sleep(0.1)

    async def main():
        listen = asyncio.create_task(HA.initSocket())
        #log = asyncio.create_task(HA.initLogger())
        cam= asyncio.create_task(webcam())
        await listen
        # await log
        await cam
    #asyncio.run(HA.state_listener())
    asyncio.run(main())

    #print('k')

    #HA.light(('light.bar_bot_right','turn_on'))

    #print(HA.get_entity_state('light.kitchen_bulb'))
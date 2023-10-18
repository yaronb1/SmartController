import json
import threading
import time

import tinytuya

import re

from definitions.TuyaDevices import CLOUD_DEVICES, CLOUD_CREDENTIALS

class Controller():
    #   outletdevice(deviceid, ip, localkey)
    cv=0
    pv=0







    def __init__(self,
                 cloud = False):


        if cloud:
            self.cloud_connect()

        self.cv =0
        self.pv = 0
    def smoother(self, val,jump,sleep=0.5):
        if val ==0:
            self.cv=0
            self.pv =0
            
        else:
        
            self.cv = self.cv+ val
            cv = (self.cv//jump)*jump
            if cv !=self.pv:
                self.pv =self.cv
                return self.cv
            time.sleep(sleep)

    def cloud_connect(self):

        self.cloud_devices = CLOUD_DEVICES

        region = CLOUD_CREDENTIALS['apiRegion']
        key = CLOUD_CREDENTIALS['apiKey']
        secret = CLOUD_CREDENTIALS['apiSecret']
        device = CLOUD_CREDENTIALS['apiDeviceID']
        try:
            self.cloud = tinytuya.Cloud(
                apiRegion = region,
                apiKey=key,
                apiSecret=secret,
                apiDeviceID=device)
        except: print('couldnt connect to tuya cloud')



    #mode - colour
                    #data - {"h":360, "s":1000, 'v':1000}

    #mode - 'white'
                    #data - {'b': 1000, 't' :1000}

    def rgb_bulb(self, id, mode='mode', data='data'):


        if mode=='colour':
            code = 'colour_data_v2'
            commands = {
                "commands": [
                    {"code": "work_mode", "value": mode},
                    {"code": code, "value": data},
                    # {"code": "bright_value_v2", "value":10}

                ]
            }



        if mode == 'white':
            code = 'bright_value_v2'

            commands = {
                "commands": [
                    {"code": "work_mode", "value": mode},
                    {"code": 'bright_value_v2', "value": data['b']},
                    {"code": 'temp_value_v2', "value": data['t']},

                    # {"code": "bright_value_v2", "value":10}

                ]
            }

        if mode=='switch_on':
            commands = {
                "commands": [
                    {"code": 'switch_led', "value": True},

                ]
            }

        if mode=='switch_off':
            commands = {
                "commands": [
                    {"code": 'switch_led', "value": False},

                ]
            }

        if mode=='toggle':
            state = self.get_device_properties(id)['result'][0]['value']

            commands = {
                "commands": [
                    {"code": 'switch_led', "value": not state},

                ]
            }





        print("Sending command...")
        result = self.cloud.sendcommand(id, commands)
        print("Results\n:", result)

    #value true turn on false turn off
    #id of device
    #code switch 1: 0 or switch 2:1
    def switch_toggle(self,id, code,):
        #id = 'bfead50cf029f5ff14fh6u'


        if code =='switch_1':
            c = 0

        elif code == 'switch_2':
            c = 1
        else: raise Exception('code can be eithr "switch_1" or "switch_2"')

        state = self.get_device_properties(id)['result'][c]['value']
        if state:
            value = False
        else:value=True

        commands = {
            "commands": [
                {"code": code, "value": value},
                #{"code": "colour_data_v2", "value": data},
                #{"code": "bright_value_v2", "value":10}

            ]
        }

        print("Sending command...")
        result = self.cloud.sendcommand(id, commands)
        print("Results\n:", result)

    def change_mode(self,id, mode):
        commands = {
        "commands": [
            {"code": "work_mode", "value": mode},
        ]
    }
        
        
        result = self.cloud.sendcommand(id, commands)

    def get_devices_from_cloud(self):

        # Display list of devices
        devices = self.cloud.getdevices()
        print("Device List: %r" % devices)
        return devices

    def get_device_properties(self, id):
        result = self.cloud.getproperties(id)
        print("Properties of device:\n", result)
        result = self.cloud.getstatus(id)
        print("status of device:\n", result)
        return result

class CloudDevice(Controller):
    '''
    the cloud device is an object for a cloud device
    it will keep a record of the status of the device so that you dont have to get the status from the cloud each time

    each control of the device myust update its status

    '''
    def __init__(self,
                 id):
        self.cloud_connect()
        self.id = id
        self.status = self.get_device_properties()
        
        self.hsv = self.get_hsv()
        
        
    def get_hsv(self):
        status = self.get_device_properties()
        
        hsv_string = self.status['result'][4]['value']
        
        hsv = [int(s) for s in re.findall(r'\d+', hsv_string)]
        
        return hsv


    def get_devices_from_cloud(self):

        # Display list of devices
        devices = self.cloud.getdevices()
        print("Device List: %r" % devices)
        return devices

    def get_device_properties(self,):
        result = self.cloud.getproperties(self.id)
        print("Properties of device:\n", result)
        result = self.cloud.getstatus(self.id)
        print("status of device:\n", result)
        return result
    def send_command(self, cmd):

        result = self.cloud.sendcommand(self.id, cmd)

        
        return result['success']

    # power the device
    # mode - switch_on
    #          switch_off
    #           toggle
    def power(self, mode = 'switch_on'):

        if mode=='switch_on':
            commands = {
                "commands": [
                    {"code": 'switch_led', "value": True},

                ]
            }

            result = self.send_command(commands)
            if result:
                self.status['result'][0]['value'] =True

        elif mode=='switch_off':
            commands = {
                "commands": [
                    {"code": 'switch_led', "value": False},

                ]
            }
            result = self.send_command(commands)
            if result:
                self.status['result'][0]['value'] =False

        elif mode=='toggle':
            state = self.status['result'][0]['value']

            commands = {
                "commands": [
                    {"code": 'switch_led', "value": not state},

                ]
            }

            result = self.send_command(commands)
            if result:
                self.status['result'][0]['value'] =not state


    #mode - 'white'
         # - 'colour'
    def work_mode(self, mode='white'):

        commands = {
            "commands": [
                {"code": 'work_mode', "value": mode},

            ]
        }

        if self.send_command(commands):
            self.status['result'][1]['value'] = mode


     # '''
     # brightness has 2 options
     # one is in white mode in [2]  between 10 -1000
     # in colour mode it is the v in hsv  -  [4]['value']['v'] 0 -1000
     #
     # the adjuster must reflect the range
     # '''
    def adjust_brightness(self, adjuster):
        
        

        if self.status['result'][1]['value']=='white':

            
            brightness = self.status['result'][2]['value'] + adjuster
            commands = {
                "commands": [
                    {"code": 'bright_value_v2', "value": brightness},

                ]
            }

            if self.send_command(commands):
                
                self.status['result'][2]['value'] = brightness
                

        elif self.status['result'][1]['value'] == 'colour':


            
            
            h = self.hsv[0]
            s = self.hsv[1]
            v = self.hsv[2] + adjuster
            
            commands = {
                "commands": [
                    {"code": 'colour_data_v2', "value": {'h':h,'s':s,'v':v}},

                ]
            }

            if self.send_command(commands):
                self.hsv=[h,s,v]
                



    # '''
    # can provide one value for temp or 2 hor hs
    
    
    # '''
    def adjust_temp_colour(self,adjuster, c=None):
        if self.status['result'][1] == 'white':

            temp = self.status['result'][3]['value'] + adjuster
            commands = {
                "commands": [
                    {"code": 'temp_value_v2', "value": temp},

                ]
            }

            if self.send_command(commands):
                self.status['result'][3]['value'] = temp

        elif self.status['result'][1]['value'] == 'colour':

            if c=='s':
                h = self.hsv[0]
                s= self.hsv[1]+adjuster
                v=self.hsv[2]
            
                commands = {
                    "commands": [
                        {"code": 'colour_data_v2', "value": {'h':h,'s':s,'v':v}},

                    ]
                }

                if self.send_command(commands):
                    self.hsv=[h,s,v]
                    
            elif c=='h':
                h = self.hsv[0]+adjuster
                s = self.hsv[1]
                v = self.hsv[2]
                commands = {
                    "commands": [
                        {"code": 'colour_data_v2', "value": {'h':h,'s':s,'v':v}},

                    ]
                }

                if self.send_command(commands):
                    self.hsv=[h,s,v]
                

    def brightness(self):
        return self.status['result'][2]['value']

    def colour(self):
        return self.status['result'][4]['value']

    def temperature(self):
        return self.status['result'][3]['value']

    def mode(self):
        return self.status['result'][1]['value']

    def switch(self):
        return self.status['result'][0]['value']


class LocalDevice(Controller):
    '''
    the cloud device is an object for a cloud device
    it will keep a record of the status of the device so that you dont have to get the status from the cloud each time

    each control of the device myust update its status

    '''
    def __init__(self,
                 id,
                 ip,
                 key,
                 version=3.3):


        self.device = tinytuya.BulbDevice(id,ip,key)
        self.device.set_version(version)

        try:
            self.brightness = self.device.brightness()
            self.temp = self.device.colourtemp()

            #self.hsv = self.device.colour_rgb()
            self.hsv= self.device.colour_hsv()
            #self.hsv=self.device.status()['dps']['24']
            self.state = self.device.state()

            self.mode = self.device.status()['dps']['21']

        except: print(f'cannot connect to {id}')
        else: print(f'connected to  {id}')



    # power the device
    # mode - switch_on
    #          switch_off
    #           toggle
    def power(self, mode = 'switch_on'):

        if mode=='switch_on':
            self.device.turn_on()
            self.state = True


        elif mode=='switch_off':
            self.device.turn_off()
            self.state = False

        elif mode=='toggle':
            if self.state:
                self.device.turn_off()
                self.state = False
            else:
                self.device.turn_on()
                self.state=True


    #mode - 'white'
         # - 'colour'
    def work_mode(self, mode='white'):

        self.device.set_mode(mode)
        self.mode = mode


     # '''
     # brightness has 2 options
     # one is in white mode in [2]  between 10 -1000
     # in colour mode it is the v in hsv  -  [4]['value']['v'] 0 -1000
     #
     # the adjuster must reflect the range
     # '''
    def adjust_brightness(self, adjuster):


        adjust = self.smoother(adjuster,10)
        
        if adjust is not None:
            new_val = self.brightness +adjust
            if new_val >=1000:
                new_val = 1000
            if new_val<=10:
                new_val=10

            self.device.set_brightness(new_val)
            self.hsv=(self.hsv[0],self.hsv[1],new_val/1000)
            self.brightness= new_val


    #set brightness of device
    # 10<brightness <1000
    def set_brightness(self, brightness):
        self.device.set_brightness(brightness)
        self.hsv = (self.hsv[0], self.hsv[1], brightness / 1000)
        self.brightness = brightness



    # '''
    # can provide one value for temp or 2 hor hs
    # '''
    def adjust_temp_colour(self,adjuster, c = 'h'):


        if self.mode == 'white':
            adjust = self.smoother(adjuster,100)
            
            if adjust is not None:
                new_val = self.temp + adjust
                if new_val>=1000:
                    new_val = 1000
                if new_val <=0:
                    new_val = 0
                self.device.set_white(self.brightness,new_val)
                self.temp = new_val

        elif self.mode =='colour':

            adjust = self.smoother(adjuster,100)
            
            if adjust is not None:
                
                h, s, v = self.hsv[0], self.hsv[1], self.hsv[2]
                if c == 'h':
                    h = h + adjust
                    if h>1000:
                        h=0
                    if h<0:
                        h=1000
                    h= h/1000
                elif c=='s':
                    s = s +adjust
                    if s>1000:
                        s=0
                    if s<0:
                        s=1000
                    s=s/1000

                self.device.set_hsv(h,s,v)
                self.hsv = (h,s,v)
                print(h,s,v)

    #set the colour using hue value
    # 10 < hue<1000
    def set_colour(self, hue):

        self.work_mode('colour')
        self.device.set_hsv(hue/1000,self.hsv[1], self.hsv[2])
        self.hsv[0]=hue/1000


    #set colour temp
    # 10 < temp < 1000
    def set_white(self, temp):

        self.work_mode('white')
        self.device.set_white(self.brightness, temp)
        self.temp = temp

                



if __name__ == "__main__":


    t =CloudDevice(id ='bf773c3578dcfd36e6c2tm')
    
    

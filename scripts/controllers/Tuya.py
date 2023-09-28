import json
import threading
import time

import tinytuya

class Controller():
    #   outletdevice(deviceid, ip, localkey)

    ac ={
        'on_cold' : '1PBrNDNQBwgTVAcIEtQGWAbYBdgHVAcIEtgGWAbUBwgTVAcIEtQHDBNQBdwHUAXcBtQGXAbUBdwHUAcIEtgGWAbUBdwHUAXcB1QF3AbUBwgTVAcIE1AHDBLUBdwHUAXcB1QF3AbUBlgG1AaME9AHCBLUBwgTVAXcBtQGWAbUBdwHVAcIE1AF3AbYBlgG1AXcB1AF3AdUBdwG1AZYBtQF3AdUBdwHUAXcBtQGWAbYBdwHUAcIEtgHCBNQBdwHVAcIEtQHCBNUBGmL0AVgB1AHCBNUBdgHVAXcBtQGWAbUBwwTUAXcBtQGWAbYBwgTUAcMEtQGWAbUBdwHVAcIEtQGWAbUBwgTVAVgB1AGWAbUBdwHVAXcB1AF3AbUBlgG2AXYB1QFYAfMBdwG1AZcBtQF3AdQBdwHVAXYBtgGWAbUBdwHUAXcB1QF2AdUBdwG1AZYBtgF2AdUBdwHUAXcBtQGWAbYBdgHVAXcB1AF3AbUBdwHVAXYB1QGjBNUBwgTUAcIEtgGWAbUBwgTVATB1',
        'off' : '1WhrODNUBwwTVAaQE9AFYAdQBdwHVAaQE9AFYAdUBwwS2AcME1QGjBNUBdwHVAXcB1QF3AdUBdwG2AcME1QF3AbUBdwHVAXcB1QF3AdUBpATVAXcB1QHDBLUBdwHVAXcB1QF3AdUBpATUAaQE1QHDBPQBWAHUAXgBtQGWAbYBdwHVAcMEtQGXAdQBWAH0AVgB1QF3AdUBdwG1AXgB1AF3AdUBdwG2AZYBtgF3AfQBWAG1AcME1QF3AfQBbgGgAcME1QGjBNUBKWL0AVgB1QHDBNUBdwHVAXcB1QF3AdUBhAT0AXgBtQGXAbUBdwH0AVgB1QGkBNUBdwHVAcME1AFYAfQBpATVAVcB9QFXAdUBdwHVAXcB1QF3AdUBWAHVAXcB1AF4AbUBlwG1AXcB1QF3AdUBdwG2AZYBtQF4AdQBdwHVAXcB1QF3AbYBdwH0AVgB1AF3AbYBdwHVAXcB9AFYAdUBdwG1AXgB9AFXAfUBowS2AcME1QHDBNQBpATVAXcB1QF3AdUBpATVATB1',
    }

    cloud_devices = {
        'device name': 'id',
        'kitchen': "64560500ecfabc7b40e1",
        'bar bot right': 'bfead50cf029f5ff14fh6u',
        'bar bot left': 'bfd40a82ebd4edd7489qsl',
        'bar top': 'bf773c3578dcfd36e6c2tm',
        'Aqua lamp': 'bf34bfbf3fbacd9f8fu3vs',
        'living room': '107586368caab5df06de',
        'Smart IR': 'bfa29112b2eb1242967nhv',
        'heater' : 'bf7757111274e8df019rgw',
        'our heater': 'bf88f8d9637a6209cclukv',
        'night light': 'bf40667rf70c9sae',
        'tester plug' : '246014102462ab4189a6',
        'Air' : 'bfd2790ca058137e1dgnst',
        'Audio' : 'bfd79969c065b03be3zwzi',

    }





    def __init__(self):

        # t1 = threading.Thread(target =  self.cloud_connect, daemon=True)
        # t1.start()

       # self.cloud_connect()

        # self.kitchen = tinytuya.OutletDevice('64560500ecfabc7b40e1', '192.168.1.137', '3f048184b29328d4')
        # self.kitchen.set_version(3.3)
        # self.living_room = tinytuya.OutletDevice('107586368caab5df06de', '192.168.1.166', 'c4cfc5c4742dee44')
        # self.living_room.set_version(3.3)
        # self.ir = tinytuya.OutletDevice('bfa29112b2eb1242967nhv', '192.168.1.198', 'cc8f3c0d549a7cc8')
        # self.ir.set_version(3.3)
        #
        #
        # self.bar_top= tinytuya.OutletDevice('bf773c3578dcfd36e6c2tm','192.168.1.191' , '_vH$xs<A!g[eRu%]')
        # self.bar_top.set_version(3.3)
        #
        # self.bar_botr = tinytuya.BulbDevice('bfead50cf029f5ff14fh6u', '192.168.1.199', ';J+XZ.t-HiL^J`_Y')
        # self.bar_botr.set_version(3.4)
        #
        self.bar_botl = tinytuya.BulbDevice('bfd40a82ebd4edd7489qsl', '192.168.1.141', 'J{S-2As|ZUD/Pv$C')
        self.bar_botl.set_version(3.4)
        #
        #
        # self.tester_plug = tinytuya.OutletDevice('246014102462ab4189a6','192.168.43.149','4cbb91435bfdc2c2')
        # self.tester_plug.set_version(3.3)


        self.cv =0
        self.pv = 0

    def smoother(self, val,jump,sleep=0.1):
        self.cv = self.cv+ val

        cv = (self.cv//jump)*jump

        if cv !=self.pv:
            self.pv =self.cv
            return self.cv

        time.sleep(sleep)


    def cloud_connect(self):

        try:
            self.cloud = tinytuya.Cloud(
                apiRegion="eu",
                apiKey="uf9snq4abh36n6uvprts",
                apiSecret="5f47cde0092c4ec59207fd6f1ba29208",
                apiDeviceID="bf773c3578dcfd36e6c2tm")
        except: print('couldnt connect to tuya cloud')



    def ac_remote(self, command):
        send = {
            'control': 'send_ir',
            'head': '',
            'key1': self.ac[command],
            'type': 0,
            'delay': 300
        }
        payload = self.ir.generate_payload(tinytuya.CONTROL, {'201': json.dumps(send)})

        self.ir.send(payload)




    # def kitchen_turn_on(self):
    #     self.kitchen.turn_on(switch=1)
    #
    # def kitchen_turn_off(self):
    #     self.kitchen.turn_off(switch=1)
    #
    # def kitchen_toggle(self):
    #     data = self.kitchen.status()
    #     switch_state = data['dps']['1']
    #     data = self.kitchen.set_status(not switch_state)  # This requires a valid key
    #
    # def couch_turn_on(self):
    #     self.living_room.turn_on(switch=1)
    #
    # def couch_turn_off(self):
    #     self.living_room.turn_off(switch=1)
    #
    # def couch_toggle(self):
    #     data = self.living_room.status()
    #     switch_state = data['dps']['1']
    #     data = self.living_room.set_status(not switch_state, switch=1)  # This requires a valid key
    #
    # def open_turn_on(self):
    #     self.living_room.turn_on(switch=2)
    #
    # def open_turn_off(self):
    #     self.living_room.turn_off(switch=2)
    #
    # def open_toggle(self):
    #     data = self.living_room.status()
    #     switch_state = data['dps']['2']
    #     data = self.living_room.set_status(not switch_state, switch=2)  # This requires a valid key

    # def all_off(self):
    #     self.open_turn_off()
    #     self.couch_turn_off()
    #     self.kitchen_turn_off()

    # def tester_toggle(self):
    #     data = self.tester_plug.status()
    #     print(data)
    #     switch_state = data['dps']['1']
    #     data = self.tester_plug.set_status(not switch_state)  # This requires a valid key
    #
    #
    # def bar_top(self,data, mode='colour'):
    #     id = 'bf773c3578dcfd36e6c2tm'
    #
    #     commands = {
    #         "commands": [
    #             {"code": "work_mode", "value": mode},
    #             {"code": "colour_data_v2", "value": data},
    #             #{"code": "bright_value_v2", "value":10}
    #
    #         ]
    #     }
    #
    #     print("Sending command...")
    #     result = self.cloud.sendcommand(id, commands)
    #     print("Results\n:", result)
    #
    # def bar_botr_control(self,data, mode='colour'):
    #     id = 'bfead50cf029f5ff14fh6u'
    #
    #     commands = {
    #         "commands": [
    #             {"code": "work_mode", "value": mode},
    #             {"code": "colour_data_v2", "value": data},
    #             #{"code": "bright_value_v2", "value":10}
    #
    #         ]
    #     }
    #
    #     print("Sending command...")
    #     result = self.cloud.sendcommand(id, commands)
    #     print("Results\n:", result)


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

        if self.status['result'][1]=='white':

            brightness = self.status['result'][2]['value'] + adjuster
            commands = {
                "commands": [
                    {"code": 'bright_value_v2', "value": brightness},

                ]
            }

            if self.send_command(commands):
                self.status['result'][2]['value'] = brightness

        elif self.status['result'][1] == 'colour':


            h = self.status['result'][4]['value']['h']
            s = self.status['result'][4]['value']['s']
            v = self.status['result'][4]['value']['v'] + adjuster
            commands = {
                "commands": [
                    {"code": 'colour_data_v2', "value": {'h':h,'s':s,'v':v}},

                ]
            }

            if self.send_command(commands):
                self.status['result'][4]['value']['v'] = v



    # '''
    # can provide one value for temp or 2 hor hs
    # '''
    def adjust_temp_colour(self,adjuster):
        if self.status['result'][1] == 'white':

            temp = self.status['result'][3]['value'] + adjuster
            commands = {
                "commands": [
                    {"code": 'temp_value_v2', "value": temp},

                ]
            }

            if self.send_command(commands):
                self.status['result'][3]['value'] = temp

        elif self.status['result'][1] == 'colour':

            h = self.status['result'][4]['value']['h'] + adjuster[0]
            s = self.status['result'][4]['value']['s'] + adjuster[1]
            v = self.status['result'][4]['value']['v']


            commands = {
                "commands": [
                    {"code": 'bright_value_v2', "value": {'h':h,'s':s,'v':v}},

                ]
            }

            if self.send_command(commands):
                self.status['result'][4]['value']['h'] = h
                self.status['result'][4]['value']['s'] = s


    def brightness(self):
        return self.status['result'][2]['value']

    def colour(self):
        return self.status['result'][4]['value']

    def temperature(self):
        return self.status['result'][3]['value']

    def work_mode(self):
        return self.status['result'][1]['value']

    def power(self):
        return self.statu['result'][0]['value']

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

        self.brightness = self.device.brightness()
        self.temp = self.device.colourtemp()
        self.hsv = self.device.colour_hsv()
        self.state = self.device.state()

        self.mode = self.device.status()['dps']['21']



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

        new_val = self.brightness +adjuster
        if new_val >=1000:
            new_val = 1000
        if new_val<=10:
            new_val=10

        self.device.set_brightness(new_val)
        self.brightness= new_val



    # '''
    # can provide one value for temp or 2 hor hs
    # '''
    def adjust_temp_colour(self,adjuster, c = 'h'):


        if self.mode == 'white':
            new_val = self.temp + adjuster
            if new_val>=1000:
                new_val = 1000
            if new_val <=0:
                new_val = 0
            self.device.set_colourtemp(new_val)
            self.temp = new_val

        elif self.mode =='colour':

            h, s, v = self.hsv[0], self.hsv[1], self.hsv[2]
            if c == 'h':
                h = h + adjuster
                if h>=360:
                    h=0
                if h<=0:
                    h=360
            elif c=='s':
                s = s +adjuster
                if s>=1000:
                    s=0
                if s<=0:
                    s=1000

            self.device.set_hsv(h,s,v)
            self.hsv = (h,s,v)




if __name__ == "__main__":
    # cloud = tinytuya.Cloud(
    #     apiRegion="eu",
    #     apiKey="uf9snq4abh36n6uvprts",
    #     apiSecret="5f47cde0092c4ec59207fd6f1ba29208",
    #     apiDeviceID="bf93403d09cada8d43gice")
    #
    # print('connected to cloud')
    #
    # did = 'bf93403d09cada8d43gice'
    # code = 'switch_1'
    #
    # # state = cloud.getstatus(id)['result'][0]['value']
    # #     if state:
    # #         value = False
    # #     else:value=True
    #
    # commands = {
    #     "commands": [
    #         # {"code": code, "value": True},
    #         {"code": "colour_data_v2", "value": {'h': 240, 's': 500, 'v': 1000}},
    #         # {"code": "bright_value_v2", "value":10}
    #
    #     ]
    # }
    #
    # print("Sending command...")
    # result = cloud.sendcommand(did, commands)
    # print("Results\n:", result)

    # c = Controller()
    #
    # print(c.bar_botl.bulb_type)
    # print(c.bar_botl.status())
    # c.bar_botl.set_hsv(0.1,0.1,1)

    # bart = tinytuya.BulbDevice("bfea58dc317140c5eeae9t",'192.168.1.104',"i]xrEx2Q#]4|=3Pd")
    # bart.set_version(3.3)
    #
    # print(bart.status())
    # c = LocalDevice("bfb498a23731ce32e9tbnn",
    #                                         '192.168.1.163',
    #                                         "]NUtEpOJAebA>p#%")
    #
    # print(c.hsv)


    # bar = [c.bar_botr, c.bar_botl, c.bar_top]
    # c.bar_botr.set_m
    #
    # for i  in bar:
    #     print(i.status())


    # bar_top = CloudDevice(id ='bf773c3578dcfd36e6c2tm')
    #
    #
    # print(bar_top.status['result'][0]['value'])
    # bar_top.power(mode = 'switch_on')

    tester = 	tinytuya.BulbDevice('bf93403d09cada8d43gice', '192.168.58.208', "T%45pN6iv5@6rnec")

    tester.set_version(3.4)
    #
    #tester.set_version(3.4)

    tester.turn_off()
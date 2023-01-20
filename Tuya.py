import json
import threading

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

    }





    def __init__(self):

        t1 = threading.Thread(target =  self.cloud_connect, daemon=True)
        t1.start()

        self.kitchen = tinytuya.OutletDevice('64560500ecfabc7b40e1', '192.168.1.137', 'cd893e334a9bd26f')
        self.kitchen.set_version(3.3)
        self.living_room = tinytuya.OutletDevice('107586368caab5df06de', '192.168.1.166', '0d81f8e3c9995536')
        self.living_room.set_version(3.3)
        self.ir = tinytuya.OutletDevice('bfa29112b2eb1242967nhv', '192.168.1.198', 'cc8f3c0d549a7cc8')
        self.ir.set_version(3.3)
        self.bar_top= tinytuya.OutletDevice('bf773c3578dcfd36e6c2tm','192.168.1.191' , 'fe08cf39c4ae21b7')
        self.bar_top.set_version(3.3)

        self.bar_botr = tinytuya.BulbDevice('bfead50cf029f5ff14fh6u', '192.168.1.197', '877857a6c63fa853')
        self.bar_botr.set_version(3.4)


        self.tester_plug = tinytuya.OutletDevice('246014102462ab4189a6','192.168.43.149','4cbb91435bfdc2c2')
        self.tester_plug.set_version(3.3)



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
                    #data - {"h":360, "s":360, 'v':1000}

    def rgb_bulb(self, id, mode, data):


        commands = {
            "commands": [
                {"code": "work_mode", "value": mode},
                {"code": "colour_data_v2", "value": data},
                #{"code": "bright_value_v2", "value":10}

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



if __name__ == "__main__":

    c = Controller()
    c.cloud_connect()
    # c.bar_botr_control(data = {"h":300, "s":100, 'v':152})
    # c.bar_botr.set_colour(255,255,0)
    # # data = c.bar_botr.status()
    # # print(data)

    #c.get_device_properties(c.cloud_devices['kitchen'])
    #c.bulb_control()
    #c.switch_toggle(c.cloud_devices['kitchen'],0)
    #c.cloud_control(True,c.devices['kitchen'],'switch_1')
    c.rgb_bulb(id= c.cloud_devices['bar top'], mode = 'colour', data = {"h":150, "s":360, "v":1000})







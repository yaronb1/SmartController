import json

import tinytuya

class Controller():
    kitchen = tinytuya.OutletDevice('64560500ecfabc7b40e1', '192.168.1.137', 'cd893e334a9bd26f')
    kitchen.set_version(3.3)
    living_room = tinytuya.OutletDevice('107586368caab5df06de', '192.168.1.166', '0d81f8e3c9995536')
    living_room.set_version(3.3)
    ir = tinytuya.OutletDevice('bfa29112b2eb1242967nhv', '192.168.1.198', 'cc8f3c0d549a7cc8')
    ir.set_version(3.3)

    ac ={
        'on_cold' : '1PBrNDNQBwgTVAcIEtQGWAbYBdgHVAcIEtgGWAbUBwgTVAcIEtQHDBNQBdwHUAXcBtQGXAbUBdwHUAcIEtgGWAbUBdwHUAXcB1QF3AbUBwgTVAcIE1AHDBLUBdwHUAXcB1QF3AbUBlgG1AaME9AHCBLUBwgTVAXcBtQGWAbUBdwHVAcIE1AF3AbYBlgG1AXcB1AF3AdUBdwG1AZYBtQF3AdUBdwHUAXcBtQGWAbYBdwHUAcIEtgHCBNQBdwHVAcIEtQHCBNUBGmL0AVgB1AHCBNUBdgHVAXcBtQGWAbUBwwTUAXcBtQGWAbYBwgTUAcMEtQGWAbUBdwHVAcIEtQGWAbUBwgTVAVgB1AGWAbUBdwHVAXcB1AF3AbUBlgG2AXYB1QFYAfMBdwG1AZcBtQF3AdQBdwHVAXYBtgGWAbUBdwHUAXcB1QF2AdUBdwG1AZYBtgF2AdUBdwHUAXcBtQGWAbYBdgHVAXcB1AF3AbUBdwHVAXYB1QGjBNUBwgTUAcIEtgGWAbUBwgTVATB1',
        'off' : '1WhrODNUBwwTVAaQE9AFYAdQBdwHVAaQE9AFYAdUBwwS2AcME1QGjBNUBdwHVAXcB1QF3AdUBdwG2AcME1QF3AbUBdwHVAXcB1QF3AdUBpATVAXcB1QHDBLUBdwHVAXcB1QF3AdUBpATUAaQE1QHDBPQBWAHUAXgBtQGWAbYBdwHVAcMEtQGXAdQBWAH0AVgB1QF3AdUBdwG1AXgB1AF3AdUBdwG2AZYBtgF3AfQBWAG1AcME1QF3AfQBbgGgAcME1QGjBNUBKWL0AVgB1QHDBNUBdwHVAXcB1QF3AdUBhAT0AXgBtQGXAbUBdwH0AVgB1QGkBNUBdwHVAcME1AFYAfQBpATVAVcB9QFXAdUBdwHVAXcB1QF3AdUBWAHVAXcB1AF4AbUBlwG1AXcB1QF3AdUBdwG2AZYBtQF4AdQBdwHVAXcB1QF3AbYBdwH0AVgB1AF3AbYBdwHVAXcB9AFYAdUBdwG1AXgB9AFXAfUBowS2AcME1QHDBNQBpATVAXcB1QF3AdUBpATVATB1',
    }

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


    def kitchen_turn_on(self):
        self.kitchen.turn_on(switch=1)

    def kitchen_turn_off(self):
        self.kitchen.turn_off(switch=1)

    def kitchen_toggle(self):
        data = self.kitchen.status()
        switch_state = data['dps']['1']
        data = self.kitchen.set_status(not switch_state)  # This requires a valid key

    def couch_turn_on(self):
        self.living_room.turn_on(switch=1)

    def couch_turn_off(self):
        self.living_room.turn_off(switch=1)

    def couch_toggle(self):
        data = self.living_room.status()
        switch_state = data['dps']['1']
        data = self.living_room.set_status(not switch_state, switch=1)  # This requires a valid key

    def open_turn_on(self):
        self.living_room.turn_on(switch=2)

    def open_turn_off(self):
        self.living_room.turn_off(switch=2)

    def open_toggle(self):
        data = self.living_room.status()
        switch_state = data['dps']['2']
        data = self.living_room.set_status(not switch_state, switch=2)  # This requires a valid key

    def all_off(self):
        self.open_turn_off()
        self.couch_turn_off()
        self.kitchen_turn_off()




if __name__ == "__main__":

    # # c = Controller()
    # #
    # # c.ac_remote('off')
    #
    # # Connect to Tuya Cloud
    # # c = tinytuya.Cloud()  # uses tinytuya.json
    # c = tinytuya.Cloud(
    #     apiRegion="eu",
    #     apiKey="uf9snq4abh36n6uvprts",
    #     apiSecret="5f47cde0092c4ec59207fd6f1ba29208",
    #     apiDeviceID="bf773c3578dcfd36e6c2tm")
    #
    # # Display list of devices
    # devices = c.getdevices()
    # print("Device List: %r" % devices)
    #
    # # Select a Device ID to Test
    # id = "bf773c3578dcfd36e6c2tm"
    #
    # # Display Properties of Device
    # result = c.getproperties(id)
    # print("Properties of device:\n", result)
    #
    # # Display Status of Device
    # result = c.getstatus(id)
    # print("Status of device:\n", result)
    #
    # commands = {
    #     "commands": [
    #         {"code": "switch_led", "value": True},
    #         {"code": "bright_value_v2", "value": 1000},
    #
    #     ]
    # }
    #
    #
    # # print("Sending command...")
    # # result = c.sendcommand(id,commands)
    # # print("Results\n:", result)


    controller = Controller().open_turn_on()






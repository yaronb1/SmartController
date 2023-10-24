from definitions.TuyaDevices import LOCAL_DEVICES
from scripts.controllers import Remote
from scripts.controllers import Tuya

class Commander:

    def __init__(self):


        self.remote= Remote.Remote()


    def connect_local_devices(self,local_devices):
        connected_devices = {}

        for room, devices_dict in local_devices.items():
            connected_devices[room]={}

            for device_name, device in devices_dict.items():
                print(device)
                print(device_name)
                id = device['id']
                ip = device['ip']
                key = device['key']
                version = device['version']
                d = Tuya.LocalDevice(
                    id=id,
                    ip=ip,
                    key=key,
                    version=version

                )

                try: a = d.device.brightness()
                except Exception as e: print (e)
                else:
                    connected_devices[room][device_name] = d

        print(f'the connected devices are...')
        print(connected_devices)

        self.remote.devices=connected_devices
        self.remote.room= list(connected_devices.keys())[0]
        self.remote.select_device('ALL')

        return connected_devices






    def test(self, args):
        print(f'tuya func called with {args} avriable ')
        #print(args)


    # power options
    def turn_off(self):
        self.remote.turn_off()

    def turn_on(self):
        self.remote.turn_on()
    def toggle(self):
        self.remote.toggle()

    def mode(self,mode):
        self.remote.work_mode(str(mode))

    def set_brightness(self,brightness):
        self.remote.set_brightness(int(brightness))

    def set_clolour(self,hue):
        self.remote.set_colour(int(hue))

    def set_white(self,temp):
        self.remote.set_white(int(temp))





from definitions.TuyaDevices import LOCAL_DEVICES
from scripts.controllers import Remote
from scripts.controllers import Tuya


def connect_local_devices(local_devices):
    connected_devices = {}
    for device_name, device in local_devices.items():
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

        connected_devices[device_name] = d

        print(f'the connected devices are...')
        print(connected_devices)

    return connected_devices

tuya_devices = connect_local_devices(LOCAL_DEVICES)
print(tuya_devices)

remote = Remote.Remote(tuya_devices)
remote.select_device('ALL')




def test(args):
    print(remote)
    print(args)


# power options
def turn_off():
    remote.turn_off()

def turn_on():
    remote.turn_on()
def toggle():
    remote.toggle()

def mode(mode):
    remote.work_mode(mode[0])

def set_brightness(brightness):
    remote.set_brightness(brightness[0])

def set_clolour(hue):
    remote.set_colour(hue[0])

def set_white(temp):
    remote.set_white(temp[0])





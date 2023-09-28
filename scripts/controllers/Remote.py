'''
This class aims to give a convnient way to control the smart devices and their function

'''
import Tuya

class Remote():
    def __init__(self):

        self. devices ={
            'BAR':{
                'bar top':Tuya.CloudDevice(id='bf773c3578dcfd36e6c2tm'),
                'bar bot left': Tuya.CloudDevice(id ='bfd40a82ebd4edd7489qsl' ),
                'bar bot right': Tuya.CloudDevice(id = 'bfead50cf029f5ff14fh6u')
            },

            'GARDEN':[],


        }

        self.selected_device = []
        self.room= None

    def move_to_room(self, room):
        self.room = room

    def select_device(self, device_no):

        if device_no=='ALL':
            self.selected_device = list(self.devices[self.rooms].values())
        else:
            self.selected_device = [list(self.devices[self.room].values())[device_no]]
            self.selected_device_name = list(self.devices[self.room].keys())[device_no]

    def turn_off(self):

        for d in self.selected_device:
            d.power(mode='switch_off')

    def turn_on(self):
        for d in self.selected_device:
            d.power(mode='switch_on')

    def toggle(self):
        for d in self.selected_device:
            d.power(mode='toggle')

    def adjust_brightness(self, adjuster):
        for d in self.selected_device:
            d.adjust_brightness(adjuster)

    def adjust_temp_colour(self, adjuster):
        for d in self.selected_device:
            d.adjust_temp_colour(adjuster)


if __name__ == '__main__':

    remote = Remote()

    remote.move_to_room('BAR')

    remote.select_device(2)

    print(remote.selected_device.id)
    print(remote.selected_device_name)
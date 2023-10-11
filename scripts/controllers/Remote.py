'''
This class aims to give a convnient way to control the smart devices and their function

'''
import time

# import tinytuya
import threading


class Remote():
    def __init__(self,
                 devices= []):

        self.devices = devices



        self.selected_device = []
        try:self.room = list(self.devices.keys())[0]
        except: pass



        self.adjuster = 0
        self.prev_adjuster = 0

        # should prevent the lag of the brightness

    # by sending the cmd only every 100 adjusters
    def smoothe_adjuster(self, adjuster):
        print(f'joy value = {adjuster}')
        if adjuster == 0:
            self.adjuster = 0
            self.prev_adjuster = 0

        else:
            self.adjuster += adjuster
            self.adjuster = (self.adjuster // 100) * 100

            if self.adjuster != self.prev_adjuster:
                # print(f'adjuster  = {self.adjuster}  prev adjuster = {self.prev_adjuster}' )
                self.prev_adjuster = self.adjuster
                return self.adjuster

    def move_to_room(self, room):
        self.room = room

    def select_device(self, device_no):

        if device_no == 'ALL':
            self.selected_device = list(self.devices[self.room].values())
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
            d.power('toggle')

    def adjust_brightness(self, adjuster):

        for d in self.selected_device:
            # t1 = threading.Thread(target = d.adjust_brightness,args = [adjust])
            d.adjust_brightness(adjuster)
            # t1.start()

    def set_brightness(self,brightness):
        for d in self.selected_device:
            d.set_brightness(brightness)


    def adjust_temp_colour(self, adjuster, c=None):

        for d in self.selected_device:
            d.adjust_temp_colour(adjuster, c)
            # t1 = threading.Thread(target = d.adjust_temp_colour,args = [adjust,c])
            # t1.start()

    def set_colour(self, hue):
        for d in self.selected_device:
            d.set_colour(hue)

    def set_white(self, temp):
        for d in self.selected_device:
            d.set_white(temp)

    def work_mode(self, mode='white'):

        for d in self.selected_device:
            d.work_mode(mode)


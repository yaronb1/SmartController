'''
a simple ui used to create movemnets and gesture

name your gesture and give a number of smaples

will call the funcs from gestures.py that create a new csv file and use it to craete the pipline that is defined in AI

single gesture requires num_of_samples

movemnet requires both end and atrt gestures

'''


from tkinter import*
from tkinter import ttk
import os

from definitions.config import ROOTDIR

from scripts.detectors import Gestures

def create(ges,samples,name):




    #collect data




    #add negatives
    #save csv

    # create pipline


    if 'selected' in ges[0].state():
        ges = 'single'

    else: ges = 'movement'

    print(ges,samples,name)

    samples = int(samples)


    if ges =='movement':
        Gestures.create_movement(name, num_of_samples=samples)

    elif ges == 'single':
        Gestures.create_gesture(name, num_of_samples=samples)

def checkbox(state, box):
    if 'selected' in state:
        box.config(state = DISABLED)

    else: box.config(state = NORMAL)


root = Tk() # create the base window / widget

# myLabel1 = Label(root, text = "Cretae new gesture") # create a label(where, text)
# myLabel2= Label(root, text = "my name is yaron")
#
# button = Button(root,text = "click me", state = DISABLED)#change state of button
#
# button.grid(row= 1, column=1)
#
# #myLabel1.pack() # pack shoves the label onto the screen
# myLabel2.grid(row = 0, column = 0)
#
#
# e = Entry(root, width = 50) # create an input field


vars = IntVar()
varm = IntVar()


heading = Label(root,text='CREATE NEW GESTURE')
heading.pack()


single_ges = ttk.Checkbutton(root, text = 'singel gesture', command= lambda : checkbox(single_ges.state(), movement))
movement = ttk.Checkbutton(root, text='movement',command = lambda : checkbox(movement.state(), single_ges))





single_ges.pack()
movement.pack()

num_of_samples = Entry(root)
num_of_samples.insert(0,'number of samples')
num_of_samples.pack()

ges_name = Entry(root)
ges_name.insert(0,'name your gesture')
ges_name.pack()

start_button = Button(root, text='CREATE', command=lambda:create([single_ges, movement], num_of_samples.get(), ges_name.get()))
start_button.pack()
root.mainloop() # loops the code til window exited



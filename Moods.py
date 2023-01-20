
'''
The class aims to have one function to control multiple lights and plugs as well as music etc
in order to creat a specific mood
'''

from SocketController import PiController

def blue(controllers):
    #print(args)
    bar_controller = controllers[0]
    tuya_controller = controllers[1]

    try:
        bar_controller.send_commands(cmd = 'dim blue 100')
        bar_controller.send_commands(cmd='dim red 0')
    except Exception as e: print(e)
    try:tuya_controller.bar_top(data={"h": 100, "s": 456, 'v': 552})
    except Exception as e: print(e)


def purple(controllers):
    #print(args)
    bar_controller = controllers[0]
    tuya_controller = controllers[1]

    try:
        bar_controller.send_commands(cmd = 'dim blue 100')
        bar_controller.send_commands(cmd='dim red 100')
    except Exception as e: print(e)
    try:tuya_controller.bar_top(data={"h":299, "s":1000, 'v':552})
    except Exception as e: print(e)




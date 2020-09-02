import holodeck
from holodeck.environments import *
import numpy as np
import sys
from pynput import keyboard

def a2s(x):
    return ' '.join(str(i) for i in x)

command = np.array([0, 0])

def on_press(key):
    try:
        if key.char == "a":
            command[1] = -1
        if key.char == "d":
            command[1] = 1
        if key.char == "w":
            command[0] = 70
        if key.char == "s":
            command[0] = -70
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    if key.char == "a":
        command[1] = 0
    if key.char == "d":
        command[1] = 0
    if key.char == "w":
        command[0] = 0
    if key.char == "s":
        command[0] = 0
    if key.char == "q":
        command[0] = 10000


#set up holodeck
env = holodeck.make("Rooms-DataGen")
# env = HolodeckEnvironment(scenario=config, start_world=True)
env.reset()

#get file ready
filename = sys.argv[1]
open(filename, "w").close()
output = open(filename, "a")

#put in header
num_angles = 64
angles = np.linspace(0, 360, num_angles)
output.write(f"{num_angles} {a2s(angles)}\n")

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

i=-1
while True:
    i+=1

    if command[0] == 10000:
        break
    print(command)

    #send to holodeck
    env.act("turtle0", command)
    state = env.tick()

    #write what's going on
    output.write(f"GT-Pose {i} {a2s(state['LocationSensor'][0:2])} {state['RotationSensor'][2]}\n")
    output.write(f"Laser {i} {a2s(state['RangeFinderSensor'])}\n")

output.close()
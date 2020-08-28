import holodeck
from holodeck.environments import *
import numpy as np
import keyboard
import sys
# np.set_printoptions(precision=3)
config = {
    "name": "DataGen",
    "world": "Rooms",
    "main_agent": "turtle0",
    "agents":[
        {
            "agent_name": "turtle0",
            "agent_type": "TurtleAgent",
            "sensors": [
				{
                    "sensor_type": "LocationSensor"
                },
                {
                    "sensor_type": "RotationSensor"
                },
                {
                    "sensor_type": "RangeFinderSensor",
                    "configuration": {
                        "LaserCount": 64,
                        "LaserMaxDistance": 10,
                        "LaserAngle": 0,
						"LaserDebug": True
                    }
                }
            ],
            "control_scheme": 0,
            "location": [1.50, 1.50, 1.0],
            "rotation": [0.0, 0.0, 0.0]
        }
    ],

    "window_width":  1280,
    "window_height": 720
}
def a2s(x):
    return ' '.join(str(i) for i in x)

#set up holodeck
env = holodeck.make("Rooms-DataGen")
# env = HolodeckEnvironment(scenario=config, start_world=False)
env.reset()

#get file ready
filename = sys.argv[1]
open(filename, "w").close()
output = open(filename, "a")

#put in header
num_angles = 64
angles = np.linspace(0, 360, num_angles)
output.write(f"{num_angles} {a2s(angles)}\n")

i=-1
while True:
    i+=1
    #get input
    command = np.array([0, 0])
    if keyboard.is_pressed('w'):
        command[0] += 70
    if keyboard.is_pressed('s'):
        command[0] -= 70
    if keyboard.is_pressed('a'):
        command[1] -= 1
    if keyboard.is_pressed('d'):
        command[1] += 1

    if keyboard.is_pressed('q'):
        break

    #send to holodeck
    env.act("turtle0", command)
    state = env.tick()

    #write what's going on
    output.write(f"GT-Pose {i} {a2s(state['LocationSensor'][0:2])} {state['RotationSensor'][2]}\n")
    output.write(f"Laser {i} {a2s(state['RangeFinderSensor'])}\n")

output.close()
import holodeck
from holodeck.environments import *

import numpy as np
import click
import keyboard
np.set_printoptions(precision=3)

config = {
    "name": "Testing",
    "world": "Rooms",
    "main_agent": "auv0",
    "agents":[
        {
            "agent_name": "auv0",
            "agent_type": "AuvAgent",
            "sensors": [
				{
                    "sensor_type": "LocationSensor"
                },
                {
                    "sensor_type": "RangeFinderSensor",
                    "configuration": {
                        "LaserCount": 8,
						"LaserDebug": True
                    }
                }
            ],
            "control_scheme": 0,
            "location": [1.50, 1.50, 3.0],
            "rotation": [20.0, 20.0, 20.0]
        }
    ],
    "window_width":  1280,
    "window_height": 720
}
env = HolodeckEnvironment(scenario=config, start_world=False)
env.reset()

while True:
    #get input
    accel = 1
    command = np.array([0, 0, 0, 0])
    if keyboard.is_pressed('w'):
        command = np.array([0, 1, 1, 1])
    if keyboard.is_pressed('s'):
        command = np.zeros(4)
    if keyboard.is_pressed('a'):
        command = np.array([0.5, 0.5, 0.5, 1])
    if keyboard.is_pressed('d'):
        command = np.array([0.5, 0.5, 1, 0.5])

    #send to holodeck
    env.act("auv0", command)
    # env.act("turtle1", command)
    state = env.tick()

    #print what's going on
    print(f"CNTRL={command}")
    # print(f"auv0: LOC={state['LocationSensor']}, LSR={state['RangeFinderSensor']}")
    # print(f"turtle1: LOC={state['turtle1']['LocationSensor']}, LSR={state['turtle1']['RangeFinderSensor']}")
    # print("")

import holodeck
import numpy as np
import click
np.set_printoptions(precision=3)

env = holodeck.make("Rooms-DataGen")
env.reset()

for _ in range(1000):
    #get input
    command = np.array([0, 0])
    c = click.getchar()
    if c == "w":
        command[0] += 100
    if c == "s":
        command[0] -= 100
    if c == "a":
        command[1] -= 20
    if c == "d":
        command[1] += 20

    #send to holodeck
    state, reward, terminal, info = env.step(command)

    #print what's going on
    print(f"CNTRL={command}, LOC={state['LocationSensor']}, LSR={state['RangeFinderSensor']}")

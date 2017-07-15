#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
from inputs import get_gamepad
import piconzero as pz
import time
import sys

pz.init()

# Control Setup

left_stick = 0.0
right_stick = 0.0

try:
    print('Press CTRL+C to quit')

    # Loop indefinitely
    while True:

        events = get_gamepad()

        for event in events:
            print(event.code, event.state)

            if event.code == "ABS_Y":

                left_stick = event.state
                if left_stick > 130:
                    left_stick = -(left_stick - 130)
                elif left_stick < 125:
                    left_stick = ((-left_stick) + 125)
                else:
                    left_stick = 0.0
                print("Y: " + str(-left_stick))

            if event.code == "ABS_RZ":
                right_stick = event.state
                if right_stick > 130:
                    right_stick = -(right_stick - 130)
                elif right_stick < 125:
                    right_stick = ((-right_stick) + 125)
                else:
                    right_stick = 0.0
                print("Y: " + str(-right_stick))

            power_left = int( (left_stick / 125.0) * 100)
            power_right = int( (right_stick / 125.0) * 100)

            print(power_left, power_right)

            pz.setMotor(0, power_left)
            pz.setMotor(1, power_right)

            # print(event.ev_type, event.code, event.state)


except KeyboardInterrupt:

    # CTRL+C exit, disable all drives
    print("stop")
    pz.stop()
    pz.cleanup( )
print("bye")

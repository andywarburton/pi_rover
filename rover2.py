#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
from inputs import get_gamepad
import piconzero as pz
import time
import sys
import random
import colorsys
import threading

# Initiate motor controller
pz.init()
animation = None

# Control Setup
left_stick = 0.0
right_stick = 0.0

# ACTIVATE BLINKY LIGHTS
pz.setOutputConfig(5, 3)
pz.setBrightness(255)

class Animation(threading.Thread):
    daemon = True
    def __init__(self):
        super(Animation, self).__init__()
        self.style = None

    def run(self,target):
        while self.running:
            self.next_color()
            time.sleep(self.sleeptime)

    def stop(self):
        self.running = False
        self.join()

class Police(Animation):
    colors = [(255,0,0),(0,0,255),(255,255,255)]
    sleeptime = 0.2

    def __init__(self):
        super(Police, self).__init__()
        self.index = 0

    def next_color():
        color = self.colors[self.index]
        self.index = (self.index+1) % len(self.colors)
        pz.setAllPixels(color)

class Rainbow(Animation):
    spacing = 360.0 / 16.0
    sleeptime = 0.001

    def next_color():
        # RAINBOW
        hue = int(time.time() * 100) % 360
        for x in range(16):
            offset = x * self.spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            pz.setPixel(x, r, g, b)
        pz.updatePixels()

class Knightrider(Animation):

    REDS = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0]
    sleeptime = 0.1

    def __init__(self):
        super(Knightrider, self).__init__()
        start_time = time.time()

    def next_color():
        delta = (time.time() - start_time) * 16

        # Triangle wave, a snappy ping-pong effect
        offset = int(abs((delta % 16) - 8))

        for i in range(8):
            pz.setPixel(i , 0, self.REDS[offset + i], 0)

        pz.updatePixels()

def np_downlights():
    # DOWNLIGHTS
    pz.setAllPixels(255,255,255, True)

# Controller events
try:
    print('Press CTRL+C to quit')

    # Loop indefinitely
    while True:

        events = get_gamepad()

        for event in events:
            print(event.code, event.state)

            # face buttons
            if event.code == "BTN_EAST":
                if animation:
                    animation.stop()
                    animation = None
                animation = Knightrider()
                animation.start()
            if event.code == "BTN_SOUTH":
                if animation:
                    animation.stop()
                    animation = None
                animation = Rainbow()
                animation.start()
            if event.code == "BTN_WEST":
                if animation:
                    animation.stop()
                    animation = None
                np_downlights()
            if event.code == "BTN_NORTH":
                if animation:
                    animation.stop()
                    animation = None
                animation = Police()
                animation.start()

            # left stick
            if event.code == "ABS_Y":

                left_stick = event.state
                if left_stick > 130:
                    left_stick = -(left_stick - 130)
                elif left_stick < 125:
                    left_stick = ((-left_stick) + 125)
                else:
                    left_stick = 0.0
                print("Y: " + str(-left_stick))

            # right stick
            if event.code == "ABS_RZ":
                right_stick = event.state
                if right_stick > 130:
                    right_stick = -(right_stick - 130)
                elif right_stick < 125:
                    right_stick = ((-right_stick) + 125)
                else:
                    right_stick = 0.0
                print("Y: " + str(-right_stick))

            # engage the motors
            power_left = int( (left_stick / 125.0) * 100)
            power_right = int( (right_stick / 125.0) * 100)
            pz.setMotor(0, power_left)
            pz.setMotor(1, power_right)

            # print(event.ev_type, event.code, event.state)


except KeyboardInterrupt:

    # CTRL+C exit, disable all drives
    print("stop")
    pz.setAllPixels(0,0,0, True)
    pz.stop()
    pz.cleanup( )
print("bye")

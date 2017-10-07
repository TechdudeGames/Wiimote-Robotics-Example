#!/usr/bin/python3
#Inital Imports
import cwiid
import time
import RPi.GPIO as GPIO
import libpwm as PWM
from blessings import Terminal
import os
##Setting up all the variables
term = Terminal()
cont = True
threshhold = 30 ##Adjustable to fit the needs of the user
speed = 1 ##Inital speed multiplyer
invert = False
right_raw = 0
left_raw = 0
right_movement = 0
left_movement = 0
last_left = 0
last_right = 0
max_speed = 8
##Setting up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, False)
GPIO.setup(12, GPIO.OUT)
GPIO.output(12, False)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, False)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, False)
GPIO.setup(19, GPIO.OUT)
GPIO.output(19, False)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23,False)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, False)
'''Initially setting up the wiimote connection.
This will try to connect to the wiimote.
'''
print ("Press 1 and 2 on your remote now.")
attempt = 0
wm = None
while not wm:
    attempt += 1
    print("Attempt %s" %(str(attempt)))
    try:
        wm=cwiid.Wiimote()
    except:
        print("Failed to connect to the Wiimote on try: %s" %(str(attempt)))
wm.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_NUNCHUK  ##Setting the report modes
os.system("clear")
while cont:
    with term.location(y=0):
        print("Robot status:")
    with term.location(y=1):
        print("Inverted:", invert)
    with term.location(y=2):
        print("Current speed multiplier:", speed)
    with term.location(y=3):
        print("Right target movement:", right_raw, "                             ")
    with term.location(y=4):
        print("Left target movement:", left_raw, "                             ")
    with term.location(y=5):
        print("Other Info:", "                             ")
    term.location(y=6)
    nunchuk = (wm.state.get('nunchuk'))  # This sometimes returns none
    if type(nunchuk) != type(None):  #This is protection if the class of nunchuk is None
        stick_tuple = nunchuk.get('stick')
        stick_list = list(stick_tuple)
        stickx = stick_list[0] - 119
        sticky = stick_list[1] - 125
        if sticky > threshhold or sticky < (-1 * threshhold):
            if stickx > threshhold or stickx < (-1 * threshhold):
                if invert:
                    right_raw = (sticky * speed)
                    left_raw = (sticky * speed)
                if not invert:
                    right_raw = (sticky * speed)
                    left_raw = (sticky * speed)
            else:
                if invert:
                    right_raw = (sticky * speed * -1)
                    left_raw = (sticky * speed * -1)
                if not invert:
                    right_raw = (sticky * speed)
                    left_raw = (sticky * speed)
        elif stickx > threshhold or stickx < (-1 * threshhold):
            left_raw = stickx * speed
            right_raw = (-1 * stickx * speed)
        else:
            right_raw = 0
            left_raw = 0
        if right_raw > threshhold or right_raw < (-1 * threshhold):
            if right_raw < 0:
                right_movement = -100
            elif right_raw > 0:
                right_movement = 100
            PWM.motor_movement(right_movement, right_raw, 1000, 15, 16, 12)
        if left_raw > threshhold or left_raw < (-1* threshhold):
            if left_raw <0:
                left_movement = 100
            elif left_raw >0:
                left_movement = -100
            PWM.motor_movement(left_movement, left_raw, 1000, 15, 21, 20)
    ##Other movement functions

    if wm.state['buttons'] & cwiid.BTN_A:
        if not wm.state['buttons'] & cwiid.BTN_B:
            PWM.motor_movement(100,50,100,20,19,26)
    if wm.state['buttons'] & cwiid.BTN_B:
        if not wm.state['buttons'] & cwiid.BTN_A:
            PWM.motor_movement(100,50,100,20,26,16)
    ###############################################
    if wm.state['buttons'] & cwiid.BTN_LEFT:
        if not wm.state['buttons'] & cwiid.BTN_RIGHT:
            PWM.motor_movement(100,50,100,20,23,24)
    if wm.state['buttons'] & cwiid.BTN_RIGHT:
        if not wm.state['buttons'] & cwiid.BTN_LEFT:
            PWM.motor_movement(100,50,100,20,24,23)
    ##Speed button controllers
    if wm.state['buttons'] & cwiid.BTN_MINUS:
        if speed - 1 < 0:
            speed=max_speed
        else:
            speed += -1
        time.sleep(0.75)
    if wm.state['buttons'] & cwiid.BTN_PLUS:
        if speed +1 > max_speed:
            speed=0
        else:
            speed += 1
        time.sleep(0.75)
    if wm.state['led'] != (speed):
        change = wm.state['led'] - speed
        wm.led = (wm.state['led'] + change)
    if wm.state['buttons'] & cwiid.BTN_1:
        invert = not invert
        time.sleep(0.75)
    if wm.state['buttons'] & cwiid.BTN_HOME:
        print("Stopping program")
        cont = False
        print("Stopping program")
        os.system("clear")
print("Finnished without error")
GPIO.cleanup()
print("Cleaned GPIO.")

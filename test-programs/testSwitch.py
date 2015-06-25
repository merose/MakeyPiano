#!/bin/python
#This script was authored by AndrewH7 and belongs to him (www.instructables.com/member/AndrewH7)
#You have permission to modify and use this script only for your own personal usage
#You do not have permission to redistribute this script as your own work
#Use this script at your own risk

import RPi.GPIO as GPIO
import os

gpio_pin_number=40

GPIO.setmode(GPIO.BOARD)

GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#It's very important the pin is an input to avoid short-circuits
#The pull-up resistor means the pin is high by default

try:
    GPIO.wait_for_edge(gpio_pin_number, GPIO.FALLING)
    #Use falling edge detection to see if pin is pulled 
    #low to avoid repeated polling
    print('Got the switch')
    #Send command to system to shutdown
except:
    pass

GPIO.cleanup()
#Revert all GPIO pins to their normal states (i.e. input = safe)

#! /usr/bin/python

from evdev import InputDevice, categorize, ecodes

if __name__ == '__main__':

  #dev = InputDevice('/dev/input/by-id/usb-JoyLabz_Makey_Makey_v1.20aa_50000000-if01-event-mouse')
  dev = InputDevice('/dev/input/by-id/usb-JoyLabz_Makey_Makey_v1.20aa_50000000-event-mouse')

  for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
      key_pressed = str(categorize(event))
      if 'KEY_LEFT' in key_pressed:
        # 0x5X for left forward. 0x51 very slow. 0x5F fastest
        print "left"
      if 'KEY_RIGHT' in key_pressed:
        # 0x6X for right forward. 0x11 very slow. 0x1F fastest
        print "right"
      if 'KEY_DOWN' in key_pressed:
        # 0x2X for straight backward. 0x21 very slow. 0x2F fastest
        print "down"
      if 'KEY_UP' in key_pressed:
        # 0x1X for straight forward. 0x11 very slow. 0x1F fastest
        print "up"
      if 'KEY_SPACE' in key_pressed:
        #stop
        print "space"
 
      print event.code == ecodes.KEY_A
      print event
      print key_pressed

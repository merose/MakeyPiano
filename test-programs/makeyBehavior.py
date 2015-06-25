from evdev import InputDevice, categorize, ecodes
from pyfirmata import Arduino, util

# Define an enumeration to represent the state of the MakeyMakey touch.

touchStateMap = {
  1: "press",
  2: "hold",
  0: "release"
}

def behavior1(touchState):
  print "behavior 1: " + touchState

def behavior2(touchState):
  print "behavior 2: " + touchState

def behavior3(touchState):
  print "behavior 3: " + touchState

def behavior4(touchState):
  print "behavior 4: " + touchState

def behavior5(touchState):
  print "behavior 5: " + touchState

def behavior6(touchState):
  print "behavior 6: " + touchState

if __name__ == '__main__':

  #board = Arduino('/dev/ttyACM0')

  dev = InputDevice('/dev/input/by-id/usb-JoyLabz_Makey_Makey_v1.20aa_50000000-event-kbd')

  for event in dev.read_loop():
    if 0<=event.value and event.value<=2:
      touchState = touchStateMap[event.value]

    if event.type == ecodes.EV_KEY:
      if event.code == ecodes.KEY_W:
        behavior1(touchState)
      elif event.code == ecodes.KEY_A:
        behavior2(touchState)
      elif event.code == ecodes.KEY_S:
        behavior3(touchState)
      elif event.code == ecodes.KEY_D:
        behavior4(touchState)
      elif event.code == ecodes.KEY_F:
        behavior5(touchState)
      elif event.code == ecodes.KEY_G:
        behavior6(touchState)
      elif event.code == ecodes.KEY_UP:
        print "UP" 
      elif event.code == ecodes.KEY_DOWN:
        print "DOWN" 
      elif event.code == ecodes.KEY_LEFT:
        print "LEFT" 
      elif event.code == ecodes.KEY_RIGHT:
        print "RIGHT" 
      elif event.code == ecodes.KEY_UP:
        print "UP" 
      elif event.code == ecodes.KEY_SPACE:
        print "SPACE"
      else:
        print(event)
        print(categorize(event))
#    else:
#      print(event)
#      print(categorize(event))

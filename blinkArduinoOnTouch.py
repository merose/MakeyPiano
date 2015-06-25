from evdev import InputDevice, categorize, ecodes
from pyfirmata import Arduino, util

if __name__ == '__main__':

  board = Arduino('/dev/ttyACM0')

  dev = InputDevice('/dev/input/by-id/usb-JoyLabz_Makey_Makey_v1.20aa_50000000-event-kbd')

  blink = False

  for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
      if event.code == ecodes.KEY_W:
        print "w"
        if event.value > 0:
          blink = True
        else:
          blink = False
      elif event.code == ecodes.KEY_A:
        print "a"
      elif event.code == ecodes.KEY_S:
        print "s"
      elif event.code == ecodes.KEY_D:
        print "d"
      elif event.code == ecodes.KEY_F:
        print "f"
      elif event.code == ecodes.KEY_G:
        print "g"
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

    if blink:
      board.digital[13].write(1)
    else:
      board.digital[13].write(0)

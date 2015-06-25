from pyfirmata import Arduino, util
import time

board = Arduino('/dev/ttyACM0')

while True:
  board.digital[13].write(1)
  time.sleep(0.5)
  board.digital[13].write(0)
  time.sleep(0.5)

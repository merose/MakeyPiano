import os
import time
os.environ["SDL_VIDEODRIVER"] = "dummy"

from evdev import InputDevice, categorize, ecodes

import pygame

if __name__ == '__main__':

  # Need to pre-init the mixer or the delay between start() and the
  # sound is large, approx. 400ms.
  # See: http://stackoverflow.com/questions/18273722/pygame-sound-delay
  pygame.mixer.pre_init(44100, -16, 2, 1024)

  pygame.init();
  pygame.display.set_mode((1,1))

  dev = InputDevice('/dev/input/by-id/usb-JoyLabz_Makey_Makey_v1.20aa_50000000-event-kbd')

  # Don't need any params since we called pre_ini().
  pygame.mixer.init()

  touchStateMap = {
    1: "press",
    2: "hold",
    0: "release"
  }

  # Ten notes for ten inputs from the MakeyMakey.
  c4 = pygame.mixer.Sound('C4-261.63.wav')
  d4 = pygame.mixer.Sound('D4-293.66.wav')
  e4 = pygame.mixer.Sound('E4-329.63.wav')
  f4 = pygame.mixer.Sound('F4-349.23.wav')
  g4 = pygame.mixer.Sound('G4-392.0.wav')
  a4 = pygame.mixer.Sound('A4-440.0.wav')
  b4 = pygame.mixer.Sound('B4-493.88.wav')
  c5= pygame.mixer.Sound('C5-523.25.wav')
  d5= pygame.mixer.Sound('D5-587.33.wav')
  e5= pygame.mixer.Sound('E5-659.26.wav')

  # Map between input codes and the notes to play.
  noteMap = {
    ecodes.KEY_UP: c4,
    ecodes.KEY_RIGHT: d4,
    ecodes.KEY_DOWN: e4,
    ecodes.KEY_LEFT: f4,
    ecodes.KEY_W: g4,
    ecodes.KEY_A: a4,
    ecodes.KEY_S: b4,
    ecodes.KEY_D: c5,
    ecodes.KEY_F: d5,
    ecodes.KEY_G: e5,
  }

  for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
      if 0<=event.value and event.value<=2:
        touchState = touchStateMap[event.value]

      note = noteMap[event.code]

      if not(note == None):
        if touchState == 'press':
          note.play()
        elif touchState == 'release':
          note.stop()
    

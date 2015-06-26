#! /bin/python

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
  organNotes = [
    pygame.mixer.Sound('audio-files/C4-261.63.wav'),
    pygame.mixer.Sound('audio-files/D4-293.66.wav'),
    pygame.mixer.Sound('audio-files/E4-329.63.wav'),
    pygame.mixer.Sound('audio-files/F4-349.23.wav'),
    pygame.mixer.Sound('audio-files/G4-392.0.wav'),
    pygame.mixer.Sound('audio-files/A4-440.0.wav'),
    pygame.mixer.Sound('audio-files/B4-493.88.wav'),
    pygame.mixer.Sound('audio-files/C5-523.25.wav'),
    pygame.mixer.Sound('audio-files/D5-587.33.wav'),
    pygame.mixer.Sound('audio-files/E5-659.26.wav'),
  ]

  pianoNotes = [
    pygame.mixer.Sound('audio-files/net_C3.wav'),
    pygame.mixer.Sound('audio-files/net_D3.wav'),
    pygame.mixer.Sound('audio-files/net_E3.wav'),
    pygame.mixer.Sound('audio-files/net_F3.wav'),
    pygame.mixer.Sound('audio-files/net_G3.wav'),
    pygame.mixer.Sound('audio-files/net_A3.wav'),
    pygame.mixer.Sound('audio-files/net_B3.wav'),
    pygame.mixer.Sound('audio-files/net_C4.wav'),
    pygame.mixer.Sound('audio-files/net_D4.wav'),
    pygame.mixer.Sound('audio-files/net_E4.wav'),
  ]

  mode = "piano"
  notes = pianoNotes

  # Map between input codes and the notes to play.
  noteMap = {
    ecodes.KEY_UP: notes[0],
    ecodes.KEY_RIGHT: notes[1],
    ecodes.KEY_DOWN: notes[2],
    ecodes.KEY_LEFT: notes[3],
    ecodes.KEY_W: notes[4],
    ecodes.KEY_A: notes[5],
    ecodes.KEY_S: notes[6],
    ecodes.KEY_D: notes[7],
    ecodes.KEY_F: notes[8],
    ecodes.KEY_G: notes[9],
  }

  for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
      if 0<=event.value and event.value<=2:
        touchState = touchStateMap[event.value]

      note = noteMap[event.code]

      if not(note == None):
        if touchState=='press':
          note.stop()
          note.play()
        elif touchState=='release' and mode=='organ':
          note.stop()
    

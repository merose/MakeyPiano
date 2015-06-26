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
    ecodes.KEY_UP: 0,
    ecodes.KEY_RIGHT: 1,
    ecodes.KEY_DOWN: 2,
    ecodes.KEY_LEFT: 3,
    ecodes.KEY_W: 4,
    ecodes.KEY_A: 5,
    ecodes.KEY_S: 6,
    ecodes.KEY_D: 7,
    ecodes.KEY_F: 8,
    ecodes.KEY_G: 9,
  }

  noteHistory = (None, None, None)

  for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
      if 0<=event.value and event.value<=2:
        touchState = touchStateMap[event.value]

      noteIndex = noteMap[event.code]
      note = notes[noteIndex]

      if not(note == None):
        # Need to stop notes if we're in organ mode and the user releases
        # the key. Otherwise we need to play the note if the user presses
        # a key.
        if touchState=='release' and mode=='organ':
          note.stop()
        elif touchState=='press':
          note.stop()
          note.play()

	  # Keep track of note history, and change modes if the user
	  # uses a tritone incantation. Make sure to turn off the organ
          # note if starting piano mode.
	  noteHistory = noteHistory[1:] + (noteIndex,)
	  if noteHistory == (3, 6, 8):
	    mode = "piano"
	    notes = pianoNotes
            note.stop()
            notes[8].play()
	  elif noteHistory == (3, 6, 9):
	    mode = "organ"
	    notes = organNotes

import os
import time
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
pygame.init();
pygame.display.set_mode((1,1))

#pygame.mixer.pre_init(44100, -16, 2, 2048)
#pygame.mixer.init()
pygame.mixer.init(48000, -16, 1, 1024)

c = pygame.mixer.Sound('../audio-files/C4-261.63.wav')
d = pygame.mixer.Sound('../audio-files/D4-293.66.wav')
e = pygame.mixer.Sound('../audio-files/E4-329.63.wav')
f = pygame.mixer.Sound('../audio-files/F4-349.23.wav')
g = pygame.mixer.Sound('../audio-files/G4-392.0.wav')
a = pygame.mixer.Sound('../audio-files/A4-440.0.wav')
b = pygame.mixer.Sound('../audio-files/B4-493.88.wav')
c2= pygame.mixer.Sound('../audio-files/C5-523.25.wav')

scale = [c, d, e, f, g, a, b, c2]

c.play()
time.sleep(0.5)
d.play()
time.sleep(0.5)
e.play()
time.sleep(0.5)
f.play()
time.sleep(0.5)
g.play()
time.sleep(2)

c.stop()
d.stop()
e.stop()
f.stop()
g.stop()

for note in scale:
  note.play()
  time.sleep(1)
  note.stop()
  time.sleep(0.5)

time.sleep(1)

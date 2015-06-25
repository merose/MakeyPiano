import subprocess
import os
import signal
import time

proc = subprocess.Popen(['omxplayer', '--no-keys', '-o', 'local', '../audio-files/SoundHelix-Song-1.mp3'])
time.sleep(3)
subprocess.call(['pkill', 'omxplayer'])

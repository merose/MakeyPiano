# MakeyPiano
Code and setup info for a Raspberry Pi and MakeyMakey piano demo, originally for the [RobotGarden](http://www.robotgarden.org/) display at the 2015
Alameda County Fair in Pleasanton, CA.

# The Hardware

* Raspberry Pi 2
* MakeyMakey, powered by USB from Raspberry Pi
* Momentary, push-button switch across pins 39 and 40 (Ground and GPIO21, resp.), to provide shutdown request for safe power-off
* USB battery to power Raspberry Pi
* Cinch terminal blocks to make the external touch-point connections easier and sturdier. (10-terminal block for the touch-points, 6-terminal block for the ground points.)

When I get a chance, I'll put photos on the Wiki.

The terminal blocks are wired to the MakeyMakey to a ground hole, the holes for the four arrow keys, and the six-pin WASDFG header. The wires to the holes designed for the aligator clips are instead attached with #4x1/4" machine screws, to make the attachment sturdier. The 6-terminal block terminals are all tied to ground, while the 10-terminal block terminals are connected to UP, RIGHT, DOWN, LEFT, W, A, S, D, F, and G, in order, left-to-right. (The order of the arrow keys follows the conventions in the CSS spec, to make it easier to remember: north, east, south, west.)

# Raspberry Pi Setup

* Install NOOBS using local keyboard layout. (en-US, in my case. Note that if you don't set the layout at the bottom of the NOOBS setup screen, you get en-UK, which shows a UK pound symbol instead of a hash.)
* Enable SSH server in raspi-config.
* Create unique SSH keys: `sudo rm /etc/ssh/ssh_host_* && sudo dpkg-reconfigure openssh-server`
* Set a static IP address to make SSH more convenient. (See http://elinux.org/RPi_Setting_up_a_static_IP_in_Debian.)
* Update packages and install a few more.
```
sudo apt-get update # To update the package index
sudo apt-get upgrade # To  update existing packages as needed
sudo apt-get install python-pip python-dev # To get pip and dev
sudo pip install evdev # To be able to read USB keyboard and mouse events
```
* The Pi will generate too much noise, by default, if the audio output amplitude is zero. Turn off audio dithering by adding a setting at the end of `/boot/config.txt`: (This does not take effect until reboot.)

```
disable_audio_dither=1
```

* Install the piano software. Git is already installed by default in NOOBS. Clone the MakeyPiano workspace into the `pi` user home directory:

```
cd ~
git clone https://github.com/merose/MakeyPiano.git
```

* Set up the shutdown switch monitor program. A momentary, pushdown switch is connected between the bottom two pins on the GPIO header, pins 39 and 40. (Other pin pairs are OK, but those are easy to remember.) Pin 40 (GPIO21) will be read using an internal pull-up resistor by the program `shutdownSwitch.py`. When pin 40 goes low, the program will initiate a shutdown via `shutdown -h now`. The `shutdownSwitch.py` program is run at boot time by editing `/etc/rc.local`. Add this line before `return 0`:

```
python /home/pi/MakeyPiano/shutdownSwitch.py &
```

* Edit `/etc/rc.local` to run the piano startup script at boot time. Add this line before `return 0`:

```
/home/pi/MakeyPiano/piano &
```

This is the end of the Pi setup.

# Running the Piano System

## Connecting Touch Points and the Speakers

1. Connect aligator clips or leads from the touch points and ground points to the terminal blocks for notes and ground, as desired.
2. Connect the battery to the Raspberry Pi.
3. Connect the speaker system using a mini-RCA patch cable.
4. Turn on the battery power. The piano system will start automatically at boot time. This may take 10-20 seconds.

## Using the Piano

* The user must touch a ground point and then touch a note touch point. Multiple notes can be played at the same time. (Up to six, usually. However, the audio volume is not adjusted automatically, so there may be more distortion if multiple notes are played simultaneously.)
* By default, the system plays sampled piano tones. To switch to organ tones (continuous sound) instead, play the notes F3, B3, and E4, in order. (The 4th, 7th, and 10th note inputs, numbered from left to right.) To switch back to piano tones, play F3, B3, and D4 in order. (The 4th, 7th, and 9th note inputs.)
* You may need to adjust the speaker volume, of course.

# Piano Software Details

## Shutdown Switch Monitor

The shutdown switch program `MakeyPiano/shutdownSwitch.py` configures pin 40 (GPIO21) as an input, together with an internal pull-up resistor. When the momentary switch is pressed, pin 40 will go low. When the monitor program sees that, it spawns a shell command to halt the Linux system: `shutdown -h now`

To safely stop the system, press the momentary switch and wait a few seconds until the green LED next to the red power LED flashes several times in a row, then turns off. The LEDs on the Ethernet interface will be off, too. At that point it is OK to turn off the power.

## Piano Software

The piano program is `MakeyPiano/piano.py`. It uses the `evdev` library to read keyboard events from the MakeyMakey and PyGame to play audio files for note presses. There is also a shell script that is used to start the Python program, `MakeyPiano/piano`, which first moves to the `MakeyPiano` directory so that the audio files can be loaded using relative paths.

There are two subdirectories:

* `audio-files` contains the audio files for the 10 piano notes. There are two sets of files, one set for piano sounds and one for continuous, organ-like sounds.
* `test-programs` contains Python programs that were used to try out features of Python or the Raspberry Pi while developing the piano software. They may be of historical interest. Two programs uses PyFirmata to talk to an Arduino connected to the Raspberry Pi. (Requires installation of PyFirmata and install of Standard Firmata to the Arduino.)

## Piano Software Inputs

The MakeyMakey emulates a USB keyboard and mouse, returning keyboard events for 11 of its inputs and mouse events for the other 7. The program `piano.py` reads 10 inputs, the four arrow keys on the MakeyMakey board and the keys on one of the two header inputs.

MakeyMakey input | Piano keyboard note
-----------------|--------------------
Up    | C3
Right | D3
Down  | E3
Left  | F3
W     | G3
A     | A3
S     | B3
D     | C4
F     | D4
G     | E4

The organ notes are one octave higher. (Of course, you can change the code to generate any notes you want.)

The code uses the `evdev` library to read the keyboard events.

# Generating Sound Output

There are several ways of generating sounds from Python. The most general is the PyAudio library, but it is rather complex. PyGame is intalled by default in NOOBS, so that library was used.

## Running PyGame Headless

PyGame wants to talk to an X11 server, which was problematic for the Alameda County Fair display. There is a way to avoid GUI output, though: specify a dummy video driver before intializing PyGame.

```python
os.environ["SDL_VIDEODRIVER"] = "dummy"
# Now initialize pygame or pygame.mixer.
```

# License

Except as noted below, all files are copyright 2015 by Mark Rose

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Other Licenses

The `shutdownSwitch.py` program was written by [an Instructables contributor](http://www.instructables.com/member/AndrewH7).
See that file for his licensing information.

Audio files were obtained from http://jetcityorange.com/musical-notes/ and http://www.audiocheck.net/blindtests_abspitch.php. Both sites indicate that the files may be freely used for noncommercial purposes. MP3 files were converted to WAV format using the online converter at http://audio.online-convert.com/convert-to-wav. The files from audiocheck.net were also converted to 16-bit samples using Audacity, as the original 24-bit samples were not playable from PyGame.

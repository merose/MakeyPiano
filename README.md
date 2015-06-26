# MakeyPiano
Code and setup info for a Raspberry Pi and MakeyMakey piano demo, originally for the 2015
Alameda County Fair in Pleasanton, CA. Written for the [RobotGarden](http://www.robotgarden.org/) display.

# The Hardware

* Raspberry Pi 2
* MakeyMakey, powered by USB from Raspberry Pi
* Momentary, push-button switch across pins 39 and 40 (Ground and GPIO21, resp.), to provide shutdown request for safe power-off
* USB battery to power Raspberry Pi

When I get a chance, I'll put photos on the Wiki. I've also added screw-terminal strips to make the MakeyMakey wiring more permanent while still allowing leads to be connected when setting up the display.

# Raspberry Pi Setup

* Install NOOBS using local keyboard layout (EN-US, in my case).
* Enable SSH server in raspi-config.
* Create unique SSH keys: `sudo rm /etc/ssh/ssh_host_* && sudo dpkg-reconfigure openssh-server`
* Set a static IP address to make SSH more convenient. (See http://elinux.org/RPi_Setting_up_a_static_IP_in_Debian.)
* Update packages and install a few more.
```
sudo apt-get update # To update index
sudo apt-get upgrade # To  update modules
sudo apt-get install python-pip python-dev # To get pip
sudo pip install evdev # To be able to read USB keyboard and mouse events
```
* The Pi will generate too much noise, by default, if the audio output amplitude is zero. Turn off audio dithering by editing `/boot/config.txt`:

```
disable_audio_dither=1
```

* Install the piano software. Git is installed by default in NOOBS. Clone the MakeyPiano workspace into the `pi` user home directory:

```
cd ~
git clone https://github.com/merose/MakeyPiano.git
```

* Set up the shutdown switch monitor program. A momentary, pushdown switch is connected between the bottom two pins on the GPIO header, pins 39 and 40. (Other pin pairs are OK, but those are easy to remember.) Pin 40 (GPIO21) will be read using an internal pull-up resistor by the program `shutdownSwitch.py`. When pin 40 goes low, the program will initiate a shutdown via `shutdown -h now`. The `shutdownSwitch.py` program is run at boot time by editing `/etc/rc.local`.

```
python /home/pi/MakePiano/shutdownSwitch.py &
```

* Install the piano software script to run at boot time. Edit `/etc/rc.local` to run the piano startup script at boot:

```
/home/pi/MakePiano/piano &
```

This is the end of the Pi setup.

# Piano Software Details

## Piano Software Inputs

The MakeyMakey emulates a USB keyboard and mouse, returning keyboard events for 11 of its inputs and mouse events for the other 7. The program `piano.py` reads 10 inputs, the four arrow keys on the MakeyMakey board and the keys on one of the two header inputs.

MakeyMakey input | Piano keyboard note
-----------------|--------------------
Up    | C4
Right | D4
Down  | E4
Left  | F4
W     | G4
A     | A4
S     | B4
D     | C5
F     | D5
G     | E5

(Of course, you can change the code to generate any notes you want.)

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

The `shutdownSwitch.py` program was written by [an Instructables contributor](www.instructables.com/member/AndrewH7).
See that file for his licensing information.

Audio files were obtained from http://jetcityorange.com/musical-notes/ and http://www.audiocheck.net/blindtests_abspitch.php. Both sites indicate that the files may be freely used for noncommercial purposes. MP3 files were converted to WAV format using the online converter at http://audio.online-convert.com/convert-to-wav.

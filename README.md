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

1. Install NOOBS using local keyboard layout (EN-US, in my case).
1. Enable SSH server in raspi-config.
1. Set a static IP address to make SSH more convenient. (See http://elinux.org/RPi_Setting_up_a_static_IP_in_Debian.)
1. Update packages and install a few more.
```
sudo apt-get update # To update index
sudo apt-get upgrade # To  update modules
sudo apt-get install python-pip python-dev # To get pip
sudo pip install evdev # To be able to read USB keyboard and mouse events
sudo apt-get install alsa-utils mpg123
```

# Raspberry Pi Soft Shutdown Switch

A momentary, pushdown switch is connected between the bottom two pins on the GPIO header, pins 39 and 40. (Other pin pairs are OK, but those are easy to remember.) Pin 40 (GPIO21) will be read using an internal pull-up resistor by the program `shutdownSwitch.py`. When pin 40 goes low, the program will initiate a shutdown via `shutdown -h now`.

The `shutdownSwitch.py` program is run at boot time by editing `/etc/rc.local`.

# The Piano Software

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

(Of course, you can change the code to generate any notes you want.)

The code uses the `evdev` library to read the keyboard events.

# Generating Sound Output

There are several ways of generating sounds from Python. The most general is the PyAudio library, but it is rather complex. PyGame is intalled by default in NOOBS, so that library was used.

## Running PyGame Headless

PyGame wants to talk to an X11 server, which was problematic for the Alameda County Fair display. There is a way to avoid GUI output, though: specify a dummy video driver before intializing PyGame.

```
os.environ["SDL_VIDEODRIVER"] = "dummy"
*initialize pygame or pygame.mixer*
```

# License

Except for the program `shutdownSwitch.py`, all code is copyright 2015 Mark Rose, and uses the Apache License.

The `shutdownSwitch.py` program was written by [an Instructables contributor](www.instructables.com/member/AndrewH7).
See that file for his licensing information.

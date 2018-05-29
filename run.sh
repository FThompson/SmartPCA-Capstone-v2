#!/bin/bash

amixer scontrols
amixer sset 'PCM' 100%
sudo sh -c 'echo "0" > /sys/class/backlight/soc\:backlight/brightness'
sudo python3 src/device.py
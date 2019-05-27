#!/usr/bin/env python3
# Power/Reset Control of Systems via GPIO
# Copyright (C) 2018, 2019  Barry Van Deerlin
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import RPi.GPIO as GPIO
from time import sleep

#     Raspberry Pi Pinout
#      3V3  (1)  (2) 5V
#    GPIO2  (3)  (4) 5V
#    GPIO3  (5)  (6) GND
#    GPIO4  (7)  (8) GPIO14
#      GND  (9) (10) GPIO15
#   GPIO17 (11) (12) GPIO18
#   GPIO27 (13) (14) GND
#   GPIO22 (15) (16) GPIO23
#      3V3 (17) (18) GPIO24
#   GPIO10 (19) (20) GND
#    GPIO9 (21) (22) GPIO25
#   GPIO11 (23) (24) GPIO8
#      GND (25) (26) GPIO7
#    GPIO0 (27) (28) GPIO1
#    GPIO5 (29) (30) GND
#    GPIO6 (31) (32) GPIO12
#   GPIO13 (33) (34) GND
#   GPIO19 (35) (36) GPIO16
#   GPIO26 (37) (38) GPIO20
#      GND (39) (40) GPIO21


# System Targets List
systems = ["system1", "system2"]
# System Power Pin List
powerpin = [22, 24]
# System Reset Pin List
resetpin = [23, 25]
# All the pins that are used
pins = powerpin + resetpin

def press(pin, seconds):
    GPIO.output(pin, GPIO.HIGH)
    sleep(seconds)
    GPIO.output(pin, GPIO.LOW)

# Setup ArgParser
parser = argparse.ArgumentParser(
    prog='empress',
    description='External Management of Power and RESet Switchs')

parser.add_argument(
    '--target', '-t',
    required=True,
    action='store',
    dest="target",
    help='Target System (required)')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    '--poweron', '-P',
    action='store_true',
    dest="poweron",
    default=False,
    help='Flag indicates Power Toggle Target System')

group.add_argument(
    '--poweroff', '-p',
    action='store_true',
    dest="poweroff",
    default=False,
    help='Flag indicates Power Off  Target System')

group.add_argument(
    '--reset', '-r',
    action='store_true',
    dest="reset",
    default=False,
    help='Flag indicates Reset Target System')

parser.add_argument(
    '--version', '-v',
    action='version',
    version='%(prog)s v0.1 Copyright (C) 2018, 2019 Barry Van Deerlin')

# Parse Args
args = parser.parse_args()

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Set Board Layout
GPIO.setwarnings(False) # Turn Warnings Off
GPIO.setup(pins, GPIO.OUT, initial=GPIO.LOW)  # Mark pins as Output

# Check if target is valid
if args.target.lower() in systems:
    # Get target index
    index = systems.index(args.target.lower())
    # If Poweron Flag Raised
    if args.poweron:
        # Apply power to 'power' pin for 200 Milliseconds
        press(powerpin[index], .2)
    # If Poweroff Flag Raised
    elif args.poweroff:
        # Apply power to 'power' pin for 5 seconds
        press(powerpin[index], 5)
    # If Reset Flag Raised
    elif args.reset:
        # Apply power to 'reset' pin for 200 Milliseconds
        press(resetpin[index], .2)
else:
    print("Target System not recognized. Known Systems listed below")
    print(systems)

# Set GPIO pins to default
GPIO.cleanup(pins)

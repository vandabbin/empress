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

def press(pin, seconds):
    GPIO.output(pin, GPIO.HIGH)
    sleep(seconds)
    GPIO.output(pin, GPIO.LOW)

# System Targets List
systems = ["tornado", "foxhole"]
# System Power Pin List
powerpin = [22, 24]
# System Reset Pin List
resetpin = [23, 25]

# Setup ArgParser
parser = argparse.ArgumentParser(
    prog='empress',
    description='External Management of Power and RESet Switchs'
)
parser.add_argument('-t',
                    '--target',
                    required=True,
                    action='store',
                    dest="target",
                    help='Target System (required)')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-P',
                   '--poweron',
                   action='store_true',
                   dest="poweron",
                   default=False,
                   help='Flag indicates Power Toggle Target System')

group.add_argument('-p',
                   '--poweroff',
                   action='store_true',
                   dest="poweroff",
                   default=False,
                   help='Flag indicates Power Off  Target System')

group.add_argument('-r',
                   '--reset',
                   action='store_true',
                   dest="reset",
                   default=False,
                   help='Flag indicates Reset Target System')

parser.add_argument('-v',
                    '--version',
                    action='version',
                    version='%(prog)s v0.1 Copyright (C) 2018, 2019 Barry Van Deerlin')

# Parse Args
args = parser.parse_args()

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Set Board Layout
GPIO.setwarnings(False) # Turn Warnings Off
GPIO.setup([22, 23, 24, 25], GPIO.OUT, initial=GPIO.LOW)  # Mark Pins 22 - 25 as Output

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

# Set GPIO Pins 22 - 25 to default
GPIO.cleanup([22, 23, 24, 25])

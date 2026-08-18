# ASTRA — dial firmware, boot stage (Raspberry Pi Pico / CircuitPython)
#
# Runs once, before code.py, before USB comes up. Two jobs:
#
#   1. The board must present itself as a KEYBOARD AND NOTHING ELSE.
#      If the CIRCUITPY drive mounts, the appliance Mac opens a Finder
#      window at login — over a 1950s television. That is the end of the
#      illusion, and launchd cannot undo it.
#   2. Leave a way back in. Ground GP15 while plugging in and the drive
#      and serial console return, so the dial can be retuned without
#      re-flashing.

import board
import digitalio
import storage
import usb_cdc
import usb_hid

MAINTENANCE_PIN = board.GP15  # tie to GND at plug-in for the drive + REPL

_jumper = digitalio.DigitalInOut(MAINTENANCE_PIN)
_jumper.direction = digitalio.Direction.INPUT
_jumper.pull = digitalio.Pull.UP
maintenance = not _jumper.value  # pulled low = maintenance mode
_jumper.deinit()

# Keyboard only. No mouse, no consumer control — the page reads digits and
# nothing else, and a stray consumer-control report can wake or mute the Mac.
usb_hid.enable((usb_hid.Device.KEYBOARD,))

if not maintenance:
    storage.disable_usb_drive()
    usb_cdc.disable()

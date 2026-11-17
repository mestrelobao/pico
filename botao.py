
import time
import board
import digitalio
import usb_midi
import adafruit_midi

from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

# MIDI output over USB
midi = adafruit_midi.MIDI(
    midi_out=usb_midi.ports[1],
    out_channel=0
)

# Button connected between GP14 and GND
button = digitalio.DigitalInOut(board.GP14)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

NOTE = 24       # C1 in many MIDI numbering conventions
VELOCITY = 127

last_pressed = False

while True:
    pressed = not button.value

    # Button was just pressed
    if pressed and not last_pressed:
        midi.send(NoteOn(NOTE, VELOCITY))

    # Button was just released
    elif not pressed and last_pressed:
        midi.send(NoteOff(NOTE, 0))

    last_pressed = pressed
    time.sleep(0.001)

# -*- coding: UTF-8 -*-
"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""
import sys
import time
import grailkit.midi as midi
from grailkit.midi.constants import NOTE_ON, CONTROL_CHANGE


def main():
    """Test some midi"""

    launch_control_xl_port = None

    print("Available ports:")

    for index, name in enumerate(midi.MidiIn.ports()):
        print(" - %s" % name)

        if name == 'Launch Control XL':
            launch_control_xl_port = index

    if not launch_control_xl_port:
        print("Port not found")
        return False

    port_in = midi.MidiIn(launch_control_xl_port)
    port_in.ignore_types(False, False, False)
    port_out = midi.MidiOut(launch_control_xl_port)

    channels = [0]*8
    matrix = [0, 1, 0, 0, 2, 0, 0, 0,
              0, 1, 0, 0, 2, 0, 0, 0,
              0, 1, 0, 0, 2, 0, 0, 0]
    interrupt = True

    # for note in [41, 42, 43, 44, 57, 58, 59, 60,
    #             73, 74, 75, 76, 89, 90, 91, 92]:
    #    port_out.send([NOTE_ON, note, 127])

    # port_out.send([176, 0, 127])

    def callback(data):
        """Midi message received"""

        cc, note, velocity, *_rest = data

        for key, value in enumerate(range(77, 85)):
            if cc == CONTROL_CHANGE and value == note:
                channels[key] = velocity

        for key, value in enumerate([41, 42, 43, 44, 57, 58, 59, 60]):
            port_out.send([NOTE_ON, value, channels[key]])

        print(data)

        if note:
            port_out.send([cc, note, velocity])

        # exit on 'device' button press
        if cc == NOTE_ON and note == 105:
            sys.exit()

    port_in.received.connect(callback)

    while interrupt:

        for i, n in enumerate(matrix):
            matrix[i] = n + 1 if n < 2 else 0
            c = [2, 16, 18][matrix[i]]
            port_out.send([240, 0, 32, 41, 2, 17, 120, 0, i, c, 247])

        time.sleep(0.5)


def test_callback():

    launch_control_xl_port = 0

    for index, name in enumerate(midi.MidiIn.ports()):
        if name == 'Launch Control XL':
            launch_control_xl_port = index

    if launch_control_xl_port == 0:
        print("Launch Control XL not found")

    port_in = midi.MidiIn(launch_control_xl_port)
    port_in.received.connect(print)

    while True:
        time.sleep(0.1)

if __name__ == '__main__':
    main()

# -*- coding: UTF-8 -*-
"""
    grailkit.midi
    ~~~~~~~~~~~~~

    MIDI library

    RtMidi easier to install via pip
    https://pypi.python.org/pypi/python-rtmidi
    http://www.pygame.org/docs/ref/midi.html
"""
import time
import rtmidi


class MIDIError(Exception):
    """Base exception class for MIDI exceptions"""

    pass


class MIDIInput(object):

    def __int__(self, device_id, buffer_size=4096):
        pass

    def close(self):
        pass

    def poll(self):
        pass

    def read(self):
        pass


class MIDIOutput(object):

    def __int__(self, device_id, latency=0, buffer_size=4096):
        pass

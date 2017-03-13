# -*- coding: UTF-8 -*-
"""
    grailkit.midi
    ~~~~~~~~~~~~~

    MIDI library based on python-rtmidi library but with better interface

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
import rtmidi

from grailkit.core import Signal


NOTE_OFF = 0x80
NOTE_ON = 0x90
POLYPHONIC_PRESSURE = POLY_PRESSURE = 0xA0
CONTROLLER_CHANGE = CONTROL_CHANGE = 0xB0
PROGRAM_CHANGE = 0xC0
CHANNEL_PRESSURE = MONO_PRESSURE = 0xD0
PITCH_BEND = 0xE0
BANK_SELECT = BANK_SELECT_MSB = 0x00
MODULATION_WHEEL = MODULATION_WHEEL_MSB = 0x01
BREATH_CONTROLLER = BREATH_CONTROLLER_MSB = 0x02
FOOT_CONTROLLER = FOOT_CONTROLLER_MSB = 0x04
PORTAMENTO_TIME = PORTAMENTO_TIME_MSB = 0x05
DATA_ENTRY = DATA_ENTRY_MSB = 0x06
CHANNEL_VOLUME = CHANNEL_VOLUME_MSB = 0x07
BALANCE = BALANCE_MSB = 0x08
PAN = PAN_MSB = 0x0A
EXPRESSION_CONTROLLER = EXPRESSION_CONTROLLER_MSB = 0x0B
EFFECT_CONTROL_1 = EFFECT_CONTROL_1_MSB = 0x0C
EFFECT_CONTROL_2 = EFFECT_CONTROL_2_MSB = 0x0D
GENERAL_PURPOSE_CONTROLLER_1 = GENERAL_PURPOSE_CONTROLLER_1_MSB = 0x10
GENERAL_PURPOSE_CONTROLLER_2 = GENERAL_PURPOSE_CONTROLLER_2_MSB = 0x11
GENERAL_PURPOSE_CONTROLLER_3 = GENERAL_PURPOSE_CONTROLLER_3_MSB = 0x12
GENERAL_PURPOSE_CONTROLLER_4 = GENERAL_PURPOSE_CONTROLLER_4_MSB = 0x13

# High resolution continuous controllers (LSB)
BANK_SELECT_LSB = 0x20
MODULATION_WHEEL_LSB = 0x21
BREATH_CONTROLLER_LSB = 0x22
FOOT_CONTROLLER_LSB = 0x24
PORTAMENTO_TIME_LSB = 0x25
DATA_ENTRY_LSB = 0x26
CHANNEL_VOLUME_LSB = 0x27
BALANCE_LSB = 0x28
PAN_LSB = 0x2A
EXPRESSION_CONTROLLER_LSB = 0x2B
EFFECT_CONTROL_1_LSB = 0x2C
EFFECT_CONTROL_2_LSB = 0x2D
GENERAL_PURPOSE_CONTROLLER_1_LSB = 0x30
GENERAL_PURPOSE_CONTROLLER_2_LSB = 0x31
GENERAL_PURPOSE_CONTROLLER_3_LSB = 0x32
GENERAL_PURPOSE_CONTROLLER_4_LSB = 0x33

# Switches
SUSTAIN = SUSTAIN_ONOFF = 0x40
PORTAMENTO = PORTAMENTO_ONOFF = 0x41
SOSTENUTO = SOSTENUTO_ONOFF = 0x42
SOFT_PEDAL = SOFT_PEDAL_ONOFF = 0x43
LEGATO = LEGATO_ONOFF = 0x44
HOLD_2 = HOLD_2_ONOFF = 0x45

# Low resolution continuous controllers
SOUND_CONTROLLER_1 = 0x46
SOUND_CONTROLLER_2 = 0x47
SOUND_CONTROLLER_3 = 0x48
SOUND_CONTROLLER_4 = 0x49
SOUND_CONTROLLER_5 = 0x4A
SOUND_CONTROLLER_6 = 0x4B
SOUND_CONTROLLER_7 = 0x4C
SOUND_CONTROLLER_8 = 0x4D
SOUND_CONTROLLER_9 = 0x4E
SOUND_CONTROLLER_10 = 0x4F
GENERAL_PURPOSE_CONTROLLER_5 = 0x50
GENERAL_PURPOSE_CONTROLLER_6 = 0x51
GENERAL_PURPOSE_CONTROLLER_7 = 0x52
GENERAL_PURPOSE_CONTROLLER_8 = 0x53
PORTAMENTO_CONTROL = PTC = 0x54
HIGH_RESOLUTION_VELOCITY_PREFIX = 0x58
EFFECTS_1 = EFFECTS_1_DEPTH = 0x5B
EFFECTS_2 = EFFECTS_2_DEPTH = 0x5C
EFFECTS_3 = EFFECTS_3_DEPTH = 0x5D
EFFECTS_4 = EFFECTS_4_DEPTH = 0x5E
EFFECTS_5 = EFFECTS_5_DEPTH = 0x5F
DATA_INCREMENT = 0x60
DATA_DECREMENT = 0x61
NRPN_LSB = NON_REGISTERED_PARAMETER_NUMBER_LSB = 0x62
NRPN_MSB = NON_REGISTERED_PARAMETER_NUMBER_MSB = 0x63
RPN_LSB = REGISTERED_PARAMETER_NUMBER_LSB = 0x64
RPN_MSB = REGISTERED_PARAMETER_NUMBER_MSB = 0x65

# Channel Mode messages
ALL_SOUND_OFF = 0x78
RESET_ALL_CONTROLLERS = 0x79
LOCAL_CONTROL = LOCAL_CONTROL_ONOFF = 0x7A
ALL_NOTES_OFF = 0x7B
OMNI_MODE_OFF = 0x7C
OMNI_MODE_ON = 0x7D
MONO_MODE_ON = 0x7E
POLY_MODE_ON = 0x7F

# System Common Messages, for all channels
SYSTEM_EXCLUSIVE = 0xF0
MIDI_TIME_CODE = MTC = 0xF1
SONG_POSITION_POINTER = 0xF2
SONG_SELECT = 0xF3
TUNING_REQUEST = TUNE_REQUEST = 0xF6
END_OF_EXCLUSIVE = 0xF7

# Midifile meta-events
SEQUENCE_NUMBER = 0x00  # 00 02 ss ss (seq-number)
TEXT = 0x01             # 01 len text...
COPYRIGHT = 0x02        # 02 len text...
SEQUENCE_NAME = 0x03    # 03 len text...
INSTRUMENT_NAME = 0x04  # 04 len text...
LYRIC = 0x05            # 05 len text...
MARKER = 0x06           # 06 len text...
CUEPOINT = 0x07         # 07 len text...
PROGRAM_NAME = 0x08     # 08 len text...
DEVICE_NAME = 0x09      # 09 len text...

MIDI_CH_PREFIX = 0x20   # MIDI channel prefix assignment (deprecated)

MIDI_PORT = 0x21        # 21 01 port, deprecated but still used
END_OF_TRACK = 0x2F     # 2f 00
TEMPO = 0x51            # 51 03 tt tt tt (tempo in µs/quarternote)
SMTP_OFFSET = 0x54      # 54 05 hh mm ss ff xx
TIME_SIGNATURE = 0x58   # 58 04 nn dd cc bb
KEY_SIGNATURE = 0x59    # 59 02 sf mi (sf = number of sharps(+) or flats(-)
SPECIFIC = 0x7F         # Sequencer specific event
TIMING_CLOCK = 0xF8
SONG_START = 0xFA
SONG_CONTINUE = 0xFB
SONG_STOP = 0xFC
ACTIVE_SENSING = 0xFE
SYSTEM_RESET = 0xFF
META_EVENT = 0xFF
ESCAPE_SEQUENCE = 0xF7

# Misc constants
FILE_HEADER = 'MThd'
TRACK_HEADER = 'MTrk'

# Timecode resolution: frames per second
FPS_24 = 0xE8
FPS_25 = 0xE7
FPS_29 = 0xE3
FPS_30 = 0xE2


def is_status(byte):
    """Return True if the given byte is a MIDI status byte, False otherwise."""

    return (byte & 0x80) == 0x80


def _available(_type='in'):
    """Returns list of available input or output ports"""

    dev = rtmidi.MidiIn() if _type == 'in' else rtmidi.MidiOut()
    ports = dev.get_ports()
    del dev

    return ports


def input_ports():
    """Returns list of all available input ports"""

    return _available(_type='in')


def output_ports():
    """Returns list of all available output ports"""

    return _available(_type='out')


class MidiError(Exception):
    """Base exception class for MIDI exceptions"""

    pass


class MidiIn(object):
    """Input device"""

    def __init__(self, port=0, name=None, virtual=False):
        """Open a Midi Input port"""

        self._dev = rtmidi.MidiIn()

        if virtual:
            self._dev.open_virtual_port(name)
        else:
            self._dev.open_port(port, name)

        # signals
        self.received = Signal(object)

        self._dev.set_callback(self._received)

    def _received(self, message):
        """Trigger signal when message received"""

        self.received.emit(message)

    def close(self):
        """Close device"""

        self._dev.close_port()

    def poll(self):
        """Poll for MIDI input.

        Checks whether a MIDI event is available in the input buffer and returns a two-element tuple with
        the MIDI message and a delta time. The MIDI message is a list of integers representing the data bytes of
        the message, the delta time is a float representing the time in seconds elapsed since the reception
        of the previous MIDI event.

        The function does not block. When no MIDI message is available, it returns None.
        """

        return self._dev.get_message()

    def ignore_types(self, sysex=True, timing=True, active_sense=True):
        """Enable/Disable input filtering of certain types of MIDI events.

        By default System Exclusive (aka sysex), MIDI Clock and Active Sensing messages are filtered from the MIDI
        input and never reach your code, because they can fill up input buffers very quickly.

        To receive them, you can selectively disable the filtering of these event types.

        To enable reception - i.e. turn off the default filtering - of sysex messages, pass sysex = False.

        To enable reception of MIDI Clock, pass timing = False.

        To enable reception of Active Sensing, pass active_sensing = False.

        These arguments can of course be combined in one call, and they all default to True.

        If you enable reception of any of these event types, be sure to either use an input callback function,
        which returns quickly or poll for MIDI input often. Otherwise you might lose MIDI
        input because the input buffer overflows.

        Windows note: the Windows Multi Media API uses fixed size buffers for the reception of sysex messages,
        whose number and size is set at compile time. Sysex messages longer than the buffer size can not
        be received properly when using the Windows Multi Media API.

        The default distribution of python-rtmidi sets the number of sysex buffers to four and the size of
        each to 8192 bytes. To change these values, edit the RT_SYSEX_BUFFER_COUNT and RT_SYSEX_BUFFER_SIZE preprocessor
        defines in RtMidi.cpp and recompile.
        """

        self._dev.ignore_types(self, sysex=sysex, timing=timing, active_sense=active_sense)

    @classmethod
    def open(cls, port=0, name=None):
        """Open the MIDI input or output port with the given port number.

        Only one port can be opened per MidiIn or MidiOut instance.
        An RtMidiError exception is raised if an attempt is made to open a port on a MidiIn or MidiOut instance,
        which already opened a (virtual) port.

        You can optionally pass a name for the RtMidi port with the name keyword or the second positional argument.
        Names with non-ASCII characters in them have to be passed as unicode or utf-8 encoded strings in Python 2.
        The default name is “RtMidi input” resp. “RtMidi output”.

        Note Closing a port and opening it again with a different name does not change the port name.
        To change the port name, delete its instance, create a new one and open the port again giving a different name.

        Raises:
            RtMidiError: Raised when trying to open a MIDI port when a
                         (virtual) port has already been opened by this instance.
        """

        return MidiIn(port=port, name=name, virtual=False)

    @classmethod
    def open_virtual(cls, name=None):
        """Open a virtual MIDI input or output port.

        Only one port can be opened per MidiIn or MidiOut instance. An RtMidiError exception is raised if an attempt
        is made to open a port on a MidiIn or MidiOut instance, which already opened a (virtual) port.

        A virtual port is not connected to a physical MIDI device or system port when first opened. You can connect it
        to another MIDI output with the OS-dependent tools provided by the low-level MIDI framework, e.g. a connect for
        ALSA, jack_connect for JACK, or the Audio & MIDI settings dialog for CoreMIDI.

        Note Virtual ports are not supported by some backend APIs, namely the Windows MultiMedia API. You can use
        special MIDI drivers like MIDI Yoke or loopMIDI to provide hardware-independent virtual MIDI ports as an
        alternative. You can optionally pass a name for the RtMidi port with the name keyword or the second positional
        argument. Names with non-ASCII characters in them have to be passed as unicode or utf-8 encoded strings
        in Python 2. The default name is “RtMidi virtual input” resp. “RtMidi virtual output”.

        Note Closing a port and opening it again with a different name does not change the port name.
        To change the port name, delete its instance, create a new one and open the port again giving a different name.
        Also, to close a virtual input port, you have to delete its MidiIn or MidiOut instance.

        Raises:
            NotImplementedError: Raised when trying to open a virtual MIDI port with the Windows MultiMedia API,
                                 which does not support virtual ports.
            RtMidiError: Raised when trying to open a virtual port when a
                         (virtual) port has already been opened by this instance.
        """

        return MidiIn(name=name, virtual=True)

    @classmethod
    def ports(cls):
        """Return a list of names of available MIDI input ports.
        The list index of each port name corresponds to its port number.
        """

        dev = rtmidi.MidiIn()
        ports = dev.get_ports(encoding='auto')
        del dev

        return ports

    @classmethod
    def ports_count(cls):
        """Return the number of available MIDI input ports."""

        dev = rtmidi.MidiIn()
        count = dev.get_port_count()
        del dev

        return count

    @classmethod
    def port_name(cls, port):
        """Return the name of the MIDI input port with given number.

        Ports are numbered from zero, separately for input and output ports.
        The number of available ports is returned by the `ports_count` method.
        """

        dev = rtmidi.MidiIn()
        name = dev.get_port_name(port, encoding='auto')
        del dev

        return name


class MidiOut(object):
    """Output device"""

    def __init__(self, port=0, name=None, virtual=False):
        """Open midi output device"""

        if virtual:
            self._dev = rtmidi.MidiOut(name=name)
        else:
            self._dev = rtmidi.MidiOut(port=port, name=name)

    def send(self, data):
        """Send a MIDI message to the output port.

        The message must be passed as an iterable of integers, each element representing one byte of the MIDI message.
        Normal MIDI messages have a length of one to three bytes, but you can also send system exclusive messages,
        which can be arbitrarily long, via this method.

        No check is made whether the passed data constitutes a valid MIDI message.
        """

        self._dev.send_message(data)

    def close(self):
        """Close output port"""

        self._dev.close_port()

    @classmethod
    def open(cls, port=0, name=None):
        """Open the MIDI input or output port with the given port number.

        Only one port can be opened per MidiIn or MidiOut instance.
        An RtMidiError exception is raised if an attempt is made to open a port on a MidiIn or MidiOut instance,
        which already opened a (virtual) port.

        You can optionally pass a name for the RtMidi port with the name keyword or the second positional argument.
        Names with non-ASCII characters in them have to be passed as unicode or utf-8 encoded strings in Python 2.
        The default name is “RtMidi input” resp. “RtMidi output”.

        Note Closing a port and opening it again with a different name does not change the port name.
        To change the port name, delete its instance, create a new one and open the port again giving a different name.

        Raises:
            RtMidiError: Raised when trying to open a MIDI port when a
                         (virtual) port has already been opened by this instance.
        """

        return MidiOut(port=port, name=name, virtual=False)

    @classmethod
    def open_virtual(cls, name=None):
        """Open a virtual MIDI input or output port.

        Only one port can be opened per MidiIn or MidiOut instance. An RtMidiError exception is raised if an attempt
        is made to open a port on a MidiIn or MidiOut instance, which already opened a (virtual) port.

        A virtual port is not connected to a physical MIDI device or system port when first opened. You can connect it
        to another MIDI output with the OS-dependent tools provided by the low-level MIDI framework, e.g. a connect for
        ALSA, jack_connect for JACK, or the Audio & MIDI settings dialog for CoreMIDI.

        Note Virtual ports are not supported by some backend APIs, namely the Windows MultiMedia API. You can use
        special MIDI drivers like MIDI Yoke or loopMIDI to provide hardware-independent virtual MIDI ports as an
        alternative. You can optionally pass a name for the RtMidi port with the name keyword or the second positional
        argument. Names with non-ASCII characters in them have to be passed as unicode or utf-8 encoded strings
        in Python 2. The default name is “RtMidi virtual input” resp. “RtMidi virtual output”.

        Note Closing a port and opening it again with a different name does not change the port name.
        To change the port name, delete its instance, create a new one and open the port again giving a different name.
        Also, to close a virtual input port, you have to delete its MidiIn or MidiOut instance.

        Raises:
            NotImplementedError: Raised when trying to open a virtual MIDI port with the Windows MultiMedia API,
                                 which does not support virtual ports.
            RtMidiError: Raised when trying to open a virtual port when a
                         (virtual) port has already been opened by this instance.
        """

        return MidiOut(name=name, virtual=True)

    @classmethod
    def ports(cls):
        """Return a list of names of available MIDI output ports.
        The list index of each port name corresponds to its port number.
        """

        dev = rtmidi.MidiOut()
        ports = dev.get_ports(encoding='auto')
        del dev

        return ports

    @classmethod
    def ports_count(cls):
        """Return the number of available MIDI output ports."""

        dev = rtmidi.MidiOut()
        count = dev.get_port_count()
        del dev

        return count

    @classmethod
    def port_name(cls, port):
        """Return the name of the MIDI output port with given number.

        Ports are numbered from zero, separately for input and output ports.
        The number of available ports is returned by the `ports_count` method.
        """

        dev = rtmidi.MidiOut()
        name = dev.get_port_name(port, encoding='auto')
        del dev

        return name

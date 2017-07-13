# -*- coding: UTF-8 -*-
"""
    grailkit.midi
    ~~~~~~~~~~~~~

    MIDI I/O library based on rtmidi (python-rtmidi),
    but with simple and better interface

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
import rtmidi

from grailkit.core import Signal


class MidiError(Exception):
    """Base exception class for MIDI exceptions"""

    pass


class MidiMessage(list):
    """Representation of midi message data"""

    def __init__(self, _list, _delta):
        super(MidiMessage, self).__init__(_list)

        self._time = _delta

    @property
    def time_delta(self):
        """Returns delta time in seconds between this and previous message"""

        return self._time


class MidiIn(object):
    """Input device"""

    def __init__(self, port=0, name=None, virtual=False):
        """Open a Midi Input port"""

        self._dev = rtmidi.MidiIn()

        try:
            if virtual:
                self._dev.open_virtual_port(name)
            else:
                self._dev.open_port(port, name)
        except TypeError:
            raise MidiError("Unable to open%s port '%s' with name '%s'. "
                            "Port number is invalid" % (" virtual" if virtual else "", port, name))
        except rtmidi.RtMidiError as error:
            raise MidiError(error)

        # signals
        self.received = Signal(object)
        self.error = Signal(int, str)

        self._dev.set_callback(self._received, None)
        self._dev.set_error_callback(self._error, None)

    def _received(self, message, user_data=None):
        """Trigger signal when message received"""

        self.received.emit(MidiMessage(message[0], message[1]))

    def _error(self, error_type, error_message, user_data=None):
        """Error callback"""

        self.error.emit(error_type, error_message)

    def close(self):
        """Close device"""

        self._dev.close_port()

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

        self._dev.ignore_types(sysex=sysex, timing=timing, active_sense=active_sense)

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
            MidiError: Raised when trying to open a MIDI port when a
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
            MidiError: Raised when trying to open a virtual port when a
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

        self._dev = rtmidi.MidiOut()

        if virtual:
            self._dev.open_virtual_port(name)
        else:
            self._dev.open_port(port, name)

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
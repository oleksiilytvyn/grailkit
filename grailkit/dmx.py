# -*- coding: UTF-8 -*-
"""
    grailkit.dmx
    ~~~~~~~~~~~~

    Send DMX signal over Serial Port USB interfaces
    Caution this module is experimental

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
import sys
import glob
import serial
import threading
from grailkit.core import Signal


def serial_ports():
    """Lists serial port names

    Returns
        A list of the serial ports available on the system
    Raises
        EnvironmentError on unsupported or unknown platforms
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(255)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []

    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()

            result.append(port)
        except (OSError, serial.SerialException):
            pass

    return result


class DMXFrame(object):
    """Representation of DMX channels"""

    _bytes = []

    def __init__(self, frame=None):
        """Create DMX data frame

        Args:
            frame (list): DMX channel values
        """
        super(DMXFrame, self).__init__()

        if frame and len(frame) > 0:
            for value in frame:
                self._bytes.append(int(value))

            self._bytes += [0] * (512 - len(frame))
        else:
            self._bytes = [0] * 512

    def __getitem__(self, key):
        """Get channel value by index

        Args:
            key (int): channel index
        Raises:
            IndexError if index is out of range"""

        if key < 0 or key > 511:
            raise IndexError("Index out of range. Index must be from 0 to 511 as DMX512 have 512 channels.")

        return self._bytes[key]

    def __setitem__(self, key, value):
        """Set channel value

        Args:
            key (int): channel index
            value (int): channel value
        Raises:
            ValueError if given wrong value
            IndexError if index is out of range
        """

        if key < 0 or key > 511:
            raise IndexError("Index out of range. Index must be from 0 to 511 as DMX512 have 512 channels.")

        if not isinstance(value, int) or (value > 255 or value < 0):
            raise ValueError("Given value is not int or out of range")

        self._bytes[key] = value

    def __delitem__(self, key):
        """Set channel value to 0

        Args:
            key (int): channel index
        Raises:
            IndexError if index is out of range
        """

        if key < 0 or key > 511:
            raise IndexError("Index out of range. Index must be from 0 to 511 as DMX512 have 512 channels.")

        self._bytes[key] = 0

    def __missing__(self, key):
        """Raise exception on missing key

        Args:
            key (int): channel index
        """

        raise AttributeError("There is no DMX channel with this index.")

    def __str__(self):
        """Returns string representation"""

        return str(bytes(self._bytes))

    def __bytes__(self):
        """Returns bytes representation"""

        return bytes(self._bytes)


class DMXDevice(object):
    """DMX device using RS245 protocol"""

    MODE_RX = 0
    MODE_TX = 1

    # setup the dmx
    # char 126 is 7E in hex. It's used to start all DMX512 commands
    _DMX_OPEN = b'\x7e'
    # char 231 is E7 in hex. It's used to close all DMX512 commands
    _DMX_CLOSE = b'\xe7'
    # packet label
    _DMX_LABEL = b'\x06\x01\x02'
    # this code seems to initialize the communications.
    _DMX_INIT1 = b'\x03\x02\x00\x00\x00'
    _DMX_INIT2 = b'\n\x02\x00\x00\x00'

    receive = Signal(DMXFrame)

    def __init__(self, port, mode=MODE_TX):
        """Create DMX device

        Args:
            port (str): serial port name
            mode: transmit or receive
        """

        self._stream = serial.Serial(port)
        self._thread = None
        self._buffer = ''

        if mode is self.MODE_TX:
            # this writes the initialization codes to the DMX
            self._stream.write(self._DMX_OPEN + self._DMX_INIT1 + self._DMX_CLOSE)
            self._stream.write(self._DMX_OPEN + self._DMX_INIT2 + self._DMX_CLOSE)

        if mode is self.MODE_RX:
            # start thread to constantly read data
            self._thread = threading.Thread(target=self._receive, args=(self._stream,))
            self._thread.start()

    def send(self, frame):
        """Send channel information to device

        Args:
            frame (DMXFrame): list of int representing DMX channels
        """

        self._stream.send(self._DMX_OPEN + self._DMX_LABEL + bytes(frame) + self._DMX_CLOSE)

    def _receive(self):
        """Receive DMX frame data"""

        self._buffer += self._stream.read()

        start_index = self._buffer.find(str(self._DMX_OPEN))
        end_index = self._buffer.find(str(self._DMX_CLOSE))

        if start_index > -1 and end_index > -1:
            buffer = self._buffer[start_index:end_index]
            self._buffer = self._buffer[end_index:]

            self.receive.emit(DMXFrame(buffer))

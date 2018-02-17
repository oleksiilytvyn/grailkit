# -*- coding: UTF-8 -*-
"""
    grailkit.dmx
    ~~~~~~~~~~~~

    Send DMX signal over Serial Port USB interfaces

    CAUTION! This module is highly unstable and incomplete

    :copyright: (c) 2018 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import sys
import glob
# serial package named pyserial in pip, ignore this inspection
# noinspection PyPackageRequirements
import serial
import threading

from grailkit.core import Signal

# todo: check this modules


def dmx_serial_ports():
    """Lists serial port names

    Returns:
        List of the serial ports available on the system
    Raises:
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


class DMXError(Exception):
    """Base class for dmx module exceptions"""

    pass


class DMXUniverse(object):
    """Representation of DMX channels"""

    def __init__(self, frame=None, universe=0):
        """Create DMX data frame

        Args:
            frame (list, set, tuple, None): DMX channel values
            universe (int): DMX universe number
        """
        super(DMXUniverse, self).__init__()

        self._length = 512
        self._bytes = self._bytes = [0] * self._length
        self._universe = universe

        if frame and len(frame) > 0:
            for index, value in enumerate(frame):
                self._bytes[index] = int(value)

    def __len__(self):
        """Returns number of channels in this DMX universe"""

        return self._length

    def __getitem__(self, key):
        """Get channel value by index

        Args:
            key (int): channel index
        Raises:
            IndexError if index is out of range
        Returns:
            int: value of DMX channel
        """

        if key < 0 or key >= self._length:
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

        if key < 0 or key >= self._length:
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

        if key < 0 or key >= self._length:
            raise IndexError("Index out of range. Index must be from 0 to 511 as DMX512 have 512 channels.")

        self._bytes[key] = 0

    def __missing__(self, key):
        """Raise exception on missing key

        Args:
            key (int): channel index
        Raises:
            AttributeError: always rises exception
        """

        raise AttributeError("There is no DMX channel with index %d" % key)

    def __str__(self):
        """Returns string representation"""

        return str(bytes(self._bytes))

    def __bytes__(self):
        """Returns bytes representation"""

        return bytes(self._bytes)

    @property
    def universe(self):
        """Returns universe number"""

        return self._universe


class DMXDevice(object):
    """DMX device using RS245 protocol"""

    MODE_RX = 0
    MODE_TX = 1

    # dmx packet labels
    LABEL = {
        'REPROGRAM_FIRMWARE_RQ': 1,
        'PROGRAM_FLASH_PAGE_RQ': 2,
        'PROGRAM_FLASH_PAGE_REPLY': 2,

        'GET_WIDGET_PARAMS_RQ': 3,
        'GET_WIDGET_PARAMS_REPLY': 3,
        'SET_WIDGET_PARAMS_RQ': 4,

        'SET_DMX_RX_MODE': 5,
        'SET_DMX_TX_MODE': 6,
        'SEND_DMX_RDM_TX': 7,
        'RECEIVE_DMX_ON_CHANGE': 8,
        'RECEIVED_DMX_COS_TYPE': 9,
        'GET_WIDGET_SN_RQ': 10,
        'GET_WIDGET_SN_REPLY': 10,
        'SEND_RDM_DISCOVERY_RQ': 11
        }

    # DMX packet start and end codes
    _DMX_OPEN = b'\x7E'
    _DMX_CLOSE = b'\xE7'

    # packet label
    _DMX_LABEL = b'\x06'

    # this code seems to initialize the communications.
    _DMX_INIT1 = b'\x03\x02\x00\x00\x00'
    _DMX_INIT2 = b'\x0A\x02\x00\x00\x00'

    def __init__(self, port, mode=MODE_TX):
        """Create DMX device

        Args:
            port (str): serial port name
            mode (int): transmit or receive
        """

        self.receive = Signal(DMXUniverse)

        self._stream = serial.Serial(port, baudrate=57600, timeout=1, stopbits=serial.STOPBITS_TWO)
        self._stream.reset_output_buffer()
        self._stream.reset_input_buffer()

        self._thread = None
        self._buffer = ''

        if mode == self.MODE_TX:
            # this writes the initialization codes to the DMX
            self._stream.write(self._DMX_OPEN + self._DMX_INIT1 + self._DMX_CLOSE)
            self._stream.write(self._DMX_OPEN + self._DMX_INIT2 + self._DMX_CLOSE)

        elif mode == self.MODE_RX:
            # start thread to constantly read data
            self._thread = threading.Thread(target=self._receive, args=(self._stream,))
            self._thread.start()

    def send(self, frame):
        """Send channel information to device

        Args:
            frame (DMXUniverse): list of int representing DMX channels
        """

        data = bytearray()
        data.extend(self._DMX_OPEN)
        data.extend(self._DMX_LABEL)
        data.append(len(frame) & 0xFF)
        data.append(len(frame) >> 8)
        data.extend(bytes(frame))
        data.extend(self._DMX_CLOSE)

        self._stream.write(data)

    def close(self):
        """Close serial port connection"""

        self._stream.close()

    def _receive(self):
        """Receive DMX frame data"""

        self._buffer += self._stream.read()

        start_index = self._buffer.find(str(self._DMX_OPEN))
        end_index = self._buffer.find(str(self._DMX_CLOSE))

        if start_index > -1 and end_index > -1:
            buffer = self._buffer[start_index:end_index]
            self._buffer = self._buffer[end_index:]

            self.receive.emit(DMXUniverse(buffer))

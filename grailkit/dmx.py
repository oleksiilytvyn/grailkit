# -*- coding: UTF-8 -*-
"""
    grailkit.dmx
    ~~~~~~~~~~~~

    Send DMX signal over Serial Port USB interfaces
    This module is experimental
"""
import sys
import glob
import serial


def serial_ports():
    """Lists serial port names

        Returns
            A list of the serial ports available on the system
        Raises
            EnvironmentError on unsupported or unknown platforms
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
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


class Device:

    MODE_RX = 0
    MODE_TX = 1

    # setup the dmx
    # char 126 is 7E in hex. It's used to start all DMX512 commands
    _DMX_OPEN = chr(126)

    # char 231 is E7 in hex. It's used to close all DMX512 commands
    _DMX_CLOSE = chr(231)

    # packet label
    _DMX_LABEL = chr(6) + chr(1) + chr(2)

    # this code seems to initialize the communications.
    _DMX_INIT1 = chr(3) + chr(2) + chr(0) + chr(0) + chr(0)
    _DMX_INIT2 = chr(10) + chr(2) + chr(0) + chr(0) + chr(0)

    def __init__(self, port, mode=MODE_TX):

        self._stream = serial.Serial(port)

        if mode is Device.MODE_TX:
            # this writes the initialization codes to the DMX
            self._stream.write(Device._DMX_OPEN + Device._DMX_INIT1 + Device._DMX_CLOSE)
            self._stream.write(Device._DMX_OPEN + Device._DMX_INIT2 + Device._DMX_CLOSE)

    def send(self, frame):
        """Send channel information to device

        Args:
            frame (list): list of int representing DMX channels
        """

        self._stream.send(Device._DMX_OPEN + Device._DMX_LABEL + ''.join(frame) + Device._DMX_CLOSE)

    def receive(self, frame):
        """Receive DMX frame data"""

        self._stream.read()

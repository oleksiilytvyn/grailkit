# -*- coding: UTF-8 -*-
# OSC implementation in pure python
# Copyright (C) 2014-2016 Oleksii Lytvyn
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
    grailkit.osc
    ~~~~~~~~~~~~

    OSC protocol implementation in pure python,
    Code from OSC project (https://bitbucket.org/grailapp/osc)
"""

import time
import struct
import socket
import logging
import decimal
import datetime
import builtins
import calendar
import collections
import socketserver

__version__ = '0.4'
__all__ = [
    'OSCPacket',
    'OSCMessage',
    'OSCBundle',
    'OSCClient',
    'OSCServer',
    'OSCSender',
    'OSCReceiver',
    'OSCForkingServer',
    'OSCThreadingServer',
    'OSCBlockingServer',
    'OSCParseError',
    'OSCBuildError',
    'OSCPacketParseError',
    'OSCMessageParseError',
    'OSCMessageBuildError',
    'OSCBundleParseError',
    'OSCBundleBuildError',
    'NTPError',
    'IMMEDIATELY'
    ]

#
# NTP library
#

NTP_IMMEDIATELY = struct.pack('>q', 1)
_NTP_SYSTEM_EPOCH = datetime.date(*time.gmtime(0)[0:3])
_NTP_EPOCH = datetime.date(1900, 1, 1)
_NTP_DELTA = (_NTP_SYSTEM_EPOCH - _NTP_EPOCH).days * 24 * 3600


class NTPError(Exception):
    """Base class for ntp errors"""


def ntp_to_system_time(date):
    """Convert a NTP time to system time.

    System time is represented by seconds since the epoch in UTC.

    Args:
        date: NTP time to be converted
    Returns:
        system time in seconds
    """

    return date - _NTP_DELTA


def system_time_to_ntp(date):
    """Convert a system time to a NTP time datagram.

    System time is represented by seconds since the epoch in UTC.

    Args:
        date: System time to be converted
    Returns:
        NTP time in seconds
    """
    try:
        ntp = date + _NTP_DELTA
    except TypeError as ve:
        raise NTPError('Invalid date: {}'.format(ve))

    num_secs, fraction = str(ntp).split('.')

    return struct.pack('>I', int(num_secs)) + struct.pack('>I', int(fraction))


class OSCParseError(Exception):
    """Base exception raised when a datagram parsing error occurs."""


class OSCBuildError(Exception):
    """Base exception raised  when a datagram building error occurs."""


IMMEDIATELY = 0
_INT_DGRAM_LEN = 4
_FLOAT_DGRAM_LEN = 4
_DATE_DGRAM_LEN = _INT_DGRAM_LEN * 2
_STRING_DGRAM_PAD = 4
_BLOB_DGRAM_PAD = 4


def write_string(val):
    """Returns the OSC string equivalent of the given python string.

    Args:
        val: string

    Raises:
        OSCBuildError if the string could not be encoded.
    """
    try:
        dgram = val.encode('utf-8')  # Default, but better be explicit.
    except (UnicodeEncodeError, AttributeError) as e:
        raise OSCBuildError('Incorrect string, could not encode {}'.format(e))

    diff = _STRING_DGRAM_PAD - (len(dgram) % _STRING_DGRAM_PAD)
    dgram += (b'\x00' * diff)

    return dgram


def read_string(dgram, start_index):
    """Get a python string from the datagram, starting at pos start_index.

    According to the specifications, a string is:
    "A sequence of non-null ASCII characters followed by a null,
    followed by 0-3 additional null characters to make the total number
    of bits a multiple of 32".

    Args:
        dgram: A datagram packet.
        start_index: An index where the string starts in the datagram.

    Returns:
        A tuple containing the string and the new end index.

    Raises:
        OSCParseError if the datagram could not be parsed.
    """
    offset = 0

    try:
        while dgram[start_index + offset] != 0:
            offset += 1

        if offset == 0:
            raise OSCParseError(
                'OSC string cannot begin with a null byte: %s' % dgram[start_index:])

        if offset % _STRING_DGRAM_PAD == 0:
            offset += _STRING_DGRAM_PAD
        else:
            offset += (-offset % _STRING_DGRAM_PAD)

        if offset > len(dgram[start_index:]):
            raise OSCParseError('Datagram is too short')

        data_str = dgram[start_index:start_index + offset]

        return data_str.replace(b'\x00', b'').decode('utf-8'), start_index + offset
    except IndexError as ie:
        raise OSCParseError('Could not parse datagram %s' % ie)

    except TypeError as te:
        raise OSCParseError('Could not parse datagram %s' % te)


def write_int(val):
    """Returns the datagram for the given integer parameter value

    Args:
        val: value to be converted

    Raises:
        OSCBuildError if the int could not be converted.
    """
    try:
        return struct.pack('>i', val)
    except struct.error as e:
        raise OSCBuildError('Wrong argument value passed: {}'.format(e))


def read_int(dgram, start_index):
    """Get a 32-bit big-endian two's complement integer from the datagram.

    Args:
        dgram: A datagram packet.
        start_index: An index where the integer starts in the datagram.

    Returns:
        A tuple containing the integer and the new end index.

    Raises:
        OSCParseError if the datagram could not be parsed.
    """
    try:
        if len(dgram[start_index:]) < _INT_DGRAM_LEN:
            raise OSCParseError('Datagram is too short')
        return (
            struct.unpack('>i', dgram[start_index:start_index + _INT_DGRAM_LEN])[0], start_index + _INT_DGRAM_LEN)
    except (struct.error, TypeError) as e:
        raise OSCParseError('Could not parse datagram %s' % e)


def write_float(val):
    """Returns the datagram for the given float parameter value

    Args:
        val: float value

    Raises:
        OSCBuildError if the float could not be converted.
    """
    try:
        return struct.pack('>f', val)
    except struct.error as e:
        raise OSCBuildError('Wrong argument value passed: {}'.format(e))


def read_float(dgram, start_index):
    """Get a 32-bit big-endian IEEE 754 floating point number from the datagram.

    Args:
        dgram: A datagram packet.
        start_index: An index where the float starts in the datagram.

    Returns:
        A tuple containing the float and the new end index.

    Raises:
        OSCParseError if the datagram could not be parsed.
    """
    try:
        if len(dgram[start_index:]) < _FLOAT_DGRAM_LEN:
            # Noticed that Reaktor doesn't send the last bunch of \x00 needed to make
            # the float representation complete in some cases, thus we pad here to
            # account for that.
            dgram += b'\x00' * (_FLOAT_DGRAM_LEN - len(dgram[start_index:]))
        return (
            struct.unpack('>f',
                          dgram[start_index:start_index + _FLOAT_DGRAM_LEN])[0],
            start_index + _FLOAT_DGRAM_LEN)
    except (struct.error, TypeError) as e:
        raise OSCParseError('Could not parse datagram %s' % e)


def read_blob(dgram, start_index):
    """ Get a blob from the datagram.

    According to the specifications, a blob is made of
    "an int32 size count, followed by that many 8-bit bytes of arbitrary
    binary data, followed by 0-3 additional zero bytes to make the total
    number of bits a multiple of 32".

    Args:
        dgram: A datagram packet.
        start_index: An index where the float starts in the datagram.

    Returns:
        A tuple containing the blob and the new end index.

    Raises:
        OSCParseError if the datagram could not be parsed.
    """
    size, int_offset = read_int(dgram, start_index)
    # Make the size a multiple of 32 bits.
    total_size = size + (-size % _BLOB_DGRAM_PAD)
    end_index = int_offset + size

    if end_index - start_index > len(dgram[start_index:]):
        raise OSCParseError('Datagram is too short.')

    return dgram[int_offset:int_offset + size], int_offset + total_size


def write_blob(val):
    """Returns the datagram for the given blob parameter value.

    Args:
        val: blob value

    Raises:
        OSCBuildError if the value was empty or if its size didn't fit an OSC int.
    """
    if not val:
        raise OSCBuildError('Blob value cannot be empty')

    dgram = write_int(len(val))
    dgram += val

    while len(dgram) % _BLOB_DGRAM_PAD != 0:
        dgram += b'\x00'

    return dgram


def get_date(dgram, start_index):
    """Get a 64-bit big-endian fixed-point time tag as a date from the datagram.

    According to the specifications, a date is represented as is:
    "the first 32 bits specify the number of seconds since midnight on
    January 1, 1900, and the last 32 bits specify fractional parts of a second
    to a precision of about 200 picoseconds".

    Args:
        dgram: A datagram packet.
        start_index: An index where the date starts in the datagram.

    Returns:
        A tuple containing the system date and the new end index.
        returns IMMEDIATELY (0) if the corresponding OSC sequence was found.

    Raises:
        OSCParseError if the datagram could not be parsed.
    """
    # Check for the special case first.
    if dgram[start_index:start_index + _DATE_DGRAM_LEN] == NTP_IMMEDIATELY:
        return IMMEDIATELY, start_index + _DATE_DGRAM_LEN
    if len(dgram[start_index:]) < _DATE_DGRAM_LEN:
        raise OSCParseError('Datagram is too short')

    num_secs, start_index = read_int(dgram, start_index)
    fraction, start_index = read_int(dgram, start_index)
    # Get a decimal representation from those two values.
    dec = decimal.Decimal(str(num_secs) + '.' + str(fraction))
    # And convert it to float simply.
    system_time = float(dec)

    return ntp_to_system_time(system_time), start_index


def write_date(system_time):
    if system_time == IMMEDIATELY:
        return NTP_IMMEDIATELY

    try:
        return system_time_to_ntp(system_time)
    except NTPError as ntpe:
        raise OSCBuildError(ntpe)


#
# Packet
#

TimedMessage = collections.namedtuple(
    typename='TimedMessage',
    field_names=('time', 'message'))


class OSCPacketParseError(Exception):
    """Base error thrown when a packet could not be parsed."""

    pass

class OSCPacket(object):
    """Unit of transmission of the OSC protocol.

    Any application that sends OSC Packets is an OSC Client.
    Any application that receives OSC Packets is an OSC Server.
    """

    def __init__(self, dgram):
        """Initialize an OSCPacket with the given UDP datagram.

        Args:
            dgram: the raw UDP datagram holding the OSC packet.

        Raises:
            OSCPacketParseError if the datagram could not be parsed.
        """
        now = calendar.timegm(time.gmtime())
        self._items = ()
        self._dgram = dgram

        try:
            if OSCBundle.is_valid(dgram):
                self._items = (TimedMessage(now, OSCBundle.parse(dgram)),)
            elif OSCMessage.is_valid(dgram):
                self._items = (TimedMessage(now, OSCMessage.parse(dgram)),)
            else:
                # Empty packet, should not happen as per the spec but heh, UDP...
                raise OSCPacketParseError('OSC Packet should at least contain an OSCMessage or an OSCBundle.')
        except (OSCBundleParseError, OSCMessageParseError) as pe:
            raise OSCPacketParseError('Could not parse packet %s' % pe)

    def __iter__(self):
        """Iterate over items"""

        return iter(self._items)

    def __len__(self):
        """Length of contents"""

        return len(self._items)

    def __getitem__(self, key):
        """Get item by index

        Returns:
            item from OSCPacket
        Raises:
            IndexError if index out of range
        """
        if key >= len(self._items):
            raise IndexError("Index out of range.")

        return self._items[key]

    def __cmp__(self, other):
        """Compare two OSCPacket's

        Returns:
            True if two OSCPacket's is the same
        """
        return self.dgram == other.dgram

    @property
    def dgram(self):
        """Returns datagram from which OSCPacket was build"""
        return self._dgram

    @property
    def size(self):
        """Size of datagram"""
        return len(self.dgram)


#
# Message
#

class OSCMessageParseError(Exception):
    """Base exception raised when a datagram parsing error occurs."""

    pass


class OSCMessageBuildError(Exception):
    """Error raised when an incomplete message is trying to be built."""

    pass


class OSCMessage(object):
    """Builds arbitrary OSCMessage instances."""

    ARG_TYPE_FLOAT = "f"
    ARG_TYPE_INT = "i"
    ARG_TYPE_STRING = "s"
    ARG_TYPE_BLOB = "b"
    ARG_TYPE_TRUE = "T"
    ARG_TYPE_FALSE = "F"

    _SUPPORTED_ARG_TYPES = (
        ARG_TYPE_FLOAT,
        ARG_TYPE_INT,
        ARG_TYPE_BLOB,
        ARG_TYPE_STRING,
        ARG_TYPE_TRUE,
        ARG_TYPE_FALSE
        )

    def __init__(self, address=None):
        """Initialize a new OSCMessage.

        Args:
            address: The osc address to send this message to.
        """

        self._address = address
        self._args = []
        self._dgram = b''

    def __iter__(self):
        """Returns an iterator over the parameters of this message."""

        return iter(self._args)

    def __len__(self):
        """Returns length of arguments"""

        return len(self._args)

    def __getitem__(self, key):
        """Get a OSCMessage argument by index

        Args:
            key (int): inex of argument

        Returns:
            argument of OSCMessage

        Raises:
            IndexError
        """

        if key >= len(self._args):
            raise IndexError("Index out of range.")

        return self._args[key]

    def __setitem__(self, key, value):
        """Set argument by index, if key is greater than 
        length of arguments `value` will be added to end of list

        Args:
            key (int): index of argument
            value: an argument
        """

        if key >= len(self._args):
            self.add(value)
        else:
            arg_type = self._arg_type(value)
            self._args[key] = (arg_type, value)

    def __delitem__(self, key):
        """Delete argument by index

        Args:
            key (int): index of argument
        """

        if key >= len(self._args):
            raise IndexError("Index out of range.")

        del self._args[key]

    def __cmp__(self, other):
        """Check two OSCMessage's to be equal

        Args:
            other (OSCMessage): other OSCMessage
        Returns:
            True if two messages equals
        """

        return self.dgram == other.dgram

    @property
    def address(self):
        """Returns the OSC address this message will be sent to."""

        return self._address

    @address.setter
    def address(self, value):
        """Sets the OSC address this message will be sent to."""

        self._address = value

    @property
    def args(self):
        """Returns list of arguments values."""

        return [a[1] for a in self._args]

    @property
    def size(self):
        """Size of datagram

        Returns:
            length of the datagram for this message.
        """

        return len(self._dgram)

    @property
    def dgram(self):
        """Datagram of OSCMessage

        Returns:
            the datagram from which this message was built.
        """

        return self._dgram

    def add(self, arg_value, arg_type=None):
        """Add a typed argument to this message.

        Args:
            arg_value: The corresponding value for the argument.
            arg_type: A value in ARG_TYPE_* defined in this class,
            if none then the type will be guessed.
        Raises:
            ValueError: if the type is not supported.
        """

        if arg_type and arg_type not in self._SUPPORTED_ARG_TYPES:
            raise ValueError(
                'arg_type must be one of {}'.format(self._SUPPORTED_ARG_TYPES))
        if not arg_type:
            arg_type = self._arg_type(arg_value)

        self._args.append((arg_type, arg_value))

    def build(self):
        """Builds an OSCMessage from the current state of this builder.

        Raises:
            OSCMessageBuildError: if the message could not be build or if the address was empty.

        Returns:
            an OSCMessage instance.
        """

        if not self._address:
            raise OSCMessageBuildError('OSC addresses cannot be empty')

        dgram = b''

        try:
            # Write the address.
            dgram += write_string(self._address)

            if not self._args:
                return OSCMessage.parse(dgram)

            # Write the parameters.
            arg_types = "".join([arg[0] for arg in self._args])
            dgram += write_string(',' + arg_types)

            for arg_type, value in self._args:
                if arg_type == self.ARG_TYPE_STRING:
                    dgram += write_string(value)
                elif arg_type == self.ARG_TYPE_INT:
                    dgram += write_int(value)
                elif arg_type == self.ARG_TYPE_FLOAT:
                    dgram += write_float(value)
                elif arg_type == self.ARG_TYPE_BLOB:
                    dgram += write_blob(value)
                elif arg_type == self.ARG_TYPE_TRUE or arg_type == self.ARG_TYPE_FALSE:
                    continue
                else:
                    raise OSCMessageBuildError('Incorrect parameter type found {}'.format(arg_type))

            return OSCMessage.parse(dgram)
        except OSCBuildError as be:
            raise OSCMessageBuildError('Could not build the message: {}'.format(be))

    def is_bundle(self):
        """Check is this a bundle

        Returns:
            whether this is bundle or not
        """

        return False

    @staticmethod
    def parse(dgram):
        """Create OSCMessage from datagram

        Args:
            dgram: from what to build OSCMessage

        Returns:
            OSCMessage parsed from datagram
        """

        message = OSCMessage()
        message._parse(dgram)

        return message

    @staticmethod
    def is_valid(dgram):
        """Check datagram to be valid OSCMessage

        Args:
            dgram: datagram os of OSCMessage

        Returns:
            whether this datagram starts as an OSC message.
        """

        return dgram.startswith(b'/')

    def _parse(self, dgram):
        """Parse datagram

        Args:
          - dgram: datagram of OSCMessage
        """

        self._dgram = dgram

        try:
            self._address, index = read_string(self._dgram, 0)

            if not self._dgram[index:]:
                # No params is legit, just return now.
                return

            # Get the parameters types.
            type_tag, index = read_string(self._dgram, index)

            if type_tag.startswith(','):
                type_tag = type_tag[1:]

            # Parse each parameter given its type.
            for param in type_tag:
                if param == "i":  # Integer.
                    val, index = read_int(self._dgram, index)
                elif param == "f":  # Float.
                    val, index = read_float(self._dgram, index)
                elif param == "s":  # String.
                    val, index = read_string(self._dgram, index)
                elif param == "b":  # Blob.
                    val, index = read_blob(self._dgram, index)
                elif param == "T":  # True.
                    val = True
                elif param == "F":  # False.
                    val = False
                # TODO: Support more exotic types as described in the specification.
                else:
                    logging.warning('Unhandled parameter type: {0}'.format(param))
                    continue

                self._args.append((param, val))
        except OSCParseError as pe:
            raise OSCMessageParseError('Found incorrect datagram, ignoring it', pe)

    def _arg_type(self, arg_value):
        """Get OSC type for `arg_value`

        Returns:
            OSC type
        """

        builtin_type = type(arg_value)
        arg_type = None

        if builtin_type == builtins.str:
            arg_type = self.ARG_TYPE_STRING
        elif builtin_type == builtins.bytes:
            arg_type = self.ARG_TYPE_BLOB
        elif builtin_type == builtins.int:
            arg_type = self.ARG_TYPE_INT
        elif builtin_type == builtins.float:
            arg_type = self.ARG_TYPE_FLOAT
        elif builtin_type == builtins.bool and arg_value:
            arg_type = self.ARG_TYPE_TRUE
        elif builtin_type == builtins.bool and not arg_value:
            arg_type = self.ARG_TYPE_FALSE

        return arg_type


#
# Bundle
#

_BUNDLE_PREFIX = b"#bundle\x00"


class OSCBundleParseError(Exception):
    """Base exception raised when a datagram parsing error occurs."""


class OSCBundleBuildError(Exception):
    """Error raised when an error occurs building the bundle."""


class OSCBundle(object):
    """Builds arbitrary OSCBundle instances."""

    def __init__(self, timestamp=IMMEDIATELY):
        """Build a new bundle with the associated timestamp.

        Args:
           timestamp: system time represented as a floating point number of
                      seconds since the epoch in UTC or IMMEDIATELY.
        """

        self._timestamp = timestamp
        self._contents = []
        self._dgram = b''

    def __iter__(self):
        """Returns:
            an iterator over the bundle's content.
        """

        return iter(self._contents)

    def __len__(self):
        """
        Returns:
            length of contents"""

        return len(self._contents)

    def __getitem__(self, key):
        """Get item from OSCBundle by index

        Returns:
            item from contents"""

        return self._contents[key]

    def __setitem__(self, key, value):
        """Set item of OSCBundle

        Args:
            key (int): index of item
            value (OSCBundle, OSCMessage): an OSCBundle or OSCMessage
        """
        
        if key >= len(self._contents):
            raise IndexError("Index out of range.")

        if not isinstance(value, OSCBundle) or not isinstance(value, OSCMessage):
            raise TypeError("Type of assigned values is not OSCBundle or OSCMessage.")

        self._contents[key] = value

    def __delitem__(self, key):
        """Remove item from bundle

        Args:
            key (int): index of item
        """

        if key >= len(self._contents):
            raise IndexError("Index out of range.")

        del self._contents[key]

    def __contains__(self, item):
        """Check if OSCMessage in bundle

        Returns:
            returns True if item in this bundle
        """

        return item in self._contents

    def __cmp__(self, other):
        """Compare two bundles

        Args:
            other (OSCBundle): other bundle to compare
        """

        return self.dgram == other.dgram

    @property
    def timestamp(self):
        """Returns:
            timestamp associated with this bundle.
        """

        return self._timestamp

    @property
    def length(self):
        """Returns:
            number of messages in bundle.
        """

        return len(self._contents)

    @property
    def size(self):
        """Returns:
            length of the datagram for this bundle.
        """

        return len(self._dgram)

    @property
    def dgram(self):
        """Returns:
            datagram from which this bundle was built.
        """

        return self._dgram

    def add(self, content):
        """Add a new content to this bundle.

        Args:
            content: Either an OSCBundle or an OSCMessage

        Raises:
            OSCBundleBuildError: if we could not build the bundle.
        """

        if isinstance(content, OSCMessage) or isinstance(content, OSCBundle):
            self._contents.append(content.build())
        else:
            raise OSCBundleBuildError("Content must be either OSCBundle or OSCMessage found {}".format(type(content)))

    def build(self):
        """Build an OSCBundle with the current state of this builder.

        Raises:
            OSCBundleBuildError: if we could not build the bundle.
        """

        dgram = b'' + _BUNDLE_PREFIX

        try:
            dgram += write_date(self._timestamp)

            for content in self._contents:
                if isinstance(content, OSCMessage) or isinstance(content, OSCBundle):
                    size = content.size
                    dgram += write_int(size)
                    dgram += content.dgram
                else:
                    raise OSCBundleBuildError(
                        "Content must be either OSCBundle or OSCMessage found {}".format(type(content)))

            return OSCBundle.parse(dgram)
        except OSCBuildError as be:
            raise OSCBundleBuildError('Could not build the bundle {}'.format(be))

    def is_bundle(self):
        """Returns whether this is bundle or not."""

        return True

    @staticmethod
    def is_valid(dgram):
        """Returns whether this datagram starts like an OSC bundle.

        Args:
            dgram: datagram of OSCBundle
        Returns:
            weather datagram is OSCBundle
        """

        return dgram.startswith(_BUNDLE_PREFIX)

    @staticmethod
    def parse(dgram):
        """Parse OSCBundle from datagram

        Args:
            dgram: datagram of OSCBundle
        Returns:
            OSCBundle instance
        """

        bundle = OSCBundle()
        bundle._parse(dgram)

        return bundle

    def _parse(self, dgram):
        """Parse datagram and fill contents of this OSCBundle

        Args:
            dgram: datagram of OSCBundle
        """

        # Interesting stuff starts after the initial b"#bundle\x00".
        self._dgram = dgram
        index = len(_BUNDLE_PREFIX)

        try:
            self._timestamp, index = get_date(self._dgram, index)
        except OSCParseError as pe:
            raise OSCBundleParseError("Could not get the date from the datagram: %s" % pe)

        # Get the contents as a list of OSCBundle and OSCMessage.
        self._contents = self._parse_contents(index)

    def _parse_contents(self, index):
        """Parse datagram into OSCBundle

        Raises:
            OSCBundleParseError: if we could not parse the bundle.
        """

        contents = []

        try:
            # An OSC Bundle Element consists of its size and its contents.
            # The size is an int32 representing the number of 8-bit bytes in the
            # contents, and will always be a multiple of 4. The contents are either
            # an OSC Message or an OSC Bundle.
            while self._dgram[index:]:
                # Get the sub content size.
                content_size, index = read_int(self._dgram, index)
                # Get the datagram for the sub content.
                content_dgram = self._dgram[index:index + content_size]
                # Increment our position index up to the next possible content.
                index += content_size
                # Parse the content into an OSC message or bundle.
                if OSCBundle.is_valid(content_dgram):
                    contents.append(OSCBundle.parse(content_dgram))
                elif OSCMessage.is_valid(content_dgram):
                    contents.append(OSCMessage.parse(content_dgram))
                else:
                    logging.warning("Could not identify content type of dgram %s" % content_dgram)
        except (OSCParseError, OSCMessageParseError, IndexError) as e:
            raise OSCBundleParseError("Could not parse a content datagram: %s" % e)

        return contents


#
# Client
#

class OSCClient(object):
    """OSC client to send OSCMessages or OSCBundle's via UDP."""

    def __init__(self, address, port):
        """Initialize the client.

        As this is UDP it will not actually make any attempt to connect to the
        given server at ip:port until the send() method is called.
        """

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setblocking(0)
        self._address = address
        self._port = port

    def send(self, message):
        """Sends an OSCBundle or OSCMessage to the server.

        Args:
            message: a OSCMessage or OSCBundle to send
        """

        self._sock.sendto(message.build().dgram, (self._address, self._port))


class OSCSender(object):
    """Send OSCMessage's and OSCBundle's to multiple servers"""

    def __init__(self):
        """Initialize the client."""

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setblocking(0)
        self._clients = []

    def add(self, address, port):
        """Add a recipient

        Args:
            address (str): ip address of server
            port (int): port of server
        """

        self._clients.append((address, port))

    def send(self, message):
        """Sends an OSCBundle or OSCMessage to the servers.

        Args:
            message: a OSCMessage or OSCBundle to send
        """

        dgram = message.build().dgram

        for address in self._clients:
            self._sock.sendto(dgram, address)


#
# Server
#

class _UDPRequestHandler(socketserver.BaseRequestHandler):
    """Handles correct UDP messages for all types of server.

    Whether this will be run on its own thread, the server's or a whole new
    process depends on the server you instantiated, look at their documentation.

    This method is called after a basic sanity check was done on the datagram,
    basically whether this datagram looks like an osc message or bundle,
    if not the server won't even bother to call it and so no new
    threads/processes will be spawned.
    """

    def handle(self):

        data = self.request[0]
        callback = self.server.handle

        # Get OSC messages from all bundles or standalone message.
        try:
            packet = OSCPacket(data)

            for timed_msg in packet:
                now = calendar.timegm(time.gmtime())

                # If the message is to be handled later, then so be it.
                if timed_msg.time > now:
                    time.sleep(timed_msg.time - now)

                callback(self.client_address, timed_msg.message, timed_msg.time)
        except OSCParseError:
            pass


class OSCServer(socketserver.UDPServer):
    """Superclass for different flavors of OSCServer"""

    def __init__(self, address, port):
        """Initialize OSCServer class

        Args:
            address (string): string representation of ip address, for example: '127.0.0.1'
            port (int): port of server
        """

        super(OSCServer, self).__init__((address, port), _UDPRequestHandler)

    def verify_request(self, request, client_address):
        """Returns true if the data looks like a valid OSC UDP datagram.

        Args:
            request: A request data
            client_address: Client address
        """

        data = request[0]

        return OSCBundle.is_valid(data) or OSCMessage.is_valid(data)

    def handle(self, address, message, date):
        """Handle receiving of OSCMessage or OSCBundle

        Args:
            address: typle (host, port)
            message: OSCMessage or OSCBundle
            date: int number which represents time of message
        Raises:
            NotImplementedError
        """

        raise NotImplementedError("Re-implement this method")


class OSCReceiver(OSCServer):
    """Receive messages only from some clients"""

    def handle(self, address, message, date):
        """Handle receiving of OSCMessage or OSCBundle

        Args:
            address: typle (host, port)
            message: OSCMessage or OSCBundle
            date: int number which represents time of message
        Raises:
            NotImplementedError
        """
        super(OSCReceiver, self).handle(address, message, date)

    def __init__(self, address, port):
        """Initialize OSCReceiver class

        Args:
            address (string): string representation of ip address, for example: '127.0.0.1'
            port (int): port of server
        """

        super(OSCReceiver, self).__init__(address, port)

        self._clients = []

    def verify_request(self, request, client_address):
        """Returns true if the data looks like a valid OSC UDP datagram.

        Args:
            request: A request data
            client_address: Client address
        """

        data = request[0]

        for client in self._clients:
            if client[0] == client_address[0] and client[1] == client_address[1]:
                return OSCBundle.is_valid(data) or OSCMessage.is_valid(data)

        return False

    def add(self, address, port):
        """Add client address

        Args:
            address (string): string representation of ip address, for example: '127.0.0.1'
            port (int): port of server
        """

        self._clients.append((address, port))


class OSCBlockingServer(OSCServer):
    """Blocking version of the UDP server.

    Each message will be handled sequentially on the same thread.
    Use this is you don't care about latency in your message handling or don't
    have a multiprocess/multithreaded environment.
    """

    def handle(self, address, message, date):
        pass


class OSCThreadingServer(socketserver.ThreadingMixIn, OSCServer):
    """Threading version of the OSC UDP server.

    Each message will be handled in its own new thread.
    Use this when lightweight operations are done by each message handlers.
    """

    def handle(self, address, message, date):
        pass


class OSCForkingServer(socketserver.ForkingMixIn, OSCServer):
    """Forking version of the OSC UDP server.

    Each message will be handled in its own new process.
    Use this when heavyweight operations are done by each message handlers
    and forking a whole new process for each of them is worth it.
    """

    def handle(self, address, message, date):
        pass

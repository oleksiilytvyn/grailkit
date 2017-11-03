# -*- coding: UTF-8 -*-
"""
    grailkit.artnet
    ~~~~~~~~~~~~~~~

    ArtNet implementation in pure Python
    Art-Net(tm) Designed by and Copyright Artistic License Holdings Ltd.
    Based on https://github.com/philchristensen/python-artnet

    CAUTION! This module is highly unstable and incomplete

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import uuid
import time
import struct
import socket
import calendar
import bitstring
import socketserver

from grailkit.dmx import DMXUniverse

# TODO: Check this module

DEFAULT_PORT = 6454

OPCODES = dict(
    # This is an ArtPoll packet, no other data is contained in this UDP packet.
    OpPoll=0x0020,
    # This is an ArtPollReply Packet. It contains device status information.
    OpPollReply=0x0021,
    # Diagnostics and data logging packet.
    OpDiagData=0x0023,
    # Used to send text based parameter commands.
    OpCommand=0x0024,
    # This is an ArtDmx data packet. It contains zero start code DMX512 information for a single DMXUniverse.
    OpOutput=0x0050,
    # This is an ArtDmx data packet. It contains zero start code DMX512 information for a single DMXUniverse.
    OpDmx=0x0050,
    # This is an ArtNzs data packet.
    # It contains non-zero start code (except RDM) DMX512 information for a single DMXUniverse.
    OpNzs=0x0051,
    # This is an ArtAddress packet. It contains remote programming information for a Node.
    OpAddress=0x0060,
    # This is an ArtInput packet. It contains enable  disable data for DMX inputs.
    OpInput=0x0070,
    # This is an ArtTodRequest packet. It is used to request a Table of Devices (ToD) for RDM discovery.
    OpTodRequest=0x0080,
    # This is an ArtTodData packet. It is used to send a Table of Devices (ToD) for RDM discovery.
    OpTodData=0x0081,
    # This is an ArtTodControl packet. It is used to send RDM discovery control messages.
    OpTodControl=0x0082,
    # This is an ArtRdm packet. It is used to send all non discovery RDM messages.
    OpRdm=0x0083,
    # This is an ArtRdmSub packet. It is used to send compressed, RDM Sub-Device data.
    OpRdmSub=0x0084,
    # This is an ArtVideoSetup packet.
    # It contains video screen setup information for nodes that implement the extended video features.
    OpVideoSetup=0x10a0,
    # This is an ArtVideoPalette packet.
    # It contains colour palette setup information for nodes that implement the extended video features.
    OpVideoPalette=0x20a0,
    # This is an ArtVideoData packet. It contains display data for nodes that implement the extended video features.
    OpVideoData=0x40a0,
    # This is an ArtMacMaster packet.
    # It is used to program the Node's MAC address, Oem device type and ESTA manufacturer code.
    # This is for factory initialisation of a Node. It is not to be used by applications.
    OpMacMaster=0x00f0,
    # This is an ArtMacSlave packet. It is returned by the node to acknowledge receipt of an ArtMacMaster packet.
    OpMacSlave=0x00f1,
    # This is an ArtFirmwareMaster packet. It is used to upload new firmware or firmware extensions to the Node.
    OpFirmwareMaster=0x00f2,
    # This is an ArtFirmwareReply packet.
    # It is returned by the node to acknowledge receipt of an ArtFirmwareMaster packet or ArtFileTnMaster packet.
    OpFirmwareReply=0x00f3,
    # Uploads user file to node.
    OpFileTnMaster=0x00f4,
    # Downloads user file from node.
    OpFileFnMaster=0x00f5,
    # Node acknowledge for downloads.
    OpFileFnReply=0x00f6,
    # This is an ArtIpProg packet. It is used to reprogramme the IP, Mask and Port address of the Node.
    OpIpProg=0x00f8,
    # This is an ArtIpProgReply packet. It is returned by the node to acknowledge receipt of an ArtIpProg packet.
    OpIpProgReply=0x00f9,
    # This is an ArtMedia packet. It is Unicast by a Media Server and acted upon by a Controller.
    OpMedia=0x0090,
    # This is an ArtMediaPatch packet. It is Unicast by a Controller and acted upon by a Media Server.
    OpMediaPatch=0x0091,
    # This is an ArtMediaControl packet. It is Unicast by a Controller and acted upon by a Media Server.
    OpMediaControl=0x0092,
    # This is an ArtMediaControlReply packet. It is Unicast by a Media Server and acted upon by a Controller.
    OpMediaContrlReply=0x0093,
    # This is an ArtTimeCode packet. It is used to transport time code over the network.
    OpTimeCode=0x0097,
    # Used to synchronise real time date and clock
    OpTimeSync=0x0098,
    # Used to send trigger macros
    OpTrigger=0x0099,
    # Requests a node's file list
    OpDirectory=0x009a,
    # Replies to OpDirectory with file list
    OpDirectoryReply=0x9b00
    )

NODE_REPORT_CODES = dict(
    RcDebug=('0x0000', "Booted in debug mode"),
    RcPowerOk=('0x0001', "Power On Tests successful"),
    RcPowerFail=('0x0002', "Hardware tests failed at Power On"),
    RcSocketWr1=('0x0003', "Last UDP from Node failed due to truncated length, Most likely caused by a collision."),
    RcParseFail=('0x0004', "Unable to identify last UDP transmission. Check OpCode and packet length."),
    RcUdpFail=('0x0005', "Unable to open Udp Socket in last transmission attempt"),
    RcShNameOk=('0x0006', "Confirms that Short Name programming via ArtAddress, was successful."),
    RcLoNameOk=('0x0007', "Confirms that Long Name programming via ArtAddress, was successful."),
    RcDmxError=('0x0008', "DMX512 receive errors detected."),
    RcDmxUdpFull=('0x0009', "Ran out of internal DMX transmit buffers."),
    RcDmxRxFull=('0x000a', "Ran out of internal DMX Rx buffers."),
    RcSwitchErr=('0x000b', "Rx Universe switches conflict."),
    RcConfigErr=('0x000c', "Product configuration does not match firmware."),
    RcDmxShort=('0x000d', "DMX output short detected. See GoodOutput field."),
    RcFirmwareFail=('0x000e', "Last attempt to upload new firmware failed."),
    RcUserFail=('0x000f',
                "User changed switch settings when address locked by remote programming. User changes ignored.")
    )

STYLE_CODES = {
    'StNode': 0x00,        # A DMX to / from Art-Net device
    'StController': 0x01,  # A lighting console.
    'StMedia': 0x02,       # A Media Server.
    'StRoute': 0x03,       # A network routing device.
    'StBackup': 0x04,      # A backup device.
    'StConfig': 0x05,      # A configuration or diagnostic tool.
    'StVisual': 0x06       # A visualiser.
    }


class ArtNetParseError(Exception):
    """Base exception related to artnet module"""

    pass


class ArtNetPacket(object):
    """ArtNet packet"""

    opcode = None
    schema = ()

    opcode_map = {}
    header = b'Art-Net\0'
    protocol_version = 14

    def __init__(self, address=None, universe=0, sequence=0, physical=0):
        """Create an empty ArtNet packed

        Args:
            address (str): IP address of sender
            sequence (int): unknown thing
            physical (int): unknown thing
            universe (int): number of DMX universe
        """

        self.address = address
        self.sequence = sequence
        self.physical = physical
        self.universe = universe

    def __str__(self):
        """String representation of ArtNet packet"""

        return '<%s from %s:%d/%d>' % (self.__class__.__name__, self.address, self.universe, self.physical)

    @property
    def dgram(self):
        """Returns datagram for packet"""

        fields = []

        for name, fmt in self.schema:
            accessor = getattr(self, 'format_%s' % name, '\0')

            if callable(accessor):
                value = accessor()
            else:
                value = getattr(self, name)

            fields.append([name, fmt, value])

        fmt = ', '.join(['='.join([f, n]) for n, f, v in fields])
        data = dict([(n, v) for n, f, v in fields])

        return bitstring.pack(fmt, **data).tobytes()

    @classmethod
    def register(cls, packet_class):
        """Register ArtNet packet type"""

        cls.opcode_map[packet_class.opcode] = packet_class

        return packet_class

    @classmethod
    def decode(cls, address, data):
        """Create packet from datagram"""

        opcode = struct.unpack('!H', data[8:10])

        if opcode not in cls.opcode_map:
            raise NotImplementedError('%x' % opcode)

        klass = cls.opcode_map[opcode]
        b = data
        fields = dict()

        for name, fmt in klass.schema:
            accessor = getattr(klass, 'parse_%s' % name, None)

            if callable(accessor):
                fields[name] = accessor(b, fmt)
            else:
                fields[name] = b.read(fmt)

        p = klass(address=address)

        for k, v in fields.items():
            setattr(p, k, v)

        return p

    @classmethod
    def is_valid(cls, data):
        """Returns True if given datagram is valid ArtNet UDP packet."""

        return data[0:8] == cls.header


@ArtNetPacket.register
class ArtNetDMXPacket(ArtNetPacket):
    """ArtNet DMX packet"""

    opcode = OPCODES['OpDmx']
    schema = (
        ('header', 'bytes:8'),
        ('opcode', 'int:16'),
        ('protocol_version', 'uintbe:16'),
        ('sequence', 'int:8'),
        ('physical', 'int:8'),
        ('universe', 'uintle:16'),
        ('length', 'uintbe:16'),
        ('framedata', 'bytes:512')
        )

    def __init__(self, **kwargs):
        super(ArtNetDMXPacket, self).__init__(**kwargs)

        self.frame = DMXUniverse()

    @classmethod
    def parse_framedata(cls, b, fmt):

        return DMXUniverse([ord(x) for x in b.read('bytes:512')])

    def format_length(self):

        return len(self.frame)

    def format_framedata(self):

        return ''.join([chr(i or 0) for i in self.frame])


@ArtNetPacket.register
class ArtNetPollPacket(ArtNetPacket):
    """ArtNet Poll packet"""

    opcode = OPCODES['OpPoll']
    schema = (
        ('header', 'bytes:8'),
        ('opcode', 'int:16'),
        ('protocol_version', 'uintbe:16'),
        ('talktome', 'int:8'),
        ('priority', 'int:8')
        )

    def __init__(self, talktome=0x02, priority=0, **kwargs):
        super(ArtNetPollPacket, self).__init__(**kwargs)

        self.talktome = talktome
        self.priority = priority


@ArtNetPacket.register
class ArtNetPollReplyPacket(ArtNetPacket):
    """ArtNet PollReply packet"""

    opcode = OPCODES['OpPollReply']
    counter = 0

    port = DEFAULT_PORT

    short_name = 'python-artnet'
    long_name = 'https://github.com/philchristensen/python-artnet.git'
    style = STYLE_CODES['StController']
    esta_manufacturer = 'PA'
    version = 1
    universe = 0
    status1 = 2
    status2 = bitstring.Bits('0b0111').int

    num_ports = 0
    port_types = '\0\0\0\0'
    good_input = '\0\0\0\0'
    good_output = '\0\0\0\0'

    bind_ip = '\0\0\0\0'
    mac_address = uuid.getnode()

    schema = (
        ('header', 'bytes:8'),
        ('opcode', 'int:16'),
        ('ip_address', 'bytes:4'),
        ('port', 'int:16'),
        ('version', 'uintbe:16'),
        ('net_switch', 'int:8'),
        ('sub_switch', 'int:8'),
        ('oem', 'uintbe:16'),
        ('ubea_version', 'int:8'),
        ('status1', 'int:8'),
        ('esta_manufacturer', 'bytes:2'),
        ('short_name', 'bytes:18'),
        ('long_name', 'bytes:64'),
        ('node_report', 'bytes:64'),
        ('num_ports', 'uintbe:16'),
        ('port_types', 'bytes:4'),
        ('good_input', 'bytes:4'),
        ('good_output', 'bytes:4'),
        ('switch_in', 'int:8'),
        ('switch_out', 'int:8'),
        ('switch_video', 'int:8'),
        ('switch_macro', 'int:8'),
        ('switch_remote', 'int:8'),
        ('spare1', 'int:8'),
        ('spare2', 'int:8'),
        ('spare3', 'int:8'),
        ('style', 'int:8'),
        ('mac_address', 'uintle:48'),
        ('bind_ip', 'bytes:4'),
        ('bind_index', 'int:8'),
        ('status2', 'int:8'),
        ('filler', 'bytes')
    )

    def __init__(self, **kwargs):
        super(ArtNetPollReplyPacket, self).__init__(**kwargs)

        ArtNetPollReplyPacket.counter += 1

    def format_ip_address(self):
        address = socket.gethostbyname(socket.gethostname())
        return bitstring.pack('uint:8, uint:8, uint:8, uint:8', *[int(x) for x in address.split('.')]).bytes

    @classmethod
    def parse_ip_address(cls, b, fmt):
        b = bitstring.BitStream(bytes=b.read(fmt))
        address = b.readlist(','.join(['uint:8'] * 4))
        return '.'.join([str(x) for x in address])

    def format_short_name(self):
        return self.short_name[0:18].ljust(18)

    @classmethod
    def parse_short_name(cls, b, fmt):
        short_name = b.read(fmt)
        return short_name.strip()

    def format_long_name(self):
        return self.long_name[0:64].ljust(64)

    @classmethod
    def parse_long_name(cls, b, fmt):
        long_name = b.read(fmt)
        return long_name.strip()

    def format_node_report(self):
        node_report = "#0001 [%s] Power On Tests successful" % ArtNetPollReplyPacket.counter
        return node_report[0:64].ljust(64)

    @classmethod
    def parse_node_report(cls, b, fmt):
        node_report = b.read(fmt)
        return node_report.strip()


@ArtNetPacket.register
class ArtNetTodRequestPacket(ArtNetPacket):
    """ArtNet TodRequest packet"""

    opcode = OPCODES['OpTodRequest']
    schema = (
        ('header', 'bytes:8'),
        ('opcode', 'int:16'),
        ('protocol_version', 'uintbe:16'),
        ('filler1', 'int:8'),
        ('filler2', 'int:8'),
        ('spare1', 'int:8'),
        ('spare2', 'int:8'),
        ('spare3', 'int:8'),
        ('spare4', 'int:8'),
        ('spare5', 'int:8'),
        ('spare6', 'int:8'),
        ('spare7', 'int:8'),
        ('net', 'int:8'),
        ('command', 'int:8'),
        ('addcount', 'int:8'),
        # ('addr', 'int:8')
        )

    def __init__(self, **kwargs):
        super(ArtNetTodRequestPacket, self).__init__(**kwargs)


class _UDPRequestHandler(socketserver.BaseRequestHandler):
    """Handles correct UDP packets for all types of server.

    Whether this will be run on its own thread, the server's or a whole new
    process depends on the server you instantiated, look at their documentation.

    This method is called after a basic sanity check was done on the datagram,
    basically whether this datagram looks like an ArtNet packet,
    if not the server won't even bother to call it and so no new
    threads/processes will be spawned.
    """

    def handle(self):
        """Handle UDP request and call handler callback"""

        data = self.request[0]
        callback = self.server.handle

        try:
            packet = ArtNetPacket.decode(self.client_address[0], data)
            now = calendar.timegm(time.gmtime())

            callback(self.client_address, packet, now)
        except ArtNetParseError:
            pass


class ArtNetServer(socketserver.UDPServer):
    """Superclass for different flavors of ArtNetServer

    You can change server logic by extending from both
    ArtNetServer and socketserver.ThreadingMixIn or socketserver.ForkingMixIn
    """

    def __init__(self, address='127.0.0.1', port=9000):
        """Initialize ArtNetServer class

        Args:
            address (string): string representation of ip address, for example: '127.0.0.1'
            port (int): port of server
        """

        super(ArtNetServer, self).__init__((address, port), _UDPRequestHandler)

    def verify_request(self, request, client_address):
        """Returns true if the data looks like a valid ArtNet UDP datagram.

        Args:
            request: A request data
            client_address: Client address
        Returns:
            True if request is valid
        """

        data = request[0]

        return ArtNetPacket.is_valid(data)

    def handle(self, address, packet, date):
        """Handle receiving of ArtNet packets

        Args:
            address: typle (host, port)
            packet: instance of ArtNetPacket
            date: int number which represents time of message
        Raises:
            NotImplementedError if you don't override it
        """

        raise NotImplementedError("Re-implement this method")


class ArtNetClient(object):
    """Send ArtNetPacket to multiple servers"""

    def __init__(self, address='127.0.0.1', port=False):
        """Initialize the client.

        Args:
            address (str): recipient ip address
            port (int): recipient port
        """

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setblocking(0)
        self._clients = []
        self._closed = False

        if address and port:
            self.add(address, port)

    def __len__(self):
        """Returns number of clients"""

        return len(self._clients)

    def __bool__(self):
        """Returns True if at least one client is available"""

        return len(self) > 0

    @property
    def clients(self):
        """Returns list of receipts"""

        return self._clients

    def add(self, address, port):
        """Add a recipient

        Args:
            address (str): ip address of server
            port (int): port of server
        Raises:
            ValueError if one of arguments is invalid
        """

        if not isinstance(address, str):
            raise ValueError("Given address is not a string")

        if not isinstance(port, int) or port <= 0:
            raise ValueError("Given port number is not int or invalid")

        self._clients.append((address, port))

    def remove(self, address, port):
        """Remove a recipient

        Args:
            address (str): ip address of server
            port (int): port of server
        """

        for client in self._clients:
            if client[0] == address and client[1] == port:
                self._clients.remove(client)

                break

    def clear(self):
        """Clear list of receipts"""

        self._clients = []

    def send(self, packet):
        """Sends an ArtNetPacket to the servers.

        Args:
            packet (ArtNetPacket): a packet to send
        """

        if not isinstance(packet, ArtNetPacket):
            raise ValueError("Given packet is not a ArtNetPacket")

        # create new socket if previously closed
        if self._closed:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.setblocking(0)
            self._closed = False

        for address in self._clients:
            self._socket.sendto(packet.dgram, address)

    def close(self):
        """Close socket connection"""

        if not self._closed:
            self._socket.close()
            self._closed = True

# -*- coding: UTF-8 -*-
"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""
from grailkit.dmx import dmx_serial_ports, DMXUniverse, DMXDevice


def main():
    """Test this module"""

    print('Available ports:')
    ports = dmx_serial_ports()
    for port in ports:
        print('\t', port)
    print('\n')

    frame = DMXUniverse()

    for x in range(4):
        frame[x*16] = 255  # brightness
        frame[x*16+1] = 255  # red
        frame[x*16+2] = 255  # green
        frame[x*16+3] = 255  # blue

    device = DMXDevice(ports[1])

    for t in range(1):
        print('Sending frame %d with L=%d' % (t+1, len(frame)))
        device.send(frame)

if __name__ == '__main__':
    main()

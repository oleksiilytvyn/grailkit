# -*- coding: UTF-8 -*-
"""
    grailkit.graphics.color
    ~~~~~~~~~~~~~~~~~~~~~~~

    Color type and predefined colors

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""


class Color(object):
    """Color representation"""

    __slots__ = ['r', 'g', 'b', 'a']

    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        """Create color

        Args:
            r (float, int): Red value
            g (float, int): Green value
            b (float, int): Blue value
            a (float, int): Opacity value
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def to_hex(self):
        """Returns color in RGB hex format"""

        return '#%02x%02x%02x' % (self.r, self.g, self.b)

    def to_hex_rgba(self):
        """Returns color in RGBA hex format"""

        return '#%02x%02x%02x%02x' % (self.r, self.g, self.b, self.a)

    @staticmethod
    def from_hex(value):
        """Create color instance from rgb hex string

        Args:
            value (str): rgb color in hex format
        """

        if value[0] == '#':
            value = value[1:]

        r = 0.0
        g = 0.0
        b = 0.0
        a = 0.0

        if len(value) == 3:
            r = int(value[:1]*2, 16)
            g = int(value[1:2]*2, 16)
            b = int(value[2:3]*2, 16)
        elif len(value) == 6:
            r = int(value[:2], 16)
            g = int(value[2:4], 16)
            b = int(value[4:6], 16)
        elif len(value) == 8:
            r = int(value[:2], 16)
            g = int(value[2:4], 16)
            b = int(value[4:6], 16)
            a = int(value[6:8], 16)

        return Color(r, g, b, a)

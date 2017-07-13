# -*- coding: UTF-8 -*-
"""
    grailkit.graphics.color
    ~~~~~~~~~~~~~~~~~~~~~~~

    Color type and predefined colors

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
import colorsys


class Color(object):
    """Color representation"""

    __slots__ = ['r', 'g', 'b', 'a']

    def __init__(self, r=0.0, g=0.0, b=0.0, a=1.0):
        """Create color

        Args:
            r (int): Red value, from 0 to 255
            g (int): Green value, from 0 to 255
            b (int): Blue value, from 0 to 255
            a (float): Opacity value, from 0.0 to 1.0
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @property
    def lightness(self):
        """Returns color lightness"""

        return colorsys.rgb_to_hls(self.r, self.g, self.b)[1]

    @property
    def hue(self):
        """Returns color hue"""

        return colorsys.rgb_to_hls(self.r, self.g, self.b)[0]

    @property
    def saturation(self):
        """Returns color saturation"""

        return colorsys.rgb_to_hls(self.r, self.g, self.b)[2]

    @property
    def alpha(self):
        """Returns alpha component"""

        return self.a

    def to_hls(self):
        """Returns HSL color components as typle (hue, lightness, saturation)"""

        return colorsys.rgb_to_hls(self.r, self.g, self.b)

    def to_hsv(self):
        """Returns typle HSV coordinates"""

        return colorsys.rgb_to_hsv(self.r, self.g, self.b)

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

        # RGB
        if len(value) == 3:
            r = int(value[:1]*2, 16)
            g = int(value[1:2]*2, 16)
            b = int(value[2:3]*2, 16)
        # RRGGBB
        elif len(value) == 6:
            r = int(value[:2], 16)
            g = int(value[2:4], 16)
            b = int(value[4:6], 16)
        # RRGGBBAA
        elif len(value) == 8:
            r = int(value[:2], 16)
            g = int(value[2:4], 16)
            b = int(value[4:6], 16)
            a = int(value[6:8], 16)

        return Color(r, g, b, a)

    @classmethod
    def from_hls(cls, h, s, l):
        """Create color from HLS"""

        return Color(*colorsys.hls_to_rgb(h, l, s))

    @classmethod
    def from_hsv(cls, h, s, v):
        """Create color from HSV"""

        return Color(*colorsys.hsv_to_rgb(h, s, v))


Colors = {
    'black': '#000000',
    'white': '#ffffff',
    'grey': '#cccccc',
    'red': '#ff0000',
    'green': '#00ff00',
    'blue': '#0000ff'
    }

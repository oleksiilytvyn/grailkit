# -*- coding: UTF-8 -*-
"""
    grailkit.app.graphics
    ~~~~~~~~~~~~~~~~~~~~~

    OpenGL library for drawing primitives and text
"""

from pyglet.gl import *
from pyglet.glu import *

from grailkit.core import Color, Rect, Point


class Graphics(object):
    """Class for handling drawing"""

    def __init__(self, context=None):
        pass

    def fill(self, r, g, b, a=1.0):
        pass

    def rect(self, x, y, width, height):
        pass

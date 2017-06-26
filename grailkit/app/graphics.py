# -*- coding: UTF-8 -*-
"""
    grailkit.app.graphics
    ~~~~~~~~~~~~~~~~~~~~~

    OpenGL library for drawing primitives and text
    https://github.com/memononen/nanovg

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
import pyglet
from pyglet.gl import *


class Graphics(object):
    """Draw 2d graphics easily using OpenGL"""

    def __init__(self, context=None):
        super(Graphics, self).__init__()

        self._context = context
        self._color = (0, 0, 0, 0)
        self._batch = pyglet.graphics.Batch()

    @property
    def color(self):
        """Paint color"""

        return self._color

    @color.setter
    def color(self, value):
        """Set paint color"""

        pass

    def clear(self):
        """Clear canvas"""

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

    def clear_rect(self, x, y, width, height):
        """Sets all pixels in the rectangle defined by starting point (x, y) and size (width, height)
        to transparent black, erasing any previously drawn content.

        Args:
            x (int, float): x coordinate
            y (int, float): y coordinate
            width (int, float): width
            height (int, float): height
        """

        # todo: Implement this
        pass

    def fill_rect(self, x, y, width, height):
        """Draws a filled rectangle at (x, y) position whose size is determined by `width` and `height`.

        Args:
            x (int, float): x coordinate
            y (int, float): y coordinate
            width (int, float): width
            height (int, float): height
        """

        # todo: Implement this
        pass

    def stroke_rect(self, x, y, width, height):
        """Paints a rectangle which has a starting point at (x, y) and has a `width` width and an `height` height onto
        the canvas, using the current stroke style.

        Args:
            x (int, float): x coordinate
            y (int, float): y coordinate
            width (int, float): width
            height (int, float): height
        """

        # todo: Implement this
        pass

    def end(self):
        """Draw graphics"""

        self._batch.draw()


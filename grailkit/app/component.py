# -*- coding: UTF-8 -*-
"""
    grailkit.app.component
    ~~~~~~~~~~~~~~~~~~~~~~

    Base type of all components

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from pyglet.gl import *


class Component(object):
    """Simple component that can handle various events and draw self no OpenGL context"""

    def __init__(self, parent=None):

        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def size(self):
        return self.width, self.height

    def on_focus(self, focused):
        """Component looses or receives focus event

        Args:
            focused (bool): True if component received focus
        """

        pass

    def on_draw(self):
        pass

    def on_mouse(self):
        pass

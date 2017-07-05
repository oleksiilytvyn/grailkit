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
        self.z = 0
        self.width = 0
        self.height = 0
        self.anchor_x = 0
        self.anchor_y = 0

        self._parent = None
        self._focused = False

    def size(self):
        """Returns width and height of component"""

        return self.width, self.height

    def minimum(self):
        """Returns minimum size of component"""

        return self.width * 0.2, self.height * 0.2

    def maximum(self):
        """Returns maximum size of component"""

        return self.width, self.height

    @property
    def is_owned(self):
        """Returns True if component owned by parent container"""

        return bool(self._parent)

    @property
    def parent(self):
        """Returns reference to parent container"""

        return self._parent

    def set_parent(self, parent=None):
        """Set parent container of this component"""

        self._parent = parent

    @property
    def focused(self):
        """Returns True if focus on this this component"""

        return self._focused

    def on_focus(self, focused):
        """Component looses or receives focus event

        Args:
            focused (bool): True if component received focus
        """

        pass

    def on_draw(self):
        """Draw component"""

        pass

    def on_update(self):
        """Update component state"""

        pass

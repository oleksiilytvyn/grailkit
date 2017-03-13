# -*- coding: UTF-8 -*-
"""
    grailkit.ui.component
    ~~~~~~~~~~~~~~~~~~~~~

    Basic UI/gl component

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from grailkit.core import Rect


class Component(Rect):
    """Implementation of simple component for further use in other classes"""

    def __int__(self, parent):
        pass

    def on_draw(self):
        """Called each time when component is drawn"""

        pass

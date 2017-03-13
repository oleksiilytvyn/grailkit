# -*- coding: UTF-8 -*-
"""
    grailkit.ui.layout
    ~~~~~~~~~~~~~~~~~~

    Layout management

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from weakref import WeakSet


class Layout(object):
    """Layout management"""

    def __init__(self):

        self._items = WeakSet()

    def append(self, component):
        """Add component to layout"""

        self._items.add(component)

# -*- coding: UTF-8 -*-
"""
    grailkit._ui.abstract.layout
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Layout components

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from .component import Component


class Layout(Component):
    """Abstract layout"""

    def __init__(self):
        super(Layout, self).__init__()

    def set_spacing(self, spacing):
        """Set spacing between components in layout

        Args:
            spacing (int): space between components in pixels
        """

        raise NotImplementedError("This is abstract method")

    def set_margins(self, left, top, right, bottom):
        """Set layout margins

        Args:
            left (int): left padding
            top (int): top padding
            right (int): right padding
            bottom (int): bottom padding
        """

        raise NotImplementedError("This is abstract method")


class BoxLayout(Layout):

    def __len__(self):
        """Returns number of components in layout"""

        return 0

    def append(self, component):
        """Append component to the layout"""

        raise NotImplementedError("This is abstract method")

    def insert(self, index, component):
        """Insert component at given position"""

        raise NotImplementedError("This is abstract method")

    def remove(self, component):
        """Remove component from layout"""

        raise NotImplementedError("This is abstract method")


class HLayout(Layout):
    """Horizontal box layout component"""

    pass


class VLayout(Layout):
    """Vertical box layout component"""

    pass


class GridLayout(Layout):
    """Grid layout component"""

    def add(self, component, row=0, column=0, row_span=1, column_span=1, align=None):

        raise NotImplementedError("This is abstract method")


class StackedLayout(BoxLayout):
    """Component that holds other components but only one can be visible at a time"""

    @property
    def current(self):
        """Returns index of currently visible component"""

        return 0

    def set_current(self, index):
        """Set component at `index` to be visible"""

        raise NotImplementedError("This is abstract method")

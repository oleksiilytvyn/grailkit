# -*- coding: UTF-8 -*-
"""
    grailkit.ui.abs.layout
    ~~~~~~~~~~~~~~~~~~~~~~

    Layout
"""
from .component import Component


class Layout(Component):
    """Abstract layout"""

    def __init__(self):
        super(Layout, self).__init__()

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

    def set_spacing(self, spacing):
        """Set spacing between components in layout

        Args:
            spacing (int): space between components in pixels
        """

        raise NotImplementedError("This is abstract method")

    def set_padding(self, left, top, right, bottom):
        """Set layout padding

        Args:
            left (int): left padding
            top (int): top padding
            right (int): right padding
            bottom (int): bottom padding
        """

        raise NotImplementedError("This is abstract method")


class HLayout(Layout):
    """Horizontal layout component"""

    pass


class VLayout(Layout):

    pass


class GridLayout(Layout):
    """Grid layout component"""

    pass

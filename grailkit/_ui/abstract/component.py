# -*- coding: UTF-8 -*-
"""
    grailkit.ui.abs.component
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""


class Component(object):

    def __init__(self):

        self._parent = None

    @property
    def name(self):
        """Returns component name"""
        return ""

    @property
    def width(self):
        """Returns component width"""

        return 0

    @property
    def height(self):
        """Returns component height"""

        return 0

    @property
    def x(self):
        """Returns component position relative to parent"""

        return 0

    @property
    def y(self):
        """Returns component position relative to parent"""

        return 0

    @property
    def visible(self):
        """Returns True if window is visible"""

        return True

    def set_visible(self, visible):
        """Show or hide the window

        Args:
            visible (bool): True if visible
        """

        raise NotImplementedError("This is abstract method")

    def activate(self):
        """Try to return focus to the window"""

        raise NotImplementedError("This is abstract method")

    def close(self):
        """Close window"""

        raise NotImplementedError("This is abstract method")

    def set_size(self, width, height):
        """Set size of window

        Args:
            width (int, float): window width
            height (int, float): window height
        """

        raise NotImplementedError("This is abstract method")

    def set_minimum_size(self, width, height):
        """Set minimum window size

        Args:
            width (int, float): window width
            height (int, float): window height
        """

        raise NotImplementedError("This is abstract method")

    def set_maximum_size(self, width, height):
        """Set a maximum window size

        Args:
            width (int, float): window width
            height (int, float): window height
        """

        raise NotImplementedError("This is abstract method")

    def set_location(self, x, y):
        """Set window location

        Args:
            x (int, float): x coordinate
            y (int, float): y coordinate
        """

        raise NotImplementedError("This is abstract method")

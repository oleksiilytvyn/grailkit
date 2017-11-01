# -*- coding: UTF-8 -*-
"""
    grailkit._ui.abstract.window
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Window classes

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""


class Window(object):
    """A basic window"""

    # Window style constants
    WINDOW_STYLE_BORDERLESS = 0
    WINDOW_STYLE_DEFAULT = 1
    WINDOW_STYLE_DIALOG = 2
    WINDOW_STYLE_TOOL = 3

    def __init__(self, width, height, caption="", style=None, resizable=True, visible=True):
        """Create a window

        Args:
            width (int): window width
            height (int): window height
            caption (str): window title
            style: window style flag
            resizable (bool): If True window can be resized by user
            visible (bool): If True window will be show immediately
        """

        self.set_caption(caption)
        self.set_size(width, height)
        self.set_resizable(resizable)
        self.set_visible(visible)

    @property
    def caption(self):
        """Returns windows title string"""

        return None

    def set_caption(self, title):
        """Set window title

        Args:
            title (str): window title
        """

        raise NotImplementedError("This is abstract method")

    @property
    def icon(self):
        """Returns window icon"""

        return None

    def set_icon(self, icon):
        """Set window icon

        Args:
            icon: window icon
        """

        raise NotImplementedError("This is abstract method")

    @property
    def width(self):
        """Returns window width"""

        return 0

    @property
    def height(self):
        """Returns window height"""

        return 0

    @property
    def resizable(self):
        """Returns True if window resizable"""

        return True

    def set_resizable(self, flag):
        """Set window as resizable"""

        raise NotImplementedError("This is abstract method")

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

    def set_component(self, component):
        """Set given component as main window component

        Args:
            component (grailkit.ui.Component): component that will take place in window
        """

        raise NotImplementedError("This is abstract method")

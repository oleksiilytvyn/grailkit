# -*- coding: UTF-8 -*-
"""
    grailkit._ui.qt.window
    ~~~~~~~~~~~~~~~~~~~~~~

    
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QVBoxLayout

from grailkit.util import OS_MAC
import grailkit.experimental._ui.abstract as abstract

# Define Qt constant as PyQt doesn't have it
QWIDGETSIZE_MAX = 16777215


class Window(abstract.Window):
    """Window"""

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

        flags = Qt.Window

        if style == Window.WINDOW_STYLE_BORDERLESS:
            flags = (Qt.Dialog if OS_MAC else Qt.Tool) | Qt.FramelessWindowHint | \
                    Qt.WindowSystemMenuHint | Qt.WindowStaysOnTopHint
        elif style == Window.WINDOW_STYLE_DIALOG:
            flags = Qt.Dialog
        elif style == Window.WINDOW_STYLE_TOOL:
            flags = Qt.Tool

        # create Qt instance
        self._qt_instance = QDialog(None, flags)

        super(Window, self).__init__(width, height,
                                     caption=caption, style=style, resizable=resizable, visible=visible)

    @property
    def caption(self):
        """Returns windows title string"""

        return str(self._qt_instance.windowTitle())

    def set_caption(self, caption):
        """Set window title

        Args:
            caption (str): window title
        """

        self._qt_instance.setWindowTitle(caption)

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

        return self._qt_instance.width()

    @property
    def height(self):
        """Returns window height"""

        return self._qt_instance.height()

    @property
    def resizable(self):
        """Returns True if window resizable"""

        return True

    def set_resizable(self, flag):
        """Set window as resizable"""

        if flag:
            self._qt_instance.setFixedSize(QWIDGETSIZE_MAX, QWIDGETSIZE_MAX)
        else:
            self._qt_instance.setFixedSize(self.width, self.height)

    @property
    def visible(self):
        """Returns True if window is visible"""

        return self._qt_instance.isVisible()

    def set_visible(self, visible):
        """Show or hide the window

        Args:
            visible (bool): True if visible
        """

        self._qt_instance.setVisible(visible)

    def activate(self):
        """Try to return focus to the window"""

        self._qt_instance.show()
        self._qt_instance.raise_()
        self._qt_instance.setWindowState(self._qt_instance.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self._qt_instance.activateWindow()

    def close(self):
        """Close window"""

        self._qt_instance.close()

    def set_size(self, width, height):
        """Set size of window

        Args:
            width (int, float): window width
            height (int, float): window height
        """

        self._qt_instance.resize(int(width), int(height))

    def set_minimum_size(self, width, height):
        """Set minimum window size

        Args:
            width (int, float): window width
            height (int, float): window height
        """

        self._qt_instance.setMinimumSize(int(width), int(height))

    def set_maximum_size(self, width, height):
        """Set a maximum window size

        Args:
            width (int, float): window width
            height (int, float): window height
        """

        self._qt_instance.setMaximumSize(int(width), int(height))

    def set_location(self, x, y):
        """Set window location

        Args:
            x (int, float): x coordinate
            y (int, float): y coordinate
        """

        self._qt_instance.move(int(x), int(y))

    def set_component(self, component):
        """Set given component as main window component

        Args:
            component (grailkit.ui.Component): component that will take place in window
        """

        layout = QVBoxLayout()
        layout.addWidget(component._qt_instance)

        self._qt_instance.setLayout(layout)

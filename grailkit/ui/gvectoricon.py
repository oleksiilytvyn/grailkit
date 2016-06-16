# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gvectoricon
    ~~~~~~~~~~~~~~~~~~~~~~~

    Like regular QIcon but vector + extended functionality
"""

from PyQt5.QtGui import QIcon

from grailkit.ui import GWidget


class GVectorIcon(QIcon, GWidget):

    def __init__(self, parent=None):
        super(GVectorIcon, self).__init__(parent)

        self._color = None

    def color(self):
        """Get icon color"""
        return self._color

    def setColor(self, color):
        """Set icon color"""
        self._color = color

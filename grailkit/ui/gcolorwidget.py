# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gcolorwidget
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Simple color picker widget with multiple color schemes
"""

from grailkit.ui import GWidget


class GColorWidget(GWidget):

    RGB = 0
    HSL = 1
    CMYK = 2

    def __init__(self, parent=None):
        super(GColorWidget, self).__init__(parent)

    def paintEvent(self, event):
        pass

    def setModel(self, model):
        pass

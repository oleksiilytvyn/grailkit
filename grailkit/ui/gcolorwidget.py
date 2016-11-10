# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gcolorwidget
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Simple color picker widget with multiple color schemes
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.ui import GWidget


class GColorWidget(GWidget):

    RGB = 0
    HSL = 1
    CMYK = 2

    def __init__(self, parent=None, color=None):
        super(GColorWidget, self).__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):

        width = self.size().width()
        height = self.size().height()

        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setBrush(Qt.red)
        p.drawRect(0, 0, width, height)

        p.end()

    def mouseMoveEvent(self, event):
        pass

    def mousePressEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

    def sizeHint(self):
        return QSize(40, 40)

    def setModel(self, model):
        pass

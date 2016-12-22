# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gcolorwidget
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Simple color picker widget
"""
import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.ui import GWidget


class GColorWidget(GWidget):

    color_changed = pyqtSignal("QColor")

    def __init__(self, color=QColor('black'), parent=None):
        super(GColorWidget, self).__init__(parent)

        self._mouse_x = 0
        self._mouse_y = 0
        self._color = color
        self._image = QImage(':/gk/widgets/colorwheel.png')

        self.setMinimumSize(QSize(128, 128))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def paintEvent(self, event):

        width = self.size().width()
        height = self.size().height()
        size = min(width, height) - 2

        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.drawImage(QRect(width / 2 - size / 2, height / 2 - size / 2, size, size), self._image)

        p.setBrush(QColor('black'))
        p.drawEllipse(width / 2 + self._mouse_x*size - 3, height / 2 + self._mouse_y*size - 3, 6, 6)

        p.end()

    def eventFilter(self, obj, event):

        return False

    def _mouse_pos(self, x, y):

        width = self.width()
        height = self.height()
        size = min(width, height)
        cx = width / 2
        cy = height / 2
        _x = x - cx
        _y = y - cy
        r = size / 2
        phi = math.atan2(_y, _x)

        if _x ** 2 + _y ** 2 > r**2:
            _x = r * math.cos(phi)
            _y = r * math.sin(phi)

        hue = (math.pi + math.atan2(self._mouse_y, self._mouse_x)) / (math.pi * 2)
        saturation = math.sqrt(self._mouse_x ** 2 + self._mouse_y ** 2)
        lightness = 0.5
        alpha = 1
        color = QColor.fromHslF(hue, saturation, lightness, alpha)
        self.color_changed.emit(color)

        return [_x / size, _y / size]

    def mouseMoveEvent(self, event):

        self._mouse_x, self._mouse_y = self._mouse_pos(event.pos().x(), event.pos().y())

        self.update()

    def mousePressEvent(self, event):

        self._mouse_x, self._mouse_y = self._mouse_pos(event.pos().x(), event.pos().y())

        self.update()

    def mouseReleaseEvent(self, event):

        self._mouse_x, self._mouse_y = self._mouse_pos(event.pos().x(), event.pos().y())

        self.update()

    def sizeHint(self):

        return QSize(100, 100)

# -*- coding: UTF-8 -*-
"""
    grailkit.qt.gtransformwidget
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A simple transformation widget

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""

import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.qt import GWidget


class GTransformWidget(GWidget):
    """Transformation widget"""

    updated = pyqtSignal(object)

    def __init__(self, parent=None):

        super(GTransformWidget, self).__init__(parent)

        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self._ui_menu = QMenu("Coverage", self)

        self._ui_whole_action = QAction('Whole area', self._ui_menu)
        self._ui_whole_action.triggered.connect(self.fillWhole)

        self._ui_left_action = QAction('Left side', self._ui_menu)
        self._ui_left_action.triggered.connect(self.fillLeft)

        self._ui_right_action = QAction('Right side', self._ui_menu)
        self._ui_right_action.triggered.connect(self.fillRight)

        self._ui_center_action = QAction('Center', self._ui_menu)
        self._ui_center_action.triggered.connect(self.center)

        self._ui_menu.addAction(self._ui_left_action)
        self._ui_menu.addAction(self._ui_right_action)
        self._ui_menu.addAction(self._ui_whole_action)
        self._ui_menu.addSeparator()
        self._ui_menu.addAction(self._ui_center_action)

        self._rect = QRect(0, 0, 100, 100)
        self._points = [
            QPointF(0, 0),
            QPointF(0, 0),
            QPointF(0, 0),
            QPointF(0, 0)]
        self.fillWhole()

        self._mouse_x = 0
        self._mouse_y = 0
        self._mouse_hold = False
        self._mouse_hold_x = 0
        self._mouse_hold_y = 0

        self._x = 0
        self._y = 0
        self._scale = 1
        self._point_index = -1

        self._font = QFont("decorative", 14)
        self._text = ""

    def contextMenu(self, event):
        """Process context menu request"""

        self._ui_menu.exec_(self.mapToGlobal(event))

    def paintEvent(self, event):
        """Paint widget controls"""

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        painter.fillRect(event.rect(), QColor("#626364"))

        rect = event.rect()
        scale = min(rect.width() / self._rect.width(), rect.height() / self._rect.height()) * 0.9

        w = self._rect.width() * scale
        h = self._rect.height() * scale

        x = (rect.width() - w) / 2
        y = (rect.height() - h) / 2

        self._x = x
        self._y = y
        self._scale = scale

        painter.fillRect(QRect(x, y, w, h), QColor("#000000"))

        painter.setPen(QColor("#d6d6d6"))
        painter.setBrush(QColor("#111111"))

        points = []

        for point in self._points:
            points.append(self.mapToWidget(point))

        painter.drawPolygon(QPolygonF(points))
        painter.setPen(QColor("#8a9fbb"))
        painter.setBrush(QColor("#8a9fbb"))

        for point in points:
            painter.drawEllipse(point, 4, 4)

        painter.setPen(QColor("#e6e6e6"))
        painter.setFont(self._font)
        painter.drawText(event.rect(), Qt.AlignCenter | Qt.TextWordWrap, self._text)

        painter.end()

    def mousePressEvent(self, event):
        """Process mouse press event"""

        self._mouse_hold = True
        index = 0

        for point in self._points:
            point = self.mapToWidget(point)

            if math.sqrt(pow(point.x() - event.x(), 2) + pow(point.y() - event.y(), 2)) <= 5:
                self._point_index = index
                self._mouse_hold_x = event.x() - point.x()
                self._mouse_hold_y = event.y() - point.y()

            index += 1

    def mouseReleaseEvent(self, event):
        """Process mouse release event"""

        self._mouse_hold = False
        self._point_index = -1

    def mouseMoveEvent(self, event):
        """Process mouse move event"""

        self._mouse_x = event.x()
        self._mouse_y = event.y()

        if self._point_index >= 0:
            point = self.mapToScreen(QPointF(event.x() - self._x, event.y() - self._y))

            self._text = "(%d, %d)" % (point.x(), point.y())
            self._points[self._point_index] = point

            self.updated.emit(self.transformation())
        else:
            self._text = ""

        self.update()

    def mapToWidget(self, point):
        """Returns point mapped to widget coordinates

        Args:
            point (QPoint, QPointF): original point to be mapped
        """

        return QPointF(self._x + self._scale * point.x(), self._y + self._scale * point.y())

    def mapToScreen(self, point):
        """Returns point mapped to screen coordinates

        Args:
            point (QPoint, QPointF): original point to be mapped
        """

        return QPointF(point.x() * (1 / self._scale), point.y() * (1 / self._scale))

    def center(self):
        """Move transformation to center"""

        w = self._rect.width()
        h = self._rect.height()

        minx = w
        miny = h
        maxx = 0
        maxy = 0

        for point in self._points:
            if point.x() < minx:
                minx = point.x()

            if point.y() < miny:
                miny = point.y()

            if point.x() > maxx:
                maxx = point.x()

            if point.y() > maxy:
                maxy = point.y()

        x = w / 2 - (maxx - minx) / 2
        y = h / 2 - (maxy - miny) / 2

        index = 0

        for point in self._points:
            point.setX(point.x() - minx + x)
            point.setY(point.y() - miny + y)

            self._points[index] = point
            index += 1

        self.updated.emit(self.transformation())
        self.update()

    def fillWhole(self):
        """Fill whole screen"""

        w = self._rect.width()
        h = self._rect.height()

        self._points[0] = QPointF(0, 0)
        self._points[1] = QPointF(w, 0)
        self._points[2] = QPointF(w, h)
        self._points[3] = QPointF(0, h)

        self.updated.emit(self.transformation())
        self.update()

    def fillLeft(self):
        """Fill left side of the screen"""

        w = self._rect.width()
        h = self._rect.height()

        self._points[0] = QPointF(0, 0)
        self._points[1] = QPointF(w / 2, 0)
        self._points[2] = QPointF(w / 2, h)
        self._points[3] = QPointF(0, h)

        self.updated.emit(self.transformation())
        self.update()

    def fillRight(self):
        """Fill right side"""

        w = self._rect.width()
        h = self._rect.height()

        self._points[0] = QPointF(w / 2, 0)
        self._points[1] = QPointF(w, 0)
        self._points[2] = QPointF(w, h)
        self._points[3] = QPointF(w / 2, h)

        self.updated.emit(self.transformation())
        self.update()

    def setArea(self, rect):
        """Set original rectangle of transform

        Args:
            rect (QRect):
        """

        self._rect = rect
        self.fillWhole()

    def area(self):
        """Returns original area"""

        return self._rect

    def points(self):
        """Returns list of QPoint"""

        return self._points

    def transformation(self):
        """Returns a QTransform object"""

        t = QTransform()
        p = []
        q = [QPointF(0, 0),
             QPointF(self._rect.width(), 0),
             QPointF(self._rect.width(), self._rect.height()),
             QPointF(0, self._rect.height())]

        for o in self._points:
            p.append(QPointF(o.x(), o.y()))

        QTransform.quadToQuad(QPolygonF(q), QPolygonF(p), t)

        return t

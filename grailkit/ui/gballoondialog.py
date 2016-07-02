# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gballoondialog
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Floating dialog with pointer and without title bar
"""

from PyQt5.QtCore import Qt, QPointF, QSize, QEvent, QObject
from PyQt5.QtGui import QPolygonF, QColor, QPainter, QPainterPath, QBrush
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from grailkit.ui import GDialog
from grailkit.util import OS_MAC


class GBalloonDialog(GDialog):
    """Dialog without title bar and frame, but with rounded corners and pointing triangle"""

    def __init__(self, parent=None):
        super(GBalloonDialog, self).__init__(parent)

        self._close_on_focus_lost = True
        self._background_color = QColor(255, 255, 255)

        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.installEventFilter(self)

        if not OS_MAC:
            effect = QGraphicsDropShadowEffect()
            effect.setBlurRadius(12)
            effect.setColor(QColor(0, 0, 0, 126))
            effect.setOffset(0)

            self.setGraphicsEffect(effect)

        self.setContentsMargins(12, 12, 12, 19)

    def paintEvent(self, event):
        """Paint a dialog"""

        # corner radius
        roundness = 5
        # pointing triangle size
        side = 5

        painter = QPainter()
        painter.begin(self)
        painter.save()

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 0, 0, 127))

        points = [QPointF(self.width() / 2, self.height() - 12),
                  QPointF(self.width() / 2 - side, self.height() - side - 12),
                  QPointF(self.width() / 2 + side, self.height() - side - 12)]
        triangle = QPolygonF(points)

        rounded_rect = QPainterPath()
        rounded_rect.addRoundedRect(12, 12, self.width() - 24, self.height() - side - 24, roundness, roundness)
        rounded_rect.addPolygon(triangle)

        painter.setOpacity(1)
        painter.fillPath(rounded_rect, QBrush(self._background_color))

        painter.restore()
        painter.end()

    def eventFilter(self, target, event):
        """Close dialog when focus is lost"""

        if self._close_on_focus_lost and event.type() == QEvent.WindowDeactivate:
            self.hide()

        return QObject.eventFilter(self, target, event)

    def sizeHint(self):
        """Default minimum size"""

        return QSize(300, 300)

    def closeOnFocusLost(self, value):
        """Close dialog when it looses focus

        Args:
            value (bool): close this dialog when it looses focus or not
        """

        self._close_on_focus_lost = value

    def showAt(self, point):
        """Show dialog tip at given point

        Args:
            point (QPoint): point to show at
        """

        self.show()
        self.raise_()
        self.move(point.x() - self.width() / 2, point.y() - self.height() + 12)

    def setBackgroundColor(self, color):
        """Set a color of whole dialog

        Args:
            color (QColor): background color of widget
        """

        self._background_color = color


# test a dialog
if __name__ == '__main__':

    import sys
    from grailkit.ui import GApplication

    app = GApplication(sys.argv)

    win = GBalloonDialog()
    win.closeOnFocusLost(False)
    win.setBackgroundColor(QColor(72, 74, 81))
    win.show()

    sys.exit(app.exec_())
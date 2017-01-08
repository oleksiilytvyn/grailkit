# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gcolorindicator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Widget that simply shows color
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.qt import GWidget


class GColorIndicator(GWidget):

    def __init__(self, color=QColor('black'), parent=None):
        super(GColorIndicator, self).__init__(parent)

        self._color = None
        self.setColor(color)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(10, 10)

    def paintEvent(self, event):
        """Draw widget"""

        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(QRectF(1, 1, self.width()-2, self.height()-2), 5, 5)
        p.setPen(QColor('#666'))
        p.fillPath(path, self._color)
        p.drawPath(path)

        p.end()

    def setColor(self, color):
        """Set color of widget

        Args:
            color (QColor): color of widget
        """

        self._color = color

    def color(self):
        """Get current color"""

        return self._color


if __name__ == "__main__":

    import sys
    from grailkit.qt import GApplication, GDialog

    app = GApplication(sys.argv)
    indicator = GColorIndicator(QColor('cyan'))

    layout = QHBoxLayout()
    layout.addWidget(indicator)

    win = GDialog()
    win.setLayout(layout)
    win.setStyleSheet("GDialog {background: #2f2f2f;}")
    win.setGeometry(300, 300, 200, 200)
    win.show()

    sys.exit(app.exec_())

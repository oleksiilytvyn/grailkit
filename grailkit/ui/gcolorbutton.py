# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gcolorbutton
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Button with color display
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GColorButton(QPushButton):

    color_changed = pyqtSignal()

    def __init__(self, parent=None, color=QColor(255, 0, 0)):
        super(GColorButton, self).__init__(parent)

        self._color = None
        self.setColor(color)

    def paintEvent(self, event):
        """Draw widget"""

        width = self.size().width()
        height = self.size().height()

        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)

        padding = 2
        path = QPainterPath()
        path.addRoundedRect(QRectF(padding, padding, width - padding * 2, height - padding * 2), 3, 3)

        p.fillPath(path, self._color)
        p.drawPath(path)

        p.setPen(Qt.green)
        p.drawText(self.rect(), 0, self.text())

        p.end()

    def setColor(self, color):
        """Set color of button"""

        if not isinstance(color, QColor):
            raise Exception("Type of given argument isn't a QColor")

        self._color = color
        self.color_changed.emit()

    def color(self):
        """Get a color of button"""

        return self._color

if __name__ == "__main__":

    import sys
    from grailkit.ui import GApplication, GDialog

    app = GApplication(sys.argv)

    button = GColorButton()

    layout = QHBoxLayout()
    layout.addWidget(button)

    win = GDialog()
    win.setLayout(layout)
    win.setStyleSheet("GDialog {background: #2f2f2f;}")
    win.show()

    sys.exit(app.exec_())

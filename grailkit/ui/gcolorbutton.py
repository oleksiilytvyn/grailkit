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

    def __init__(self, text="", color=QColor(255, 0, 0), parent=None):
        super(GColorButton, self).__init__(text, parent)

        self._color = None
        self.setColor(color)

    def setColor(self, color):
        """Set color of button

        Args:
            color (QColor): color of icon
        """

        if not isinstance(color, QColor):
            raise Exception("Type of given argument isn't a QColor")

        self._color = color
        self.setIcon(QIcon(self._pixmap()))
        self.color_changed.emit()

    def color(self):
        """Get a color of button"""

        return self._color

    def _pixmap(self):
        """Generate pixmap for button"""

        size = 32
        pix = QPixmap(size, size)
        pix.fill(Qt.transparent)

        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)

        pen_color = QColor("black") if self._color.lightness() >= 64 else QColor("white")

        p.setPen(QPen(pen_color))
        p.setBrush(QBrush(self._color))
        p.drawEllipse(1, 1, size-2, size-2)
        p.end()

        return pix

if __name__ == "__main__":

    import sys
    from grailkit.ui import GApplication, GDialog

    app = GApplication(sys.argv)
    button = GColorButton("Pick Color")

    def change_color():
        color = QColorDialog.getColor(button.color())
        button.setColor(color)

    button.clicked.connect(change_color)

    layout = QHBoxLayout()
    layout.addWidget(button)

    win = GDialog()
    win.setLayout(layout)
    win.setStyleSheet("GDialog {background: #2f2f2f;}")
    win.show()

    sys.exit(app.exec_())

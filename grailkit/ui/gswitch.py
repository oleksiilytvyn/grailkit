# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gswitch
    ~~~~~~~~~~~~~~~~~~~

    Simple two state switch widget
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.ui import GWidget


class GSwitch(QAbstractButton, GWidget):
    """Simple two state switch widget"""

    state_changed = pyqtSignal(bool)

    def __init__(self, parent=None, state=True):
        super(GSwitch, self).__init__(parent)

        self._state = state
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

    def paintEvent(self, event):
        """Draw a widget"""

        width = self.size().width()
        height = self.size().height()

        on_color = QColor()
        on_color.setNamedColor("#8a9fbd")
        off_color = QColor()
        off_color.setNamedColor("#676869")
        switch_color = QColor()
        switch_color.setNamedColor("#2f2f2f")

        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(QRectF(1, 1, width - 2, height - 2), 3, 3)

        flag_path = QPainterPath()

        pen_color = QColor()
        pen_color.setNamedColor("#444444")

        pen = QPen()
        pen.setWidth(1)
        pen.setColor(pen_color)
        p.setPen(pen)

        if self._state:
            p.fillPath(path, on_color)
            flag_path.addRoundedRect(QRectF(width / 2, 3, width / 2 - 3, height - 6), 3, 3)
        else:
            p.fillPath(path, off_color)
            flag_path.addRoundedRect(QRectF(3, 3, width /2 - 3, height - 6), 3, 3)

        p.drawPath(path)
        p.fillPath(flag_path, switch_color)

        p.end()

    def mousePressEvent(self, event):
        """React to mouse click"""

        self._state = not self._state
        self.state_changed.emit(self._state)

    def sizeHint(self):
        """Resize rule"""

        return QSize(52, 22)

    def setState(self, state):
        """Set state of switch"""

        self._state = state

    def state(self):
        """Get state of switch"""

        return self._state


if __name__ == "__main__":

    import sys
    from grailkit.ui import GApplication, GDialog

    app = GApplication(sys.argv)

    switch = GSwitch()
    label = QLabel("Press the switch")

    layout = QHBoxLayout()
    layout.addWidget(label)
    layout.addWidget(switch)

    win = GDialog()
    win.setLayout(layout)
    win.setStyleSheet("GDialog {background: #2f2f2f;}QLabel {color: #e6e6e6;}")
    win.show()

    sys.exit(app.exec_())

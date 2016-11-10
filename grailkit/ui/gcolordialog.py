# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gcolordialog
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Color picker dialog
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.ui import GDialog, GColorWidget


class GColorDialog(GDialog):

    def __init__(self, parent=None, color=QColor(0, 0, 0)):
        super(GColorDialog, self).__init__(parent)

        self._color = color

        self.__ui__()

    def __ui__(self):
        self._widget = GColorWidget(None, self._color)

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addWidget(self._widget)

        self.setLayout(self._layout)


if __name__ == "__main__":

    import sys
    from grailkit.ui import GApplication

    app = GApplication(sys.argv)

    win = GColorDialog()
    win.show()

    sys.exit(app.exec_())

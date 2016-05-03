# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gframeless
    ~~~~~~~~~~~~~~~~~~~~~~

    Frameless dialog implementation
"""
import sys

from PyQt5.QtCore import Qt

from grailkit.ui import GDialog
from grailkit.util import OS_MAC


class GFrameless(GDialog):
    """Frameless dialog that stays on top and not shown in menu bar"""

    def __init__(self, parent=None):
        super(GFrameless, self).__init__(parent)

        # set a widget background
        self.setStyleSheet("background-color: #000000;")

        # set window flags
        self.setWindowFlags((Qt.Dialog if OS_MAC else Qt.Tool) |
                            Qt.FramelessWindowHint |
                            Qt.WindowSystemMenuHint |
                            Qt.WindowStaysOnTopHint)

# test a dialog
if __name__ == '__main__':
    from grailkit.ui import GApplication

    app = GApplication(sys.argv)
    win = GFrameless()
    win.setGeometry(100, 100, 200, 200)
    win.show()

    sys.exit(app.exec_())

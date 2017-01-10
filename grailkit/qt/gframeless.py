# -*- coding: UTF-8 -*-
"""
    grailkit.qt.gframeless
    ~~~~~~~~~~~~~~~~~~~~~~

    Frameless dialog implementation
"""
from PyQt5.QtCore import Qt

from grailkit.qt import GDialog
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

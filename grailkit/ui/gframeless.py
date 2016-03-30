# -*- coding: UTF-8 -*-

from PyQt5.QtCore import Qt


from grailkit.ui import GDialog
from grailkit import util


class GFrameless(GDialog):
    """Frameless dialog"""

    def __init__(self, parent=None):
        super(GFrameless, self).__init__(parent)

        self.setWindowFlags((Qt.Dialog if util.OS_MAC else Qt.Tool) |
                            Qt.FramelessWindowHint |
                            Qt.WindowSystemMenuHint |
                            Qt.WindowStaysOnTopHint)

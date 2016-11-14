# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gdialog
    ~~~~~~~~~~~~~~~~~~~

    Base class for all Grail Kit UI dialogs
"""
from PyQt5.QtWidgets import QDialog, QDesktopWidget

from grailkit.ui import GWidget


class GDialog(QDialog, GWidget):
    """Abstract dialog window"""

    def __init__(self, parent=None):
        super(GDialog, self).__init__(parent)

    def moveToCenter(self):
        """Move window to the center of current screen"""

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        self.move(qr.topLeft())

# -*- coding: UTF-8 -*-
"""
    grailkit.qt.gdialog
    ~~~~~~~~~~~~~~~~~~~

    Base class for all Grail Kit UI dialogs
"""
from PyQt5.QtWidgets import QDialog, QDesktopWidget

from grailkit.qt import GWidget


class GDialog(QDialog, GWidget):
    """Abstract dialog window"""

    def __init__(self, parent=None):
        super(GDialog, self).__init__(parent)

    def moveToCenter(self):
        """Move window to the center of current screen"""

        geometry = self.frameGeometry()
        geometry.moveCenter(QDesktopWidget().availableGeometry().center())

        self.move(geometry.topLeft())

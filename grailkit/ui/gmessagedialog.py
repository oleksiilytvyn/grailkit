# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gmessagedialog
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Replecement for default OS message dialog
"""
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.ui import GDialog


class GMessageDialog(GDialog):
    """Message dialog, replacement of a default dialog"""

    def __init__(self, parent=None):
        super(GMessageDialog, self).__init__(parent)

    def _init_ui(self):
        pass


# test a dialog
if __name__ == '__main__':
    from grailkit.ui import GApplication

    app = GApplication(sys.argv)
    win = GMessageDialog()
    win.show()

    sys.exit(app.exec_())

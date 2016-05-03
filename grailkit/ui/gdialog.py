# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gdialog
    ~~~~~~~~~~~~~~~~~~~

    Base class for all Grail Kit UI dialogs
"""
from PyQt5.QtWidgets import QDialog

from grailkit.ui import GWidget


class GDialog(QDialog, GWidget):
    """Dialog window"""

    pass


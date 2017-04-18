# -*- coding: UTF-8 -*-
"""
    grailkit.qt.button
    ~~~~~~~~~~~~~~~~~~

    
"""

from PyQt5.QtWidgets import QAbstractButton


class Button(QAbstractButton):
    """Basic button widget"""

    def __init__(self, parent=None):
        super(Button, self).__init__(parent)

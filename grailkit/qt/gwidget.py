# -*- coding: UTF-8 -*-
"""
    grailkit.qt.gwidget
    ~~~~~~~~~~~~~~~~~~~

    Base widget for all Grail Kit Qt components
"""
from PyQt5.QtWidgets import QWidget


class GWidget(QWidget):
    """Base widget"""

    def className(self):
        """
        Returns widget name that used in stylesheet.

        stylesheet example:
            GDialog {
                background: red;
            }
        """

        return type(self).__name__

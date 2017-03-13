# -*- coding: UTF-8 -*-
"""
    grailkit.qt.gwidget
    ~~~~~~~~~~~~~~~~~~~

    Base widget for all Grail Kit Qt components

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
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

# -*- coding: UTF-8 -*-
"""
    grailkit.qt.line_edit
    ~~~~~~~~~~~~~~~~~~~~~

    Line edit

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit

from grailkit.qt import Component


class LineEdit(QLineEdit, Component):
    """Line edit widget"""

    def __init__(self, *args, **kwargs):
        super(LineEdit, self).__init__(*args, **kwargs)

        self.setAttribute(Qt.WA_MacShowFocusRect, False)

# -*- coding: UTF-8 -*-
"""
    grailkit.qt.button
    ~~~~~~~~~~~~~~~~~~

    Button component

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""

from PyQt5.QtWidgets import QPushButton

from grailkit.qt import Component


class Button(QPushButton, Component):
    """Basic button widget"""

    def __init__(self, *args):
        super(Button, self).__init__(*args)

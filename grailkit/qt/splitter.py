# -*- coding: UTF-8 -*-
"""
    grailkit.qt.splitter
    ~~~~~~~~~~~~~~~~~~~~

    Splitter component

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from PyQt5.QtWidgets import QSplitter
from grailkit.qt import Component


class Splitter(QSplitter, Component):
    """Splitter component"""

    def __init__(self, *args):
        super(Splitter, self).__init__(*args)

        self.setHandleWidth(1)
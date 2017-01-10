# -*- coding: UTF-8 -*-
"""
    grailkit.qt.gspacer
    ~~~~~~~~~~~~~~~~~~~

    Transparent widget that only task to stretch components and fill space
"""

from PyQt5.QtWidgets import QSizePolicy

from grailkit.qt import GWidget


class GSpacer(GWidget):
    """Widget that simply allocate space and spread widgets"""

    def __init__(self, policy_horizontal=QSizePolicy.Expanding, policy_vertical=QSizePolicy.Expanding, parent=None):
        super(GSpacer, self).__init__(parent)

        self.setSizePolicy(policy_horizontal, policy_vertical)

# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gspacer
    ~~~~~~~~~~~~~~~~~~~

    Transparent widget that only task to stretch components and fill space
"""

from PyQt5.QtWidgets import QSizePolicy

from grailkit.ui import GWidget


class GSpacer(GWidget):

    def __init__(self, policy_horizontal=QSizePolicy.Expanding, policy_vetrical=QSizePolicy.Expanding, parent=None):
        super(GSpacer, self).__init__(parent)

        self.setSizePolicy(policy_horizontal, policy_vetrical)

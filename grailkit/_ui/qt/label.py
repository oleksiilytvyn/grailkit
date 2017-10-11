# -*- coding: UTF-8 -*-
"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""
from PyQt5.QtWidgets import QLabel

import grailkit._ui.abstract as abstract
from .component import Component


class Label(abstract.Label, Component):
    """Basic label component"""

    def __init__(self, text=""):
        super(Label, self).__init__()

        self._qt_instance = QLabel(text)

# -*- coding: UTF-8 -*-
"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""
from PyQt5.QtWidgets import QLayout, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget
import grailkit._ui.abstract as abstract
from .component import Component


class Layout(abstract.Layout, Component):

    def __init__(self):
        super(Layout, self).__init__()

    def append(self, item):

        self._qt_layout.addWidget(item._qt_instance)


class HLayout(abstract.HLayout, Layout):

    def __init__(self):
        super(HLayout, self).__init__()


class VLayout(abstract.VLayout, Layout):

    def __init__(self):
        super(VLayout, self).__init__()

        self._qt_layout = QVBoxLayout()
        self._qt_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_layout.setSpacing(0)

        self._qt_instance = QWidget()
        self._qt_instance.setLayout(self._qt_layout)

    def append(self, item):

        self._qt_layout.addWidget(item._qt_instance)


class GridLayout(abstract.GridLayout, Layout):

    pass

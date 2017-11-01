# -*- coding: UTF-8 -*-
"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""
from PyQt5.QtWidgets import QLayout, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget
import grailkit.experimental._ui.abstract as abstract
from .component import Component


class Layout(abstract.Layout, Component):

    def __init__(self):
        super(Layout, self).__init__()


class BoxLayout(abstract.BoxLayout, Layout):

    def __init__(self):
        super(BoxLayout, self).__init__()

        if not self._qt_layout:
            self._qt_layout = QHBoxLayout()

        self._qt_layout.setContentsMargins(0, 0, 0, 0)
        self._qt_layout.setSpacing(0)

        self._qt_instance = QWidget()
        self._qt_instance.setLayout(self._qt_layout)

    def __len__(self):
        """Returns number of components in layout"""

        return self._qt_layout.count()

    def append(self, component):
        """Append component to the layout"""

        self._qt_layout.addWidget(component._qt_instance)

    def insert(self, index, component):
        """Insert component at given position"""

        self._qt_layout.insertWidget(index, component._qt_instance)

    def remove(self, component):
        """Remove component from layout"""

        for index in range(self._qt_layout.count()):
            item = self._qt_layout.itemAt(index)

            if component._qt_instance == item:
                self._qt_layout.takeAt(index)

    def set_spacing(self, spacing):
        """Set spacing between components in layout

        Args:
            spacing (int): space between components in pixels
        """

        self._qt_layout.setSpacing(spacing)

    def set_margins(self, left, top, right, bottom):
        """Set layout margins

        Args:
            left (int): left padding
            top (int): top padding
            right (int): right padding
            bottom (int): bottom padding
        """

        self._qt_layout.setContentsMargins(left, top, right, bottom)


class HLayout(abstract.HLayout, BoxLayout):

    def __init__(self):

        self._qt_layout = QHBoxLayout()
        super(HLayout, self).__init__()


class VLayout(abstract.VLayout, BoxLayout):

    def __init__(self):

        self._qt_layout = QVBoxLayout()
        super(VLayout, self).__init__()


class GridLayout(abstract.GridLayout, Layout):

    def __init__(self):
        super(GridLayout, self).__init__()

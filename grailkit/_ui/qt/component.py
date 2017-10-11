# -*- coding: UTF-8 -*-
"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from .object import Object


class Component(Object):
    """Empty component"""

    def __init__(self):
        super(Component, self).__init__()

        self._qt_instance = QWidget()

    @property
    def width(self):
        """Returns component width"""

        return self._qt_instance.width()

    @property
    def height(self):
        """Returns component height"""

        return self._qt_instance.height()

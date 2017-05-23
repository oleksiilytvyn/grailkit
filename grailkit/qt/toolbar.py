# -*- coding: UTF-8 -*-
"""
    grailkit.qt.toolbar
    ~~~~~~~~~~~~~~~~~~~

    Toolbar component

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from grailkit.qt import Component, HLayout, Spacer


class Toolbar(Component):
    """Toolbar component"""

    def __init__(self, parent=None):
        super(Toolbar, self).__init__(parent)

        self._layout = HLayout()
        self._layout.setSpacing(8)
        self._layout.setContentsMargins(8, 2, 8, 2)

        self.setMaximumHeight(36)
        self.setMinimumHeight(36)

        self.setLayout(self._layout)

    def addAction(self, action):
        pass

    def addSeparator(self):
        """Add separator to the toolbar"""

        self.addWidget(ToolbarSeparator())

    def addStretch(self):
        """Add space stretch"""

        self.addWidget(Spacer())

    def addWidget(self, component):
        """Add widget to the toolbar

        Args:
            component (Component): component widget
        """

        self._layout.addWidget(component)


class ToolbarSeparator(Component):

    pass

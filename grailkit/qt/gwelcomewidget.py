# -*- coding: UTF-8 -*-
"""
    grailkit.qt.gwelcomewidget
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements widget for welcome screen with title, description and list of actions
    for user to choose from.

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QSizePolicy

from grailkit.qt import GWidget, GWelcomeAction
from grailkit.qt.gapplication import AppInstance


class GWelcomeWidget(GWidget):
    """Widget with title, icon and actions below"""

    def __init__(self, title="", description="", icon=None, parent=None):
        super(GWelcomeWidget, self).__init__(parent)

        # fix stylesheet issues
        self.setStyleSheet(AppInstance()._get_stylesheet())

        self._icon = None
        self.__ui__()

        if icon:
            self.setIcon(icon)
            self.setIconVisible(True)
        else:
            self.setIconVisible(False)

        self.setTitle(title)
        self.setDescription(description)

    def __ui__(self):
        """Create ui"""

        self._ui_icon = QLabel(self)
        self._ui_icon.setAlignment(Qt.AlignCenter)
        self._ui_icon.setGeometry(0, 0, 64, 64)

        self._ui_title = QLabel("Welcome")
        self._ui_title.setObjectName("g_welcome_title")
        self._ui_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._ui_description = QLabel("Choose some action below")
        self._ui_description.setObjectName("g_welcome_description")
        self._ui_description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._ui_actions_layout = QVBoxLayout()
        self._ui_actions_layout.setSpacing(14)
        self._ui_actions_layout.setContentsMargins(0, 0, 0, 0)

        self._ui_actions = QWidget()
        self._ui_actions.setContentsMargins(50, 0, 50, 0)
        self._ui_actions.setLayout(self._ui_actions_layout)

        self._ui_layout = QVBoxLayout()
        self._ui_layout.setSpacing(0)
        self._ui_layout.setContentsMargins(0, 0, 0, 0)

        self._ui_layout.addStretch(1)
        self._ui_layout.addWidget(self._ui_icon)
        self._ui_layout.addSpacing(12)
        self._ui_layout.addWidget(self._ui_title)
        self._ui_layout.addWidget(self._ui_description)
        self._ui_layout.addWidget(self._ui_actions)
        self._ui_layout.addStretch(1)

        self.setLayout(self._ui_layout)

    def addWidget(self, widget):
        """Add action to list

        Args:
            widget (GWelcomeAction): action to be added
        """

        self._ui_actions_layout.addWidget(widget)

    def setTitle(self, title):
        """Set widget title

        Args:
            title (str): title text
        """

        self._ui_title.setText(title)

    def setDescription(self, text):
        """Set widget description

        Args:
            text (str): description text
        """

        self._ui_description.setText(text)

    def setIcon(self, icon):
        """Set icon of widget

        Args:
            icon (QIcon, QPixmap): icon of widget
        """

        size = 128

        if isinstance(icon, QIcon):
            self._icon = icon.pixmap(size)

        if isinstance(icon, QPixmap):
            self._icon = icon.scaledToWidth(size)

        self._ui_icon.setPixmap(self._icon)

    def setIconVisible(self, flag):
        """Make icon visible or not

        Args:
            flag (bool): True if it visible
        """

        if flag:
            self._ui_icon.show()
        else:
            self._ui_icon.hide()

    def resizeEvent(self, event):
        """Align widgets"""

        super(GWelcomeWidget, self).resizeEvent(event)

        width = self.size().width()

        if width <= 300:
            padding = 50
        elif width >= 600:
            padding = (width - 350) * 0.5
        else:
            padding = width * 0.2

        self._ui_actions.setContentsMargins(padding, 0, padding, 0)

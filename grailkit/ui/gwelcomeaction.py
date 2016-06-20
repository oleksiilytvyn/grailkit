# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gwelcomeaction
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Action button widget for GWelcomeWidget
"""

from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QAbstractButton, QLabel, QVBoxLayout

from grailkit.ui import GWidget


class GWelcomeAction(QAbstractButton, GWidget):

    def __init__(self, title="Action", text="Take some action", icon=None, parent=None):
        super(GWelcomeAction, self).__init__(parent)

        self._icon = None
        self._title = title
        self._text = text

        self._ui_title = QLabel(self._title)
        self._ui_title.setObjectName("q_welcome_action_title")

        self._ui_text = QLabel(self._text)
        self._ui_text.setObjectName("q_welcome_action_text")

        self._ui_layout = QVBoxLayout()
        self._ui_layout.setContentsMargins(0, 0, 0, 0)
        self._ui_layout.setSpacing(0)
        self._ui_layout.addStretch(1)
        self._ui_layout.addWidget(self._ui_title)
        self._ui_layout.addWidget(self._ui_text)
        self._ui_layout.addStretch(1)

        self.setIcon(icon)
        self.setText(self._text)

        self.setLayout(self._ui_layout)

    def sizeHint(self):
        """Default size of widget"""

        return QSize(64, 64)

    def paintEvent(self, paint):
        """Custom painting"""

        p = QPainter(self)
        p.save()

        if self._icon:
            p.drawPixmap(QPoint(0, 5), self._icon)

        p.restore()

    def setIcon(self, icon):
        """Set action icon

        Args:
            icon (QIcon, QPixmap): icon of action
        """

        size = 56

        if isinstance(icon, QIcon):
            self._icon = icon.pixmap(size)

        if isinstance(icon, QPixmap):
            self._icon = icon.scaledToWidth(size)

    def setTitle(self, title):
        """Set a title of action

        Args:
            title (str): set a title of action
        """

        self._title = title
        self._ui_title.setText(self._title)

    def setText(self, text):
        """Set a description text of this action

        Args:
            text (str): text of action
        """

        super(GWelcomeAction, self).setText("")

        self._text = text
        self._ui_text.setText(self._text)

    def title(self):
        """Get title of action

        Returns: str
        """

        return self._title

    def text(self):
        """Get a text of action

        Returns: str
        """

        return self._text

    def icon(self):
        """Get a icon of action

        Returns: QIcon
        """

        return QIcon(self._icon)

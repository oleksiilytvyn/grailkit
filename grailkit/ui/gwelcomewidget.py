# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gwelcomewidget
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements widget for welcome screen with title, description and list of actions
    for user to choose from.
"""

from grailkit.ui import GWidget


class GWelcomeWidget(GWidget):

    def __init__(self, parent=None):
        super(GWelcomeWidget, self).__init__(parent)

        self.__ui__()

    def __ui__(self):
        """Create ui"""
        self._ui_title = QLabel()
        self._ui_description = QLabel()

    def addAction(self, action):
        pass

    def resizeEvent(self):
        """Align widgets"""
        pass

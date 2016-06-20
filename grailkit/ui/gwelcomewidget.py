# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gwelcomewidget
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Implements widget for welcome screen with title, description and list of actions
    for user to choose from.
"""

from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QSizePolicy

from grailkit.ui import GWidget, GWelcomeAction


class GWelcomeWidget(GWidget):
    """"""

    def __init__(self, parent=None):
        super(GWelcomeWidget, self).__init__(parent)

        self.__ui__()

    def __ui__(self):
        """Create ui"""

        self._ui_title = QLabel("Welcome")
        self._ui_title.setObjectName("g_welcome_title")
        self._ui_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._ui_description = QLabel("Choose some action below")
        self._ui_description.setObjectName("g_welcome_description")
        self._ui_description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._ui_actions_layout = QVBoxLayout()
        self._ui_actions_layout.setSpacing(2)
        self._ui_actions_layout.setContentsMargins(0, 0, 0, 0)

        self._ui_actions = QWidget()
        self._ui_actions.setContentsMargins(50, 0, 50, 0)
        self._ui_actions.setLayout(self._ui_actions_layout)

        self._ui_layout = QVBoxLayout()
        self._ui_layout.setSpacing(0)
        self._ui_layout.setContentsMargins(0, 0, 0, 0)

        self._ui_layout.addStretch(1)
        self._ui_layout.addWidget(self._ui_title)
        self._ui_layout.addWidget(self._ui_description)
        self._ui_layout.addWidget(self._ui_actions)
        self._ui_layout.addStretch(1)

        self.setLayout(self._ui_layout)

    def addWidget(self, widget):
        """Add action to list"""

        self._ui_actions_layout.addWidget(widget)

    def setTitle(self, title):

        self._ui_title.setText(title)

    def setDescription(self, text):

        self._ui_description.setText(text)

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


# test a widget
if __name__ == '__main__':

    import sys
    from PyQt5.QtWidgets import QHBoxLayout, QApplication, QStyle
    from grailkit.ui import GApplication, GDialog

    app = GApplication(sys.argv)
    win = GDialog()
    win.setGeometry(100, 100, 400, 600)

    widget = GWelcomeWidget()
    widget.setTitle("Welcome to GrailKit 0.1.0")
    widget.setDescription("Choose some action below")

    widget.addWidget(
        GWelcomeAction("Create", "Write a new document", QApplication.style().standardIcon(QStyle.SP_FileIcon)))
    widget.addWidget(GWelcomeAction("Open", "Edit existing one", QApplication.style().standardIcon(QStyle.SP_DirIcon)))
    widget.addWidget(
        GWelcomeAction("Save", "Save current file", QApplication.style().standardIcon(QStyle.SP_DialogSaveButton)))

    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(widget)

    win.setLayout(layout)
    win.setStyleSheet("background: #2f2f2f;")
    win.show()

    sys.exit(app.exec_())

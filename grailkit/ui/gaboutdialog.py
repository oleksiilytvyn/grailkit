# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gaboutdialog
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Generic about dialog window
"""
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.ui import GDialog, GApplication


class GAboutDialog(GDialog):
    """Default about dialog"""

    def __init__(self, parent=None, title="Application", description="version 1.0", icon=None):
        """A basic about dialog"""

        super(GAboutDialog, self).__init__(parent)

        self._title = title
        self._description = description
        self._icon = icon

        self.url_report = ""
        self.url_help = ""

        self._init_ui()

    def _init_ui(self):

        self._ui_pixmap = QApplication.style().standardIcon(QStyle.SP_MessageBoxInformation)

        self._ui_icon = QLabel(self)
        self._ui_icon.setPixmap(self._ui_pixmap.pixmap(64))
        self._ui_icon.setAlignment(Qt.AlignCenter)
        self._ui_icon.setGeometry(48, 52, 64, 64)

        self._ui_title = QLabel(self._title, self)
        self._ui_title.setStyleSheet("font-size: 20pt;")
        self._ui_title.setGeometry(160, 34, 311, 26)

        self._ui_description = QPlainTextEdit(self._description, self)
        self._ui_description.setStyleSheet("background: transparent;")
        self._ui_description.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._ui_description.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._ui_description.setReadOnly(True)
        self._ui_description.setGeometry(156, 74, 311, 88)

        self._ui_btn_help = QPushButton("Help")
        self._ui_btn_help.clicked.connect(self.help)

        self._ui_btn_report = QPushButton("Report a problem")
        self._ui_btn_report.clicked.connect(self.report)

        self.ui_btn_close = QPushButton("Close")
        self.ui_btn_close.setDefault(True)
        self.ui_btn_close.clicked.connect(self.close)

        self._ui_buttons_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self._ui_buttons_layout.addWidget(self._ui_btn_help)
        self._ui_buttons_layout.addStretch()
        self._ui_buttons_layout.addWidget(self._ui_btn_report)
        self._ui_buttons_layout.addWidget(self.ui_btn_close)

        self._ui_buttons = QWidget(self)
        self._ui_buttons.setLayout(self._ui_buttons_layout)
        self._ui_buttons.setGeometry(8, 172, 484 - 16, 50)

        self.setWindowTitle("About %s" % (self._title,))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setGeometry(100, 100, 484, 224)
        self.setFixedSize(484, 224)

    def help(self):
        """Open a web page"""
        url = QUrl(self.url_help)
        QDesktopServices.openUrl(url)

    def report(self):
        """Open a web page"""
        url = QUrl(self.url_report)
        QDesktopServices.openUrl(url)

# test a dialog
if __name__ == '__main__':
    app = GApplication(sys.argv)
    win = GAboutDialog()
    win.show()

    sys.exit(app.exec_())

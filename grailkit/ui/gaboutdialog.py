# -*- coding: UTF-8 -*-

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.ui import GDialog, GApplication


class GAboutDialog(GDialog):
    """Default about dialog"""

    def __init__(self, parent=None, title="", description=""):
        super(GAboutDialog, self).__init__(parent)

        self._init_ui()

    def _init_ui(self):
        self.ui_icon = QLabel(self)
        self.ui_icon.setPixmap(QPixmap(":/icons/128.png"))
        self.ui_icon.setAlignment(Qt.AlignCenter)
        self.ui_icon.setStyleSheet("background: black;")
        self.ui_icon.setGeometry(55, 68, 48, 48)

        self.ui_title = QLabel("Grail", self)
        self.ui_title.setGeometry(160, 34, 311, 26)

        self.ui_description = QPlainTextEdit("description", self)
        self.ui_description.setReadOnly(True)
        self.ui_description.setGeometry(160, 74, 311, 100)

        self.ui_btn_help = QPushButton("Help")
        self.ui_btn_report = QPushButton("Report a problem")
        self.ui_btn_close = QPushButton("Close")

        self.ui_buttons_layout = QHBoxLayout()
        self.ui_buttons_layout.addWidget(self.ui_btn_help)
        self.ui_buttons_layout.addWidget(self.ui_btn_report)
        self.ui_buttons_layout.addWidget(self.ui_btn_close)

        self.ui_buttons = QWidget(self)
        self.ui_buttons.setLayout(self.ui_buttons_layout)
        self.ui_buttons.setGeometry(16, 187, 455, 40)

        self.setWindowTitle('About')
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setGeometry(100, 100, 484, 224)
        self.setFixedSize(484, 224)

# test a dialog
if __name__ == '__main__':
    app = GApplication(sys.argv)
    win = GAboutDialog()
    win.show()

    sys.exit(app.exec_())

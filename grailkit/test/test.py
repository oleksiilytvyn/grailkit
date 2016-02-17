#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys

from PyQt5.QtWidgets import QMainWindow

from grailkit.ui import GApplication


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 480)
        self.setMinimumSize(320, 240)
        self.setWindowTitle("Grail")
        self.show()


def main():
    """Launch application"""

    app = GApplication(sys.argv)
    win = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

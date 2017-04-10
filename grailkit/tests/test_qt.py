# -*- coding: UTF-8 -*-
"""
    grailkit.tests.test_qt
    ~~~~~~~~~~~~~~~~~~~~~~

    Launch testing application using all grailkit Qt components
"""
import sys

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QStyle, QApplication

from grailkit.qt import *


class FramelessExample(Frameless):

    def __init__(self):
        super(FramelessExample, self).__init__()

        self.setGeometry(0, 0, 300, 200)

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)

        p.fillRect(QRect(0, 0, self.width(), self.height()), QColor("#ff0000"))

        p.end()

class ExampleDialog(Dialog):

    def __init__(self):
        super(ExampleDialog, self).__init__()

        self.__ui__()

    def __ui__(self):

        self.ui_list = List()

        for i in range(10):
            self.ui_list.addItem(ListItem('Item #%d' % i))

        self.ui_welcome = Welcome(title='Welcome to Grailkit 1.0',
                                  description='This is example of components',
                                  icon=QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning))
        self.ui_welcome.addWidget(WelcomeAction(title='First action',
                                                icon=QApplication.style().standardIcon(QStyle.SP_MessageBoxQuestion)))
        self.ui_welcome.addWidget(WelcomeAction(title='Second action',
                                                icon=QApplication.style().standardIcon(QStyle.SP_MessageBoxWarning)))
        self.ui_welcome.addWidget(WelcomeAction(title='Third action',
                                                icon=QApplication.style().standardIcon(QStyle.SP_MessageBoxCritical)))

        self.ui_layout = HLayout()
        self.ui_layout.addWidget(self.ui_list)
        self.ui_layout.addWidget(self.ui_welcome)

        self.setLayout(self.ui_layout)


def main():

    app = Application(sys.argv)

    fl = FramelessExample()
    fl.show()

    dialog = ExampleDialog()
    dialog.show()

    about_dialog = AboutDialog()
    about_dialog.show()

    message_dialog = MessageDialog()
    message_dialog.show()

    progress_dialog = ProgressDialog()
    progress_dialog.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()

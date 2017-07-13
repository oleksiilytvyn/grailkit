# -*- coding: UTF-8 -*-
"""
    grailkit.tests.test_qt
    ~~~~~~~~~~~~~~~~~~~~~~

    Launch testing application using all grailkit Qt components
"""
import sys
import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from grailkit.qt import *


class ExampleDialog(Dialog):
    """Example dialog with list, welcome, toolbar"""

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

        self.ui_toolbar = Toolbar()
        self.ui_toolbar.addWidget(Label('Untitled Project'))
        self.ui_toolbar.addStretch()
        self.ui_toolbar.addWidget(Button('Go'))
        self.ui_toolbar.addWidget(Button('Stop'))
        self.ui_toolbar.addWidget(Button('|<'))
        self.ui_toolbar.addWidget(Button('>|'))
        self.ui_toolbar.addStretch()
        self.ui_toolbar.addWidget(Button('MIDI'))
        self.ui_toolbar.addWidget(Button('OSC'))

        self.ui_splitter = Splitter()
        self.ui_splitter.addWidget(self.ui_list)
        self.ui_splitter.addWidget(self.ui_welcome)
        self.ui_splitter.setSizes([200, self.ui_splitter.width() - 200])

        self.ui_layout = VLayout()
        self.ui_layout.addWidget(self.ui_toolbar)
        self.ui_layout.addWidget(self.ui_splitter)

        self.setLayout(self.ui_layout)
        self.setWindowTitle('Test dialog')
        self.setGeometry(300, 300, 600, 400)


class DisplayTexture(QImage):

    def __init__(self, *args):
        super(DisplayTexture, self).__init__(*args)

    def render(self):

        _time = datetime.datetime.now()
        text = "%s:%s:%s" % (str(_time.hour).zfill(2), str(_time.minute).zfill(2), str(_time.second).zfill(2))
        padding = 10

        p = QPainter()
        p.begin(self)
        p.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        p.fillRect(self.rect(), Qt.black)

        p.setPen(QColor('#fff'))
        box = QRect(self.rect().topLeft(), self.rect().bottomRight())
        box.adjust(padding, padding, -padding, -padding)

        p.drawText(box, Qt.AlignCenter | Qt.TextWordWrap, text)

        p.end()


class TextureDialog(QWidget):

    def __init__(self, parent=None, texture=None):
        super(TextureDialog, self).__init__(parent)

        self._texture = texture

        self.setGeometry(300, 300, 300, 400)

    def paintEvent(self, QPaintEvent):

        p = QPainter()
        p.begin(self)

        p.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        p.fillRect(self.rect(), Qt.black)

        if self._texture:
            p.drawImage(self.rect(), self._texture)

        p.end()


class SettingsDialog(Dialog):
    """Sample settings dialog"""

    def __init__(self):
        super(SettingsDialog, self).__init__()

        self.__ui__()

    def __ui__(self):

        self.ui_list = List()
        self.ui_list.addItem(ListItem('General'))
        self.ui_list.addItem(ListItem('Plugins'))
        self.ui_list.addItem(ListItem('Bible'))

        self.ui_panel_layout = VLayout()
        self.ui_panel_layout.setSpacing(4)
        self.ui_panel_layout.addWidget(Label('Hello world'))
        self.ui_panel_layout.addWidget(Switch())
        self.ui_panel_layout.addWidget(LineEdit())
        search = SearchEdit()
        search.setPlaceholderText("Search...")
        self.ui_panel_layout.addWidget(search)
        self.ui_panel_layout.addWidget(Button('Go!'))
        self.ui_panel_layout.addWidget(Spacer())

        self.ui_panel = Component()
        self.ui_panel.setLayout(self.ui_panel_layout)

        self.ui_layout = HLayout()
        self.ui_layout.addWidget(self.ui_list)
        self.ui_layout.addWidget(self.ui_panel)

        self.setLayout(self.ui_layout)

        self.setWindowTitle('Settings')
        self.setGeometry(200, 200, 400, 300)


if __name__ == '__main__':

    # application
    app = Application(sys.argv)

    # about dialog
    about_dialog = AboutDialog(title='GrailKit',
                               description="This is test of GrailKit components library")
    about_dialog.move(QPoint(450, 20))
    about_dialog.show()

    # message dialog
    message_dialog = MessageDialog(title="The title",
                                   text="Text message dialog",
                                   buttons=[MessageDialog.Ok, MessageDialog.Cancel, MessageDialog.Cancel],
                                   icon=MessageDialog.Information)
    message_dialog.move(0, 150)
    message_dialog.show()

    m = MessageDialog.information(None, 'The title', 'The message about something happened')
    m.show()

    # progress dialog
    progress_dialog = ProgressDialog(title="Some progress",
                                     text="Wait until something happens...")
    progress_dialog.setRange(0, 100)
    progress_dialog.setValue(60)
    progress_dialog.move(QPoint(0, 20))
    progress_dialog.show()

    # example dialog with toolbar, welcome, list
    dialog = ExampleDialog()
    dialog.moveCenter()
    dialog.show()

    settings = SettingsDialog()
    settings.show()

    # texture example

    tex = DisplayTexture(QSize(300, 400), QImage.Format_RGB32)
    tex.render()

    display_1 = TextureDialog(None, tex)
    display_1.setWindowTitle("Texture 1")
    display_1.show()

    display_2 = TextureDialog(None, tex)
    display_2.setWindowTitle("Texture 2")
    display_2.show()

    def repaint_texture():
        tex.render()
        display_1.repaint()
        display_2.repaint()

    timer = QTimer()
    timer.timeout.connect(repaint_texture)
    timer.start(100)

    sys.exit(app.exec())

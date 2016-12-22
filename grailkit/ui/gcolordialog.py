# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gcolordialog
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Color picker dialog
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.ui import GDialog, GColorWidget


class GColorDialog(GDialog):

    color_changed = pyqtSignal("QColor")

    def __init__(self, color=QColor(0, 0, 0), parent=None):
        super(GColorDialog, self).__init__(parent)

        self._color = color

        self.__ui__()

    def __ui__(self):
        """Create dialog UI"""

        # HSL layout
        self.ui_hsl_widget = HSLWidget()

        # RGB layout
        self.ui_rgb_widget = RGBWidget()

        # Palette layout
        self.ui_palette_widget = QWidget()

        # general layout
        self.ui_stack = QStackedWidget()

        self.ui_buttons_layout = QHBoxLayout()
        self.ui_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.ui_buttons_layout.setSpacing(2)

        self.ui_buttons = QWidget()
        self.ui_buttons.setLayout(self.ui_buttons_layout)

        self.ui_button_group = QButtonGroup(self)
        self.ui_button_group.buttonClicked.connect(self._button_clicked)

        self._add_tab("HSL", self.ui_hsl_widget)
        self._add_tab("RGB", self.ui_rgb_widget)
        self._add_tab("Palette", self.ui_palette_widget)
        self._set_tab(0)

        self.ui_line = QWidget()
        self.ui_line.setStyleSheet("border-bottom: 1px solid #222;")

        self.ui_actions = QDialogButtonBox()
        self.ui_actions.addButton('Cancel', QDialogButtonBox.RejectRole)
        self.ui_actions.addButton('Ok', QDialogButtonBox.AcceptRole)
        self.ui_actions.rejected.connect(self.reject)
        self.ui_actions.accepted.connect(self.accept)

        self.ui_layout = QVBoxLayout()
        self.ui_layout.setContentsMargins(0, 0, 0, 0)
        self.ui_layout.setSpacing(0)
        self.ui_layout.addWidget(self.ui_buttons)
        self.ui_layout.addWidget(self.ui_stack)
        self.ui_layout.addWidget(self.ui_line)
        self.ui_layout.addWidget(self.ui_actions)

        self.setLayout(self.ui_layout)
        self.setWindowTitle("Color")

    def _add_tab(self, name, widget):

        btn = QPushButton(name)
        btn.setDefault(False)
        btn.setAutoDefault(False)
        btn.setCheckable(True)
        btn.setChecked(False)

        index = len(self.ui_button_group.buttons())

        self.ui_buttons_layout.addWidget(btn)
        self.ui_button_group.addButton(btn, index)

        self.ui_stack.addWidget(widget)

    def _set_tab(self, index):

        btn = self.ui_button_group.button(index)
        btn.setChecked(True)

        self.ui_stack.setCurrentIndex(index)

    def _button_clicked(self, btn):

        index = self.ui_button_group.id(btn)

        self.ui_stack.setCurrentIndex(index)

    def setColor(self, color):
        """Set color

        Args:
            color (QColor): selected color
        """

        self._color = color

    def color(self):
        """Get selected color"""

        return self._color


class HSLWidget(QWidget):

    color_changed = pyqtSignal("QColor")

    def __init__(self):
        super(HSLWidget, self).__init__()

        self.__ui__()

    def __ui__(self):

        self.ui_color = GColorWidget()
        self.ui_color.color_changed.connect(self._changed)
        self.ui_brightness = QSlider(Qt.Horizontal, None)

        self.ui_layout = QVBoxLayout()
        self.ui_layout.addWidget(self.ui_color)
        self.ui_layout.addWidget(self.ui_brightness)

        self.setLayout(self.ui_layout)

    def _changed(self, color):
        print(color)


class RGBWidget(QWidget):

    def __init__(self):
        super(RGBWidget, self).__init__()

        self.__ui__()

    def __ui__(self):

        self.ui_slider_r = QSlider(Qt.Horizontal, None)
        self.ui_slider_g = QSlider(Qt.Horizontal, None)
        self.ui_slider_b = QSlider(Qt.Horizontal, None)

        self.ui_layout = QVBoxLayout()
        self.ui_layout.addWidget(self.ui_slider_r)
        self.ui_layout.addWidget(self.ui_slider_g)
        self.ui_layout.addWidget(self.ui_slider_b)

        self.setLayout(self.ui_layout)


if __name__ == "__main__":

    import sys
    from grailkit.ui import GApplication, GColorBalloon

    app = GApplication(sys.argv)

    win = GColorDialog()
    win.show()

    balloon = GColorBalloon()
    balloon.show()

    sys.exit(app.exec_())

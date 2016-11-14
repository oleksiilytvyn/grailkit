# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gsearchedit
    ~~~~~~~~~~~~~~~~~~~~~~~

    Utility functions and constants
"""
import sys

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtWidgets import QStyle, QToolButton, QLineEdit, QStyleOption

from grailkit.ui import GWidget


class GSearchEdit(QLineEdit):
    """Basic edit input for search with clear button"""

    keyPressed = pyqtSignal('QKeyEvent')
    focusOut = pyqtSignal('QFocusEvent')

    def __init__(self, parent=None):
        super(GSearchEdit, self).__init__(parent)

        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.textChanged.connect(self._text_changed)

        self._ui_clear_btn = QToolButton(self)
        self._ui_clear_btn.setIconSize(QSize(14, 14))
        self._ui_clear_btn.setIcon(QIcon(':/gk/icon/search-clear.png'))
        self._ui_clear_btn.setCursor(Qt.ArrowCursor)
        self._ui_clear_btn.hide()
        self._ui_clear_btn.clicked.connect(self.clear)

        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        # To-Do: move styles to qss file if possible
        self.setStyleSheet("""
                QLineEdit {
                    background-color: #e9e9e9;
                    padding-right: %spx;
                    }
                """ % str(self._ui_clear_btn.sizeHint().width() / 2 + frame_width + 1))

        size_hint = self.minimumSizeHint()

        self.setMinimumSize(
            max(size_hint.width(), self._ui_clear_btn.sizeHint().height() + frame_width * 2 + 2),
            max(size_hint.height(), self._ui_clear_btn.sizeHint().height() + frame_width * 2 + 2))

    def resizeEvent(self, event):
        """Redraw some elements"""

        size = self.rect()
        btn_size = self._ui_clear_btn.sizeHint()

        self._ui_clear_btn.move(size.width() - btn_size.width() - 4,
                                size.height() / 2 - btn_size.height() / 2 + 2)

    def keyPressEvent(self, event):
        """Implements keyPressed signal"""

        super(GSearchEdit, self).keyPressEvent(event)

        self.keyPressed.emit(event)

    def focusOutEvent(self, event):
        super(GSearchEdit, self).focusOutEvent(event)

        self.focusOut.emit(event)

    def _text_changed(self, text):
        """Process text changed event"""

        self._ui_clear_btn.setVisible(len(text) > 0)

    def className(self):
        """Returns widget name that used in stylesheet."""

        return "GSearchEdit"

# test a dialog
if __name__ == '__main__':

    from grailkit.ui import GDialog, GApplication
    from PyQt5.QtWidgets import QHBoxLayout

    app = GApplication(sys.argv)

    win = GDialog()
    layout = QHBoxLayout()
    layout.addWidget(GSearchEdit())
    layout.setContentsMargins(0, 0, 0, 0)
    win.setStyleSheet("background: #626364;")
    win.setLayout(layout)
    win.show()

    sys.exit(app.exec_())

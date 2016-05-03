# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gsearchedit
    ~~~~~~~~~~~~~~~~~~~~~~~

    Utility functions and constants
"""
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.ui import GWidget


class GSearchEdit(QLineEdit, GWidget):
    """Basic edit input for search with clear button"""

    keyPressed = pyqtSignal('QKeyEvent')

    def __init__(self, parent=None):
        super(GSearchEdit, self).__init__(parent)

        self.textChanged.connect(self._text_changed)

        self._ui_clear_btn = QToolButton(self)
        self._ui_clear_btn.setIconSize(QSize(14, 14))
        self._ui_clear_btn.setIcon(QIcon(':/icons/search-clear.png'))
        self._ui_clear_btn.setCursor(Qt.ArrowCursor)
        self._ui_clear_btn.setStyleSheet("border: none; padding: 0px;")
        self._ui_clear_btn.hide()

        self._ui_clear_btn.clicked.connect(self.clear)

        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.setStyleSheet("QLineEdit { padding-right: %spx; height: 21px;} " %
                           str(self._ui_clear_btn.sizeHint().width() + frame_width + 1))

        size_hint = self.minimumSizeHint()

        self.setMinimumSize(
            max(size_hint.width(), self._ui_clear_btn.sizeHint().height() + frame_width * 2 + 2),
            max(size_hint.height(), self._ui_clear_btn.sizeHint().height() + frame_width * 2 + 2))

    def resizeEvent(self, event):
        """Redraw some elements"""

        size_hint = self._ui_clear_btn.sizeHint()
        self._ui_clear_btn.move(self.rect().right() - size_hint.width(),
                                (self.rect().bottom() + 5 - size_hint.height()) / 2)

    def keyPressEvent(self, event):
        super(GSearchEdit, self).keyPressEvent(event)

        self.keyPressed.emit(event)

    def _text_changed(self, text):
        self._ui_clear_btn.setVisible(len(text) > 0)


# test a dialog
if __name__ == '__main__':
    from grailkit.ui import GDialog, GApplication

    app = GApplication(sys.argv)
    win = GDialog()
    layout = QHBoxLayout()
    layout.addWidget(GSearchEdit())
    win.setLayout(layout)
    win.show()

    sys.exit(app.exec_())

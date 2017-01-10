# -*- coding: UTF-8 -*-
"""
    grailkit.qt.gsearchedit
    ~~~~~~~~~~~~~~~~~~~~~~~

    Line edit with clear button and more signals
"""
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyle, QToolButton, QLineEdit

from grailkit.qt import GWidget


class GSearchEdit(QLineEdit, GWidget):
    """Basic edit input for search with clear button"""

    keyPressed = pyqtSignal('QKeyEvent')
    focusOut = pyqtSignal('QFocusEvent')

    def __init__(self, parent=None):
        super(GSearchEdit, self).__init__(parent)

        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.textChanged.connect(self._text_changed)

        self._ui_clear = QToolButton(self)
        self._ui_clear.setIconSize(QSize(14, 14))
        self._ui_clear.setIcon(QIcon(':/gk/icon/search-clear.png'))
        self._ui_clear.setCursor(Qt.ArrowCursor)
        self._ui_clear.setStyleSheet("QToolButton {background: none;}")
        self._ui_clear.hide()
        self._ui_clear.clicked.connect(self.clear)

        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)

        self.setStyleSheet("""
                QLineEdit {
                    background-color: #e9e9e9;
                    padding-right: %spx;
                    }
                """ % str(self._ui_clear.sizeHint().width() / 2 + frame_width + 1))

        size_hint = self.minimumSizeHint()
        btn_size_hint = self._ui_clear.sizeHint()

        self.setMinimumSize(
            max(size_hint.width(), btn_size_hint.height() + frame_width * 2 + 2),
            max(size_hint.height(), btn_size_hint.height() + frame_width * 2 + 2))

    def resizeEvent(self, event):
        """Redraw some elements"""

        size = self.rect()
        btn_size = self._ui_clear.sizeHint()
        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)

        self._ui_clear.move(size.width() - btn_size.width() / 2 - frame_width * 2,
                            size.height() / 2 - btn_size.height() / 2 + frame_width)

    def keyPressEvent(self, event):
        """Implements keyPressed signal"""

        super(GSearchEdit, self).keyPressEvent(event)

        self.keyPressed.emit(event)

    def focusOutEvent(self, event):
        """Focus is lost"""

        super(GSearchEdit, self).focusOutEvent(event)

        self.focusOut.emit(event)

    def _text_changed(self, text):
        """Process text changed event"""

        self._ui_clear.setVisible(len(text) > 0)
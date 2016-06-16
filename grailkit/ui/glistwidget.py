# -*- coding: UTF-8 -*-
"""
    grailkit.ui.glistwidget
    ~~~~~~~~~~~~~~~~~~~~~~~

    Simple list widget
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from grailkit.ui import GWidget


class GListWidget(QListWidget, GWidget):
    """Simple list widget"""

    def __init__(self, parent=None):
        super(GListWidget, self).__init__(parent)

        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.setAlternatingRowColors(True)

        # Fix a items overlapping issue
        self.setStyleSheet("QListWidget::item {padding: 4px 12px;}")

        self._scrollbar_original = self.verticalScrollBar()
        self._scrollbar = QScrollBar(Qt.Vertical, self)
        self._scrollbar.valueChanged.connect(self._scrollbar_original.setValue)
        self._scrollbar_original.valueChanged.connect(self._scrollbar.setValue)

        self._update_scrollbar()

    def _update_scrollbar(self):
        """Update a custom scrollbar"""

        original = self._scrollbar_original

        if original.value() == original.maximum() and original.value() == 0:
            self._scrollbar.hide()
        else:
            self._scrollbar.show()

        self._scrollbar.setPageStep(original.pageStep())
        self._scrollbar.setRange(original.minimum(), original.maximum())
        self._scrollbar.resize(8, self.rect().height())
        self._scrollbar.move(self.rect().width() - 8, 0)

    def paintEvent(self, event):
        """Redraw a widget"""
        QListWidget.paintEvent(self, event)

        self._update_scrollbar()


class GListItem(QListWidgetItem):
    """GListWidget list item"""

    def __init__(self, parent=None):
        super(GListItem, self).__init__(parent)


# test a widget
if __name__ == '__main__':

    import sys
    from grailkit.ui import GApplication, GDialog

    app = GApplication(sys.argv)
    win = GDialog()
    items = GListWidget()

    for index in range(10):
        items.addItem(GListItem("Item # %d" % (index,)))

    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(items)

    win.setLayout(layout)
    win.show()

    sys.exit(app.exec_())

# -*- coding: UTF-8 -*-
"""
    grailkit.qt.tree
    ~~~~~~~~~~~~~~~~

    TreeWidget and TreeItem
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView


class Tree(QTreeWidget):
    """Tree widget with predefined properties"""

    def __init__(self, parent=None):
        super(Tree, self).__init__(parent)

        self.setAlternatingRowColors(True)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.header().close()
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setWordWrap(True)
        self.setAnimated(False)
        self.setSortingEnabled(False)


class TreeItem(QTreeWidgetItem):
    """Representation of node as QTreeWidgetItem"""

    def __init__(self, data=None):
        super(TreeItem, self).__init__()

        self._data = data

    def object(self):
        """Returns associated object"""

        return self._data

    def setObject(self, data):
        """Set associated object"""

        self._data = data

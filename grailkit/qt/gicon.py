# -*- coding: UTF-8 -*-
"""
    grailkit.qt.gicon
    ~~~~~~~~~~~~~~~~~

    QIcon with color changing capabilities
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor


class GIcon(QIcon):

    def __init__(self, path=None):
        super(GIcon, self).__init__(path)

    def pixmap_color(self, width, height, color):
        """Create a pixmap from original icon, changing black color to given color

        Args:
            width (int): width of pixmap
            height (int): height of pixmap
            color (QColor): color of icon
        Returns:
            QPixmap of icon
        """

        pixmap = self.pixmap(width, height)
        mask = pixmap.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
        pixmap.fill(color)
        pixmap.setMask(mask)

        return pixmap

    def addColoredPixmap(self, width=128, height=128, color=QColor("#000"), mode=QIcon.Normal, state=QIcon.On):
        """Add a pixmap with given color

        Args:
            width (int): width of added pixmap
            height (int): height of added pixmap
            color (QColor): color of icon
            mode: QIcon mode
            state: QIcon state
        """

        self.addPixmap(self.pixmap_color(width, height, color), mode, state)

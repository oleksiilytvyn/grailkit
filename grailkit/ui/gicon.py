# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gicon
    ~~~~~~~~~~~~~~~~~

    QIcon with color changing capabilities
"""
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


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


if __name__ == "__main__":

    import sys
    from grailkit.ui import GApplication, GDialog

    app = GApplication(sys.argv)

    win = GDialog()
    icon_svg = GIcon(":/gk/icon/close.svg")
    icon = QIcon()
    icon.addPixmap(icon_svg.pixmap_color(128, 128, QColor("#f00")), QIcon.Active, QIcon.On)
    icon.addPixmap(icon_svg.pixmap_color(128, 128, QColor("#0f0")), QIcon.Active, QIcon.Off)
    icon.addPixmap(icon_svg.pixmap_color(128, 128, QColor("#0ff")), QIcon.Normal, QIcon.On)
    icon.addPixmap(icon_svg.pixmap_color(128, 128, QColor("#f0f")), QIcon.Normal, QIcon.Off)
    icon.addPixmap(icon_svg.pixmap_color(128, 128, QColor("#00f")), QIcon.Selected, QIcon.On)
    icon.addPixmap(icon_svg.pixmap_color(128, 128, QColor("#ff0")), QIcon.Selected, QIcon.Off)

    pixmap = icon_svg.pixmap_color(128, 128, QColor("#ff0000"))

    label = QLabel()
    label.setPixmap(pixmap)

    btn = QPushButton("Button")
    btn.setCheckable(True)
    btn.setIcon(icon)

    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(btn)

    win.setLayout(layout)
    win.setWindowIcon(icon)
    win.show()

    sys.exit(app.exec_())

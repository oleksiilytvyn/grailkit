# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gcolorslider
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Slider with ability to set gradient as background
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class GColorSlider(QSlider):

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(GColorSlider, self).__init__(orientation, parent)

        self._background = QBrush(Qt.darkGray, Qt.DiagCrossPattern)
        self._gradient = QLinearGradient()
        self._gradient.setCoordinateMode(QGradient.StretchToDeviceMode)

    def paintEvent(self, event):
        super(GColorSlider, self).paintEvent(event)

        p = QPainter()
        p.begin(self)

        panel = QStyleOptionFrame()
        panel.initFrom(self)
        panel.lineWidth = 1
        panel.midLineWidth = 0
        panel.state |= QStyle.State_Sunken

        self.style().drawPrimitive(QStyle.PE_Frame, panel, p, self)
        r = self.style().subElementRect(QStyle.SE_FrameContents, panel, self)
        p.setClipRect(r)

        if self.orientation() == Qt.Horizontal:
            self._gradient.setFinalStop(1, 0)
        else:
            self._gradient.setFinalStop(0, 1)

        p.setPen(Qt.NoPen)
        p.setBrush(self._background)
        p.drawRect(1, 1, self.geometry().width()-2, self.geometry().height()-2)
        p.setBrush(self._gradient)
        p.drawRect(1, 1, self.geometry().width()-2, self.geometry().height()-2)

        p.setClipping(False)
        opt_slider = QStyleOptionSlider()
        self.initStyleOption(opt_slider)
        opt_slider.state &= ~QStyle.State_HasFocus
        opt_slider.subControls = QStyle.SC_SliderHandle

        if self.isSliderDown():
            opt_slider.state |= QStyle.State_Sunken
            opt_slider.activeSubControls = QStyle.SC_SliderHandle

        opt_slider.rect = self.style().subControlRect(QStyle.CC_Slider,opt_slider, QStyle.SC_SliderHandle, self)

        self.style().drawComplexControl(QStyle.CC_Slider, opt_slider, p, self)

        p.end()

    def setGradient(self, gradient):
        self._gradient = gradient


if __name__ == "__main__":

    import sys
    from grailkit.qt import GApplication, GDialog

    app = GApplication(sys.argv)
    h_slider = GColorSlider(Qt.Horizontal)
    v_slider = GColorSlider(Qt.Vertical)

    layout = QHBoxLayout()
    layout.addWidget(v_slider)
    layout.addWidget(h_slider)

    win = GDialog()
    win.setLayout(layout)
    win.setStyleSheet("GDialog {background: #2f2f2f;}")
    win.show()

    sys.exit(app.exec_())

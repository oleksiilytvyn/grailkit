# -*- coding: UTF-8 -*-
"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""
from PyQt5.QtCore import Qt
from grailkit.util import default_key
import grailkit.experimental._ui.abstract as abstract


def qt_align(align):
    """Convert grailkit align to Qt align constant"""

    _align = {
        abstract.ALIGN_LEFT: Qt.AlignLeft,
        abstract.ALIGN_RIGHT: Qt.AlignRight,
        abstract.ALIGN_H_CENTER: Qt.AlignHCenter,
        abstract.ALIGN_JUSTIFY: Qt.AlignJustify,
        abstract.ALIGN_TOP: Qt.AlignTop,
        abstract.ALIGN_BOTTOM: Qt.AlignBottom,
        abstract.ALIGN_V_CENTER: Qt.AlignVCenter,
        abstract.ALIGN_BASELINE: Qt.AlignBaseline,
        abstract.ALIGN_CENTER: Qt.AlignCenter
        }

    return default_key(_align, align, default=Qt.AlignCenter)

# -*- coding: UTF-8 -*-
"""
    grailkit._ui.qt.label
    ~~~~~~~~~~~~~~~~~~~~~

    Label component implementation
"""
from PyQt5.QtWidgets import QLabel

import grailkit.experimental._ui.abstract as abstract

from .util import qt_align
from .component import Component


class Label(abstract.Label, Component):
    """Basic label component"""

    def __init__(self, text=""):
        super(Label, self).__init__()

        self._qt_instance = QLabel(text)

    @property
    def text(self):
        """Returns label text"""

        return self._qt_instance.text()

    def set_text(self, text):
        """Set label text

        Args:
            text (str): label text
        """

        self._qt_instance.setText(text)

    @property
    def wordwrap(self):
        """Return True if wordwrap enabled"""

        return self._qt_instance.wordWrap()

    def set_wordwrap(self, flag):
        """Sets text wordwrap

        Args:
            flag (bool): wordwrap
        """

        self._qt_instance.setWordWrap(flag)

    @property
    def align(self):
        """Returns text align"""

        return self._qt_instance.alignment()

    def set_align(self, align):
        """Set text align

        Args:
            align (int): text alignment
        """

        self._qt_instance.setAlignment(qt_align(align))

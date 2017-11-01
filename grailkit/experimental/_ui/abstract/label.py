# -*- coding: UTF-8 -*-
"""
    grailkit._ui.abstract.label
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Label component

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
from .component import Component


class Label(Component):
    """Basic label component"""

    def __init__(self, text=""):
        super(Label, self).__init__()

    @property
    def text(self):
        """Returns label text"""

        return ""

    def set_text(self, text):
        """Set label text

        Args:
            text (str): label text
        """

        raise NotImplementedError("This is abstract method")

    @property
    def wordwrap(self):
        """Return True if wordwrap enabled"""

        return True

    def set_wordwrap(self, flag):
        """Sets text wordwrap

        Args:
            flag (bool): wordwrap
        """

        raise NotImplementedError("This is abstract method")

    @property
    def align(self):
        """Returns text align"""

        return None

    def set_align(self, align):
        """Set text align

        Args:
            align (int): text alignment
        """

        raise NotImplementedError("This is abstract method")

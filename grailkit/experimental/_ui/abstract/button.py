# -*- coding: UTF-8 -*-
"""
    grailkit._ui.abstract.button
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Button component

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from .component import Component


class Button(Component):

    BUTTON_STYLE_DEFAULT = 0
    BUTTON_STYLE_OUTLINE = 1
    BUTTON_STYLE_OPAQUE = 2

    def __init__(self, text="", style=None):
        super(Button, self).__init__()

    @property
    def text(self):
        return ""

    def set_text(self, text):
        pass

    def set_color(self, color):
        pass

    def set_icon(self, icon):
        pass

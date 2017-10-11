# -*- coding: UTF-8 -*-
"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""
from .component import Component


class Label(Component):
    """Basic label component"""

    def __init__(self, text=""):
        super(Label, self).__init__()

    @property
    def text(self):
        return ""

    def set_text(self, text):
        pass

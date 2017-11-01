# -*- coding: UTF-8 -*-
"""
    grailkit._ui.abstract.list
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    List component

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from .component import Component


class List(Component):

    def __init__(self):
        super(List, self).__init__()

    def append(self, component):
        pass

    def remove(self, component):
        pass


class ListItem(object):
    """Abstract list item"""

    def __init__(self, text=""):
        pass

    @property
    def text(self):
        return ""

    def set_text(self, text):
        pass

    @property
    def data(self):
        return None

    def set_data(self, data):
        pass

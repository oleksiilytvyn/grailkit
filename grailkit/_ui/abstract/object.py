# -*- coding: UTF-8 -*-
"""

    ~~~~~~~~~~~~~~~~~~~~~~~~~~


"""
from grailkit.core import Signalable


class Object(Signalable):
    """Base class for all ui module classes"""

    def __init__(self):
        super(Object, self).__init__()

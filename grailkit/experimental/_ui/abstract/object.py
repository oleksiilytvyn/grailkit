# -*- coding: UTF-8 -*-
"""
    grailkit._ui.abstract.object
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Base object of all ui classes

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
from grailkit.core import Signalable


class Object(Signalable):
    """Base class for all ui module classes"""

    def __init__(self):
        super(Object, self).__init__()

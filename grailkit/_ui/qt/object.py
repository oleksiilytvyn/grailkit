# -*- coding: UTF-8 -*-
"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""
import grailkit._ui.abstract as abstract


class Object(abstract.Object):

    def __init__(self):
        super(Object, self).__init__()

        self._qt_instance = None

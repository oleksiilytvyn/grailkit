#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PyQt5.QtWidgets import QDialog


class GDialog(QDialog):
    """Dialog window"""

    def className( self ):
        """
        Returns widget name that used in stylesheet.
        
        stylesheet example:
            GDialog {
                background: red;
            }
        """

        return type(self).__name__

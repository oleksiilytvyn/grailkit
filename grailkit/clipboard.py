# -*- coding: UTF-8 -*-
"""
    grailkit.clipboard
    ~~~~~~~~~~~~~~~~~~

    Manage OS clipboard

    https://github.com/asweigart/pyperclip
"""
import pyperclip


def copy(data):
    """Copy given `data` to clipboard"""

    pyperclip.copy(data)


def paste():
    """Get data from clipboard"""

    return pyperclip.paste()

# -*- coding: UTF-8 -*-
"""
    grailkit.clipboard
    ~~~~~~~~~~~~~~~~~~

    Manage OS clipboard

    https://github.com/asweigart/pyperclip
"""
try:
    import pyperclip
except ImportError:
    def copy(data): pass

    def paste(): pass

    pyperclip = {
        copy: copy,
        paste: paste
        }


def copy(data):
    """Copy given `data` to clipboard"""

    pyperclip.copy(data)


def paste():
    """Get data from clipboard"""

    return pyperclip.paste()
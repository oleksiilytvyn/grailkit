# -*- coding: UTF-8 -*-
"""
    grailkit.app.window
    ~~~~~~~~~~~~~~~~~~~

    Pyglet window extension

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
import pyglet


class Window(pyglet.window.Window):
    """Simple window"""

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

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

        self._layout = None

    def set_layout(self, component):
        """Set window layout component"""

        self._layout = component

    def on_draw(self):
        """Draw window layout if available"""

        if self._layout:
            self._layout.draw()

# -*- coding: UTF-8 -*-
"""
    grailkit.app.button
    ~~~~~~~~~~~~~~~~~~~

    Button component

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
from .component import Component
from .graphics import Graphics


class Button(Component):
    """Button component"""

    def __init__(self, parent=None):
        super(Button, self).__init__(parent)

    def on_draw(self):
        """Draw component"""

        g = Graphics()
        g.color = (20, 20, 20, 255)
        g.fill_rect(self.x, self.y, self.width, self.y)
        g.end()

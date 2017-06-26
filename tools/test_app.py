# -*- coding: UTF-8 -*-
"""
    
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""
import sys
import pyglet
import random

from grailkit.app import Application


class AppWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__(*args, **kwargs)

        self.label = pyglet.text.Label('Hello, world',
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=self.width // 2,
                                       y=self.height // 2,
                                       anchor_x='center',
                                       anchor_y='center')

    def on_draw(self):
        """Draw everything"""

        self.clear()
        self.label.draw()

    def on_resize(self, width, height):
        """Update resizing"""
        super(AppWindow, self).on_resize(width, height)

        self.label.x = self.width // 2
        self.label.y = self.height // 2


if __name__ == '__main__':

    app = Application(sys.argv)

    window = AppWindow(caption="Hello World!",
                       resizable=True,
                       style=pyglet.window.Window.WINDOW_STYLE_DEFAULT)

    tool = pyglet.window.Window(caption='Tools',
                                style=pyglet.window.Window.WINDOW_STYLE_TOOL)

    @tool.event
    def on_draw():
        main_batch = pyglet.graphics.Batch()
        pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)

        # for is less likely to get stuck than while
        for i in range(2):
            x = random.randint(0, window.width)
            y = random.randint(0, window.height)
            dest_x = random.randint(0, window.width)
            dest_y = random.randint(0, window.height)

            main_batch.add(2, pyglet.gl.GL_LINES, None,
                           ('v2f', (x, y, dest_x, dest_y)),
                           ('c3B', (255, 0, 0, 0, 255, 0))  # c3B is a gradient (0,0,0, 255,255,255) combo
                           # this gradient will be per line, not end to end.
                           )
        main_batch.draw()

    app.run()

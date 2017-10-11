# -*- coding: UTF-8 -*-
"""
Test ui module
"""
import sys
import grailkit.ui as ui

app = ui.Application(sys.argv)
win = ui.Window(800, 600, caption="Grailkit Window", style=ui.Window.WINDOW_STYLE_DIALOG)

layout = ui.VLayout()
layout.append(ui.Label("Hello world"))

win.set_component(layout)

sys.exit(app.run())

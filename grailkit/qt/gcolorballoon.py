# -*- coding: UTF-8 -*-
"""
    grailkit.qt.gcolorballoon
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Color picker balloon dialog
"""

from grailkit.qt import GBalloonDialog, GColorDialog


class GColorBalloon(GColorDialog, GBalloonDialog):

    pass


if __name__ == '__main__':

    import sys
    from grailkit.qt import GApplication

    app = GApplication(sys.argv)

    win = GColorBalloon()
    win.show()

    sys.exit(app.exec_())

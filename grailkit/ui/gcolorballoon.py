# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gcolorballoon
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Color picker balloon dialog
"""

from grailkit.ui import GBalloonDialog, GColorDialog


class GColorBalloon(GColorDialog, GBalloonDialog):

    pass


if __name__ == '__main__':

    import sys
    from grailkit.ui import GApplication

    app = GApplication(sys.argv)

    win = GColorBalloon()
    win.show()

    sys.exit(app.exec_())

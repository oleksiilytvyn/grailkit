# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gapplication
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Extended QApplication class
"""
import re
import sys

from PyQt5.QtCore import QSharedMemory, QFile, Qt
from PyQt5.QtWidgets import QApplication, QStyleFactory

import grailkit.resources


class GApplication(QApplication):
    """Base class for all grail applications"""

    def __init__(self, argv):
        """For proper work you need to set application name via self.setApplicationName(name)"""
        super(GApplication, self).__init__(argv)

        self._shared_memory = None
        self._sys_exception_handler = sys.excepthook

        # set a exception handler
        sys.excepthook = self.unhandledException

        # prevent from running more than one instance
        if not self.moreThanOneInstanceAllowed() and self.isAlreadyRunning():
            self.quit()

        # fix for retina displays
        try:
            self.setAttribute(Qt.AA_UseHighDpiPixmaps)
        except:
            pass

        # use GTK style if available
        for style in QStyleFactory.keys():
            if "gtk" in style.lower():
                self.setStyle(QStyleFactory.create("gtk"))

        self.setStyleSheet(self._get_stylesheet())

    def _get_stylesheet(self):
        """
        Get the application stylesheet

        Returns: string
        """

        data = ""
        stream = QFile(":/gk/ui.qss")

        if stream.open(QFile.ReadOnly):
            data = str(stream.readAll())
            stream.close()

        data = re.sub(r'\\n', '', data)
        data = re.sub(r'\\t', '', data)

        return data[2:-1]

    def quit(self):
        """Quit application and close all connections"""

        self._shared_memory.detach()
        super(GApplication, self).quit()
        sys.exit()

    def unhandledException(self, exctype, value, traceback_object):
        """Re-implement this method to catch exceptions"""
        self._sys_exception_handler(exctype, value, traceback_object)

    def isAlreadyRunning(self):
        """Check for another instances of Grail

        Returns: Boolean
        """

        self._shared_memory = QSharedMemory(self.applicationName())

        if self._shared_memory.attach():
            self.anotherInstanceStarted()
            return True
        else:
            self._shared_memory.create(1)

        return False

    def moreThanOneInstanceAllowed(self):
        """Allow multiple instances or not"""

        return True

    def anotherInstanceStarted(self):
        """Re-implement this method to show dialog when application is already running."""

        pass

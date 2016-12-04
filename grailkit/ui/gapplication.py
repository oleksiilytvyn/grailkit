# -*- coding: UTF-8 -*-
"""
    grailkit.ui.gapplication
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Extended QApplication class
"""
import re
import sys

from PyQt5.QtCore import QSharedMemory, QFile, Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication, QStyleFactory

import grailkit.resources


class GApplication(QApplication):
    """Base class for all grail applications"""

    def __init__(self, argv):
        """For proper work you need to set application name via self.setApplicationName(name)"""
        super(GApplication, self).__init__(argv)

        self._shared_memory = None
        self._sys_exception_handler = sys.excepthook
        self._stylesheet_file = None
        self._stylesheet = ""

        self.lastWindowClosed.connect(self.quit)

        # set a exception handler
        sys.excepthook = self.unhandledException

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

        # prevent from running more than one instance
        if not self.moreThanOneInstanceAllowed() and self.isAlreadyRunning():
            self.quit()

    def _get_stylesheet(self):
        """
        Get the application stylesheet

        Returns: string
        """

        self._stylesheet = self._read_stylesheet(":/gk/ui.qss")
        self._stylesheet += self._read_stylesheet(self._stylesheet_file)

        return self._stylesheet

    def _read_stylesheet(self, file_path):
        """Read and return stylesheet file contents"""

        if not file_path:
            return ""

        data = ""
        stream = QFile(file_path)

        if stream.open(QFile.ReadOnly):
            data = str(stream.readAll())
            stream.close()

        return re.sub(r'(\\n)|(\\r)|(\\t)', '', data)[2:-1]

    def setStyleSheetFile(self, file_path):
        """Set a global style from a file

        Args:
            file_path (str): path to stylesheet file
        """

        self._stylesheet_file = file_path
        self.setStyleSheet(self._get_stylesheet())

    def getStyleSheet(self):
        """Returns application stylesheet"""

        return self._stylesheet

    def quit(self):
        """Quit application and close all connections"""

        if self._shared_memory and self._shared_memory.isAttached():
            self._shared_memory.detach()

        super(GApplication, self).quit()

    def unhandledException(self, exctype, value, traceback_object):
        """Re-implement this method to catch exceptions"""

        self._sys_exception_handler(exctype, value, traceback_object)

    def isAlreadyRunning(self):
        """Check for another instances of this application

        Returns: bool
        """

        self._shared_memory = QSharedMemory(self.applicationName())

        if self._shared_memory.attach():
            self.anotherInstanceStarted()
            return True
        else:
            self._shared_memory.create(1)

        return False

    def moreThanOneInstanceAllowed(self):
        """Allow multiple instances or not

        Returns: bool
        """

        return True

    def anotherInstanceStarted(self):
        """Re-implement this method to show dialog when application is already running."""

        pass


def AppInstance():
    """Get instance of Application

    Returns: instance of QCoreApplication or GApplication
    """

    return QCoreApplication.instance()

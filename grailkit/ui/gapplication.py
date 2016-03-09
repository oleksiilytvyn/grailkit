# -*- coding: UTF-8 -*-

import re
import sys

from PyQt5.QtCore import QSharedMemory, QFile, Qt
from PyQt5.QtWidgets import QApplication, QStyleFactory


class GApplication(QApplication):
    """Base class for all grail applications"""

    # allow multiple instances
    _multiple_instances = True
    _shared_memory = None
    _old_excepthook = None

    def __init__(self, argv):
        """For proper work you need to set application name via self.setApplicationName(name)"""
        super(GApplication, self).__init__(argv)

        self._old_excepthook = sys.excepthook
        sys.excepthook = self.hook_exception

        # prevent from running more than one instance
        if not self._multiple_instances and self.isAlreadyRunning():
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
        stream = QFile(":/stylesheet/app.qss")

        if stream.open(QFile.ReadOnly):
            data = str(stream.readAll())
            stream.close()

        data = re.sub(r'\\n', '', data)
        data = re.sub(r'\\t', '', data)

        return data[2:-1]

    def setMultipleInstances(self, enable):
        """Enable multiple instances to run

        Args:
            enable: enable or disable multiple instances
        """

        self._multiple_instances = bool(enable)

    def isAlreadyRunning(self):
        """Check for another instances of Grail

        Returns: Boolean
        """

        self.shared_memory = QSharedMemory(self.applicationName())

        if self.shared_memory.attach():
            self.alredy_running()
            return True
        else:
            self.shared_memory.create(1)

        return False

    def quit(self):
        """Quit application and close all connections"""

        self.shared_memory.detach()
        super(GApplication, self).quit()
        sys.exit()

    def alredy_running(self):
        """Reimplement this method to show dialog when application is alredy running."""
        pass

    def hook_exception(self, exctype, value, traceback_object):
        """Reimplement this method to catch exceptions"""
        self._old_excepthook(exctype, value, traceback_object)

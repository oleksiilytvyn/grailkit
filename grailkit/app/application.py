# -*- coding: UTF-8 -*-
"""
    grailkit.app.application
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Application instance management
"""
import sys

from PyQt5.QtCore import QSharedMemory, Qt
from PyQt5.QtWidgets import QApplication, QStyleFactory


class Application(object):
    """Application event loop"""

    __instance = None

    def __init__(self, argv):

        # don't allow creation of multiple instances
        if self.__instance:
            raise Exception("Only one instance of Application class is allowed")

        self._name = ''
        self._organization = ''
        self._domain = ''

        self._qt_app = QApplication(argv)
        self._qt_app.lastWindowClosed.connect(self.quit)
        self._shared_memory = None
        self._sys_exception_handler = sys.excepthook

        # set a exception handler
        sys.excepthook = self.unhandled_exception

        # fix for retina displays
        try:
            self._qt_app.setAttribute(Qt.AA_UseHighDpiPixmaps)
        except:
            pass

        # use GTK style if available
        for style in QStyleFactory.keys():
            if "gtk" in style.lower():
                self._qt_app.setStyle(QStyleFactory.create('gtk'))

        # prevent from running more than one instance
        if self.is_single_instance() and self.is_already_running():
            self.quit()

    @property
    def name(self):
        return self._name

    def run(self):
        """Run application event loop"""

        pass

    def quit(self):
        """Quit application event loop"""

        if self._shared_memory and self._shared_memory.isAttached():
            self._shared_memory.detach()

        self._qt_app.quit()

    def on_instance(self):
        """This method called when current instance is not firstly launched.
        Re-implement this method to show dialog when application is already running."""

        pass

    def is_single_instance(self):
        """Return True if multiple instances not allowed,
        by default any number of instances are allowed

        Returns: bool
        """

        return False

    def is_already_running(self):
        """Check for another instances of this application

        Returns: bool
        """

        self._shared_memory = QSharedMemory(self._name)

        if self._shared_memory.attach():
            self.on_instance()

            return True
        else:
            self._shared_memory.create(1)

        return False

    def unhandled_exception(self, exception_type, value, traceback_object):
        """Re-implement this method to catch exceptions"""

        # call default handler by default
        self._sys_exception_handler(exception_type, value, traceback_object)

    @classmethod
    def instance(cls):
        """Returns singleton instance"""

        return cls.__instance

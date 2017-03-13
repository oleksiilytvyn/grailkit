# -*- coding: UTF-8 -*-
"""
    grailkit.ui.application
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""

import os
import sys
import mmap
import pyglet


class Application(object):
    """Application """

    __instance = None

    def __int__(self, argv):
        """Create main application loop"""

        # don't allow creation of multiple instances
        if self.__instance:
            raise Exception("Only one instance of Application class is allowed")

        self._sys_exception_handler = sys.excepthook

        # set a exception handler
        sys.excepthook = self.unhandled_exception

        # prevent from running more than one instance
        if self.single_instance() and self.is_already_running():
            self.quit()

        pyglet.app.run()

    def _attach(self):
        """Attach a shared memory"""
        pass

    def _release(self):
        """Release shared memory"""
        pass

    def quit(self):
        """Quit application and break application event loop"""

        self._release()
        pyglet.app.exit()

    def unhandled_exception(self, exception_type, value, traceback_object):
        """Re-implement this method to catch exceptions"""

        # call default handler
        self._sys_exception_handler(exception_type, value, traceback_object)

    def on_instance(self):
        """This method called when another instance is started.
        Re-implement this method to show dialog when application is already running."""

        pass

    def single_instance(self):
        """Return True if multiple instances not allowed

        Returns: bool
        """

        return False

    def is_already_running(self):
        """Check for another instances of this application

        Returns: bool
        """

        return False

    @classmethod
    def instance(cls):
        """Get application instance"""

        return cls.__instance

# -*- coding: UTF-8 -*-
"""
    grailkit.app.application
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Application instance management

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
import sys
import socket
import pyglet


class Application(object):
    """Application event loop"""

    __instance = None

    def __init__(self, argv):

        # don't allow creation of multiple instances
        if self.__instance:
            raise Exception("Only one instance of Application class is allowed")

        self._name = 'Application'
        self._organization = 'Organization'
        self._domain = 'example.com'
        self._version = '0.1'
        self._argv = argv
        self._socket = None
        self._port = 65432
        self._already_running = False

        # set a exception handler
        self.__exception_handler = sys.excepthook
        sys.excepthook = self.on_exception

        self._bind()

        # prevent from running more than one instance
        if self.is_single_instance() and self.is_already_running():
            self.on_instance()

    @property
    def name(self):
        """This property holds the name of this application"""

        return self._name

    @name.setter
    def name(self, value):
        """Name of application

        Args:
            value (str): application name
        """

        self._name = value

    @property
    def organization(self):
        """This property holds the name of the organization that wrote this application"""

        return self._organization

    @organization.setter
    def organization(self, value):
        """Set the name of organization

        Args:
            value (str): organization name
        """

        self._organization = value

    @property
    def domain(self):
        """This property holds the Internet domain of the organization that wrote this application"""

        return self._domain

    @domain.setter
    def domain(self, value):
        """Set domain name of organization

        Args:
            value (str): internet domain name
        """

        self._domain = value

    @property
    def version(self):
        """This property holds version of this application"""

        return self._version

    @version.setter
    def version(self, value):
        """Set version of application

        Args:
            value (str): version string
        """

        self._version = value

    def run(self):
        """Run application event loop"""

        pyglet.app.run()

    def quit(self):
        """Quit application event loop"""

        pyglet.app.exit()

    def is_single_instance(self):
        """Return True if multiple instances not allowed,
        by default any number of instances are allowed

        Returns: bool
        """

        return True

    def is_already_running(self):
        """Check for another instances of this application

        Returns: bool
        """

        return self._already_running

    def on_instance(self):
        """This method called when current instance is not firstly launched.
        Re-implement this method to show dialog when application is already running."""

        self.quit()
        sys.exit()

    def on_exception(self, exception_type, value, traceback_object):
        """Re-implement this method to catch exceptions"""

        # call default handler by default
        self.__exception_handler(exception_type, value, traceback_object)

    def _bind(self):
        """Bind socket"""
        # xxx: replace with another solution that can check application name

        self._already_running = False

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind(('localhost', self._port))
        except:
            self._already_running = True

    @classmethod
    def instance(cls):
        """Returns singleton instance"""

        return cls.__instance

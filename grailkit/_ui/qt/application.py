# -*- coding: UTF-8 -*-
"""
    grailkit.ui.qt.application
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    
"""
import re
import sys

from PyQt5.QtCore import QSharedMemory, QFile, Qt
from PyQt5.QtWidgets import QApplication, QStyleFactory

# load qt resources
import grailkit.resources
import grailkit._ui.abstract as abstract


class Application(abstract.Application):
    """Application instance"""

    __instance = None

    def __init__(self, argv):
        super(Application, self).__init__(argv)

        self._qt_instance = QApplication(argv)
        self._qt_instance.lastWindowClosed.connect(self.quit)

        # fix for retina displays
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            self._qt_instance.setAttribute(Qt.AA_UseHighDpiPixmaps)

        # use GTK style if available
        for style in QStyleFactory.keys():
            if "gtk" in style.lower():
                self._qt_instance.setStyle(QStyleFactory.create("gtk"))

        self._qt_instance.setStyleSheet(self.__stylesheet)

        self._shared_memory = None

    @property
    def __stylesheet(self):
        """Get the application stylesheet

        Returns: stylesheet string
        """

        file_path = ":/gk/ui.qss"
        data = ""
        stream = QFile(file_path)

        if stream.open(QFile.ReadOnly):
            data = str(stream.readAll())
            stream.close()

        return re.sub(r'(\\n)|(\\r)|(\\t)', '', data)[2:-1]

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

        self._qt_instance.setApplicationName(value)
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

        self._qt_instance.setOrganizationName(value)
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

        self._qt_instance.setOrganizationDomain(value)
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

        self._qt_instance.setApplicationVersion(value)
        self._version = value

    def run(self):
        """Run application event loop"""

        return self._qt_instance.exec()

    def quit(self):
        """Quit application event loop"""

        if self._shared_memory and self._shared_memory.isAttached():
            self._shared_memory.detach()

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

        self._shared_memory = QSharedMemory(self.name)

        if self._shared_memory.attach():
            self.on_instance()
            return True
        else:
            self._shared_memory.create(1)

        return False

    def on_instance(self):
        """This method called when current instance is not firstly launched.
        Re-implement this method to show dialog when application is already running."""

        pass

    @classmethod
    def instance(cls):
        """Returns singleton instance"""

        return cls.__instance

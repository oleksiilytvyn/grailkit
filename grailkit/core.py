# -*- coding: UTF-8 -*-

import os
import sys
import shutil
import platform

# Platform constants
OS_ANY = True
OS_WIN = platform.system() == "Windows"
OS_MAC = platform.system() == "Darwin"
OS_UNIX = platform.system() == "unix"
OS_LINUX = platform.system() == "Linux"


class PathUtils:

    def get_app(self):
        """Get the path to main script file no matter how it's run.

        Returns:
            path to python script
            :rtype: string
        """

        apppath = sys.path[0]

        if hasattr(sys, 'frozen'):
            apppath = os.path.dirname(sys.executable)
        elif '__file__' in locals():
            apppath = os.path.dirname(__file__)
        else:
            apppath = sys.path[0]

        return os.path.abspath(apppath)

    def get_appdata(self, appname):
        """Returns appdata path for any platform

        Args:
            appname: name of application

        Returns:
            path
        """
        if sys.platform == 'win32':
            appdata = os.path.join(os.environ['APPDATA'], appname)
        else:
            appdata = os.path.expanduser(os.path.join("~", "." + appname))

        return os.path.abspath(appdata)

    def copy(self, source, destination):
        """Copy file 'source' to file 'destination'

        Args:
            source: path of file to be copied
            destination: file destination path

        Returns:
            returns True if copy is successful.
        """
        directory = os.path.dirname(os.path.realpath(destination))

        if not os.path.exists(source):
            return False

        if not os.path.exists(directory):
            os.makedirs(directory)

        if os.path.exists(source):
            shutil.copyfile(source, destination)

        return True

# export path utils
path = PathUtils()

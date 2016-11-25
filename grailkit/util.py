# -*- coding: UTF-8 -*-
"""
    grailkit.util
    ~~~~~~~~~~~~~

    Utility functions and constants
"""
import os
import sys
import time
import shutil
import platform
import gettext

# Platform constants
OS_ANY = True
OS_WIN = platform.system() == "Windows"
OS_MAC = platform.system() == "Darwin"
OS_UNIX = platform.system() == "unix"
OS_LINUX = platform.system() == "Linux"


def path_app():
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


def path_appdata(app_name):
    """Returns appdata path for any platform

    Args:
        app_name: name of application

    Returns:
        path
    """

    if sys.platform == 'win32':
        appdata = os.path.join(os.environ['APPDATA'], app_name)
    else:
        appdata = os.path.expanduser(os.path.join("~", "." + app_name))

    return os.path.abspath(appdata)


def copy_file(source, destination):
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


def millis_now():
    """Returns time in milliseconds since epoch"""

    return int(round(time.time() * 1000))


def __(message):
    """Translate string using gettext"""

    # to-do: implement this function
    return gettext.gettext(message)

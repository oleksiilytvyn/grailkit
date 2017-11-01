# -*- coding: UTF-8 -*-
"""
    grailkit.util
    ~~~~~~~~~~~~~

    Utility functions and constants

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import os
import sys
import time
import shutil
import platform

# Platform constants
OS_WIN = platform.system() == "Windows"
OS_MAC = platform.system() == "Darwin"
OS_UNIX = platform.system() == "unix"
OS_LINUX = platform.system() == "Linux"


def application_location():
    """Get the path to main script file no matter how it's run.

    Returns:
        path to current python script
    """

    if hasattr(sys, 'frozen'):
        path = os.path.dirname(sys.executable)
    elif '__file__' in locals():
        path = os.path.dirname(__file__)
    else:
        path = sys.path[0]

    return os.path.abspath(path)


def data_location(app_name):
    """Returns path to application data folder

    Args:
        app_name: name of application

    Returns:
        path to folder
    """

    if sys.platform == 'win32':
        path = os.path.join(os.environ['APPDATA'], app_name)
    else:
        path = os.path.expanduser(os.path.join("~", "." + app_name))

    return os.path.abspath(path)


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


def default_key(obj, key, default=None):
    """Get value by attribute in object or by key in dict
    if property exists returns value otherwise return `default` value.
    If object not exist or object don't have property returns `default`

    Args:
        obj (object, dict, list): dictionary
        key (str, int): key of property
        default (object): Object that returned if key not found
    """

    if obj and isinstance(obj, dict):
        return obj[key] if key in obj else default
    elif obj and isinstance(obj, object):
        return getattr(obj, key, default)
    else:
        return default


def file_exists(path):
    """Check if file exists

    Args:
        path (str): path to file
    """

    return os.path.exists(os.path.dirname(os.path.realpath(path))) and os.path.isfile(path)

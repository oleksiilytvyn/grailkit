# -*- coding: UTF-8 -*-
"""Utility functions and constants.

:copyright: (c) 2017-2020 by Oleksii Lytvyn (http://alexlitvin.name).
:license: MIT, see LICENSE for more details.
"""
from typing import Union, Any

import os
import sys
import time
import types
import shutil
import platform

# Platform constants
OS_WIN = platform.system() == "Windows"
OS_MAC = platform.system() == "Darwin"
OS_UNIX = platform.system() == "unix"
OS_LINUX = platform.system() == "Linux"

BUILTIN_TYPES = (
    bool,
    int,
    float,
    complex,
    str,
    dict,
    list,
    set,
    frozenset,
    tuple,
    bytes,
    bytearray,
    types.FunctionType,
    types.LambdaType,
    types.BuiltinFunctionType)


def application_location() -> str:
    """Get the path to main script file no matter how it's run.

    Returns:
        str: path to current python script
    """
    if hasattr(sys, 'frozen'):
        path = os.path.dirname(sys.executable)
    elif '__file__' in locals():
        path = os.path.dirname(__file__)
    else:
        path = sys.path[0]

    return os.path.abspath(path)


def data_location(app_name: str) -> str:
    """Return path to application data folder.

    Args:
        app_name (str): name of application

    Returns:
        str: path to folder
    """
    if sys.platform == 'win32':
        path = os.path.join(os.environ['APPDATA'], app_name)
    else:
        path = os.path.expanduser(os.path.join("~", "." + app_name))

    return os.path.abspath(path)


def copy_file(source: str, destination: str) -> bool:
    """Copy file 'source' to file 'destination'.

    Args:
        source (str): path of file to be copied
        destination (str): file destination path

    Returns:
        bool: True if copy is successful otherwise False
    """
    directory = os.path.dirname(os.path.realpath(destination))

    if not os.path.exists(source):
        return False

    if not os.path.exists(directory):
        os.makedirs(directory)

    if os.path.exists(source):
        shutil.copyfile(source, destination)

    return True


def millis_now() -> int:
    """Get current time in ms.

    Returns:
        int: time in milliseconds since epoch
    """
    return int(round(time.time() * 1000))


def default_key(obj: object, key: str, default: Any = None) -> Any:
    """Get value by attribute in object or by key in dict.

    If property exists returns value otherwise returns `default` value.
    If object not exist or object don't have property returns `default`.

    Args:
        obj (object, list, tuple, dict): dictionary
        key (str, int): key of property
        default (object): Object that returned if key not found
    Returns:
        value by given key or default
    """
    if obj and isinstance(obj, dict):
        return obj[key] if key in obj else default
    elif obj and isinstance(obj, object):
        return getattr(obj, key, default)
    else:
        return default


def file_exists(path: str) -> bool:
    """Check if file exists.

    Args:
        path (str): path to file
    Returns:
        bool: True if file exists, False otherwise
    """
    return os.path.exists(os.path.dirname(os.path.realpath(path))) and os.path.isfile(path)


def is_builtin(type_object: Union[type, object]) -> bool:
    """Check if object type is built-in.

    Args:
        type_object (type, object): object or type to check
    Returns:
        bool: True if built-in else False
    """
    return isinstance(type_object, type) or isinstance(type_object, BUILTIN_TYPES)


def object_type(object_ref: Union[type, object]) -> type:
    """Get type of anything.

    Args:
        object_ref (type, object): Object or type
    Returns:
        type: Type of given object
    """
    return object_ref if isinstance(object_ref, type) else type(object_ref)

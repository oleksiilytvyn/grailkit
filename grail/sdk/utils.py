#!/usr/bin/env python
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


def script_path():
  """Get the path to main script file no matter how it's run.

  Returns:
    path to python script
  """

  if hasattr(sys, 'frozen'):
    path = os.path.dirname(sys.executable)
  elif '__file__' in locals():
    path = os.path.dirname(__file__)
  else:
    path = sys.path[0]

  return path


def app_path( appname ):
  """Returns appdata path for any platform

  Args:
    - appname: name of program

  Returns: path
  """
  if sys.platform == 'win32':
    appdata = os.path.join(os.environ['APPDATA'], appname)
  else:
    appdata = os.path.expanduser(os.path.join("~", "." + appname))

  return appdata


def copy_file( a, b ):
  """Copy file A to file B

  Args:
    - a: path of file to be copied
    - b: path of file copy

  Returns:
    returns True if copy is succefull.
  """
  directory = os.path.dirname(os.path.realpath( b ))

  if not os.path.exists( a ):
    return False

  if not os.path.exists(directory):
    os.makedirs(directory)

  if os.path.exists( a ):
    shutil.copyfile( a, b )

  return True

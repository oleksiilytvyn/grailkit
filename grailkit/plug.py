# -*- coding: UTF-8 -*-
"""
    grailkit.plug
    ~~~~~~~~~~~~~

    Simple plugin loading mechanism

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""
import re
import os
import importlib


class PluginRegistry(type):
    """Subclasses registration mechanism based on meta-classes

    Use this class as meta-class to register plugin classes
    """

    def __init__(cls, *args):
        """Args:
            name (str): class name
            bases (list): class bases
            attrs (list): attributes
        """
        super(PluginRegistry, cls).__init__(*args)

        if not hasattr(cls, '__registry__'):
            cls.__registry__ = set()

        cls.__registry__.add(cls)
        # Remove base classes
        cls.__registry__ -= set(args[1])


class Plugin(object, metaclass=PluginRegistry):
    """Basic plugin class"""

    def __init__(self):
        pass

    @classmethod
    def plugins(cls):
        """Returns list of classes extended from Plugin"""

        return cls.__registry__


def discover(location):
    """Load and execute python modules in given location

    Args:
        location (str): path to plugins folder
    Returns:
        List of modules loaded
    """

    # todo: add loading of packages in directory

    location = os.path.abspath(location)
    module_name = os.path.basename(location)
    files = filter(re.compile('.py$', re.IGNORECASE).search, os.listdir(location))
    plugins = map(lambda fp: '.' + os.path.splitext(fp)[0], files)

    # import parent module / namespace
    importlib.import_module(module_name)
    modules = []

    for plugin in plugins:
        if not plugin.startswith('__'):
            modules.append(importlib.import_module(plugin, package=module_name))

    return modules

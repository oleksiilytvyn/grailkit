# -*- coding: UTF-8 -*-
"""
    grailkit.plug
    ~~~~~~~~~~~~~

    Simple plugin discovery, loading & registration mechanisms

    :copyright: (c) 2018 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
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
    """Base plugin class"""

    def __init__(self):
        pass

    @classmethod
    def plugins(cls):
        """Returns list of classes extended from Plugin"""

        return cls.__registry__


def discover(location, packages=False, exclude=None):
    """Load and execute python modules in given location

    Args:
        location (str): path to plugins folder
        packages (bool): If True sub-modules will be also loaded
        exclude (list): list of excluded modules, if modules also included. see `include_modules` argument
    Returns:
        list: modules loaded
    """

    location = os.path.abspath(location)
    module_name = os.path.basename(location)
    files = filter(re.compile('.py$', re.IGNORECASE).search, os.listdir(location))
    plugins = map(lambda fp: '.' + os.path.splitext(fp)[0], files)

    # import parent module / namespace
    importlib.import_module(module_name)
    modules = []
    exclude = exclude or []

    # include packages
    if packages:
        for name in os.listdir(location):
            if os.path.isfile(os.path.join(location, name + '/__init__.py')) and name not in exclude:
                modules.append(importlib.import_module(name, package=module_name))

    # include modules
    for plugin in plugins:
        if not plugin.startswith('__'):
            modules.append(importlib.import_module(plugin, package=module_name))

    return modules

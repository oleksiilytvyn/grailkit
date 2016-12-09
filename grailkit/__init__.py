# -*- coding: UTF-8 -*-
"""
    grailkit
    ~~~~~~~~

    GrailKit is a library for Grail like apps
"""

import os
from grailkit.util import path_appdata

# library version
__version__ = '0.1.1'

# path to shader folder
PATH_SHARED = path_appdata("grail-shared")
# path to library
PATH_LIBRARY = os.path.join(PATH_SHARED, "library.grail-library")
# path to settings
PATH_SETTINGS = os.path.join(PATH_SHARED, "settings.grail")

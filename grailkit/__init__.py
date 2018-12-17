# -*- coding: UTF-8 -*-
"""
    grailkit
    ~~~~~~~~

    GrailKit is a library for Grail like apps,
    library which consists of UI components for PyQt,
    grail files IO and networking libraries

    :copyright: (c) 2018 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""

import os
from grailkit.util import data_location

# library version
__version__ = '0.7'

# path to shader folder
PATH_SHARED = data_location("grail-shared")

# path to library
PATH_LIBRARY = os.path.join(PATH_SHARED, "library.grail-library")

# path to settings
PATH_SETTINGS = os.path.join(PATH_SHARED, "settings.grail")

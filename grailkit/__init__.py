# -*- coding: UTF-8 -*-
"""
GrailKit is a set of modules that help develop interactive apps.

:copyright: (c) 2017-2020 by Oleksii Lytvyn (http://alexlitvin.name).
:license: MIT, see LICENSE for more details.
"""

import os
from grailkit.util import data_location

# library version
__version__ = '0.10.1'

# path to shader folder
PATH_SHARED = data_location("grail-shared")

# path to library
PATH_LIBRARY = os.path.join(PATH_SHARED, "library.grail-library")

# path to settings
PATH_SETTINGS = os.path.join(PATH_SHARED, "settings.grail")

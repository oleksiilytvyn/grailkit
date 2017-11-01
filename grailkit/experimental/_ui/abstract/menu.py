# -*- coding: UTF-8 -*-
"""
    grailkit._ui.abstract.menu
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Menus & Actions

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: GNU, see LICENSE for more details.
"""


class Menu(object):
    """Abstract menu"""

    MENU_ACTION = 0
    MENU_SECTION = 1
    MENU_SEPARATOR = 2

    def __init__(self, name=""):
        """Create menu instance

        Args:
            name (str): menu name
        """

        pass

    def __len__(self):
        """Returns number of actions in menu"""

        return 0

    def append(self, item, style=None):
        """Append action to menu

        Args:
            item (grailkit._ui.Action): action to be added
            style: item style (action, separator, section caption)
        """

        raise NotImplementedError("This is abstract method")

    def remove(self, item):
        """Remove action from menu

        Args:
            item (grailkit._ui.Action): action that will be removed
        """

        raise NotImplementedError("This is abstract method")

    def insert(self, index, item, style=None):
        """Insert action at `index` to menu

        Args:
            index (int): item index
            item (grailkit._ui.Action): action to be added
            style: item style (action, separator, section caption)
        """

        raise NotImplementedError("This is abstract method")

    def clear(self):
        """Remove all actions from menu"""

        raise NotImplementedError("This is abstract method")

    def show(self, x, y):
        """Show menu at (x, y) position

        Args:
            x (int): screen x-coordinate
            y (int): screen y-coordinate
        """

        raise NotImplementedError("This is abstract method")


class Action(object):
    """Abstract menu action"""

    def __init__(self, name):
        """Create menu action

        Args:
            name (str): action name
        """

        self._name = name
        self._icon = None
        self._menu = None

    @property
    def name(self):
        """Returns item name"""

        return self._name

    def set_name(self):
        """Set action name"""

        raise NotImplementedError("This is abstract method")

    @property
    def icon(self):
        """Returns action icon"""

        return self._icon

    def set_icon(self, icon):
        """Set action name"""

        raise NotImplementedError("This is abstract method")

    @property
    def menu(self):
        """Returns associated menu"""

        return self._menu

    def set_menu(self, menu):
        """Associate menu with action, to be it's submenu"""

        raise NotImplementedError("This is abstract method")

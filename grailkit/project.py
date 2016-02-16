#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class ProjectError(Exception):
    """Base class for all project related exceptions"""
    pass


class Project:
    """Representation of a project"""

    _name = "Untitled project"
    _description = ""
    _author = ""
    _created = 0
    _modified = 0

    _db = None
    _items = []

    def __init__(self, file_path="", create=False):
        """Open or create a project

        Args:
            file_path (str): path to file
            create (bool): create file if not exists
        """

        if not file_path:
            raise ProjectError("Can't open project, file not specified.")

    def items(self): pass

    def insert(self, index, item): pass

    def append(self, item): pass

    def remove(self, index): pass

    def __len__(self):
        """Get number of cuelist in project"""
        pass

    def __getitem__(self, key): pass

    def __setitem__(self, key, value): pass

    def __delitem__(self, key): pass

    def __iter__(self):
        pass

    def __reversed__(self):
        pass


class Cuelist:
    """Representation of cuelist"""

    _id = 0
    _name = "Untitled cuelist"

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def __init__(self):
        """Create a cuelist"""
        pass

    def items(self):
        """List all cues inside this cuelist"""
        pass

    def insert(self, index, item):
        """Add Cue item to cuelist at `index` position

        Args:
            index (int): position to inset
            item (Cue): Cue to insert
        """
        pass

    def append(self, item):
        """Add Cue item to end of list

        Args:
            item (Cue): Cue to be added
        """
        pass

    def remove(self, index):
        """

        Args:
            index: index of item that will be removed
        """
        pass

    def __len__(self): pass

    def __getitem__(self, key): pass

    def __setitem__(self, key, value): pass

    def __delitem__(self, key): pass

    def __iter__(self): pass

    def __reversed__(self): pass


class Cue:
    """Representation of a Cue in Cuelist"""

    # Follow type
    FOLLOW_OFF = 0
    FOLLOW_ON = 1
    FOLLOW_CONTINUE = 2
    FOLLOW_TYPE = (FOLLOW_OFF, FOLLOW_ON, FOLLOW_CONTINUE)

    # default colors
    COLOR_RED = "#B71C1C"
    COLOR_ORANGE = "#EF6C00"
    COLOR_YELLOW = "#FFEB3B"
    COLOR_GREEN = "#8BC34A"
    COLOR_BLUE = "#03A9F4"
    COLOR_PURPLE = "#673AB7"
    COLOR_GRAY = "#BDBDBD"
    COLOR_DEFAULT = "#FFFFFF"
    COLORS = (COLOR_DEFAULT, COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_PURPLE, COLOR_GRAY)

    _id = 0
    _parent = 0
    _number = "1"
    _name = "Untitled cue"
    _color = COLOR_DEFAULT
    _pre_wait = 0
    _post_wait = 0
    _follow = FOLLOW_ON

    _items = []
    _data = {}

    @property
    def id(self):
        """unique identifier of cue"""
        return self._id

    @property
    def parent(self):
        """Identifier of parent cue, if 0 is in root of Cuelist"""
        return self._parent

    @property
    def number(self):
        """Identifier of cue assigned by user"""
        return self._number

    @property
    def name(self):
        """any text that describe cue"""
        return self._name

    @property
    def color(self):
        """any text that describe cue"""
        return self._color

    @property
    def pre_wait(self):
        """Wait before execution of cue"""
        return self._pre_wait

    @property
    def post_wait(self):
        """Wait after execution of cue"""
        return self._post_wait

    @property
    def follow(self):
        """Execute next cue after this finishes, move cursor to next or do nothing."""
        return self._follow

    @property
    def data(self):
        """Abstract data of cue"""
        return self._data

    def __init__(self):
        """Create a cue instance"""
        pass

    def items(self):
        """Get list of sub cues

        Returns:
            list of child cues
        """
        return self._items

    def insert(self, index, item):
        """Insert a child cue after

        Args:
            index (int): insert to index
            item (Cue): cue item
        """
        pass

    def append(self, item):
        """Add a child cue to end

        Args:
            item: cue item
        """
        return self.insert(len(self), item)

    def remove(self, index):
        """Remove item by index

        Args:
            index: index of an item
        """
        pass

    def __len__(self):
        """Child cues count"""
        return len(self._items)

    def __iter__(self):
        """Iterate through child cues"""
        return self._items

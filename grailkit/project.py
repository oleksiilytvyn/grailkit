# -*- coding: UTF-8 -*-

from grailkit.dna import DNA, DNAEntity


class ProjectError(Exception):
    """Base class for all project related exceptions"""
    pass


class Project(DNA):
    """Representation of a project"""

    _name = "Untitled project"
    _description = ""
    _author = ""
    _created = 0
    _modified = 0

    _items = []

    def __init__(self, file_path="", create=False):
        """Open or create a project

        Args:
            file_path (str): path to file
            create (bool): create file if not exists
        """

        super(Project, self).__init__(file_path, create=create)

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


class Cuelist(DNAEntity):
    """Representation of cuelist"""

    def __init__(self, parent):
        """Create a cuelist"""
        super(Cuelist, self).__init__(parent)

        self._name = "Untitled cuelist"


class Cue(DNAEntity):
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
    def number(self):
        """Identifier of cue assigned by user"""
        return self._number

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

    def __init__(self, parent):
        """Create a cue instance"""
        super(Cue, self).__init__(parent)

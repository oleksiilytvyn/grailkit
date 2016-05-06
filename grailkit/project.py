# -*- coding: UTF-8 -*-
"""
    grailkit.project
    ~~~~~~~~~~~~~~~~

    Interface to Grail project files
"""
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
    _id = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def created(self):
        return self._created

    @property
    def modified(self):
        return self._modified

    def __init__(self, file_path="", create=False):
        """Open or create a project

        Args:
            file_path (str): path to file
            create (bool): create file if not exists
        """

        super(Project, self).__init__(file_path, create=create)

        # read properties
        # find settings

    def __len__(self):
        """Get number of cuelist in project"""
        return len(self.cuelists())

    def settings(self):
        """Get a setting object"""
        entity = self._entities(filter_type=DNA.TYPE_SETTINGS,
                                filter_parent=self._id,
                                factory=Settings)

        if len(entity) == 0:
            entity = self._create(name="Settings",
                                  parent=self._id,
                                  entity_type=DNA.TYPE_SETTINGS,
                                  factory=Settings)
            return entity

        return entity[0]

    def cuelists(self):
        """Get all cuelists in project"""
        return self._entities(filter_type=DNA.TYPE_CUELIST,
                              filter_parent=self._id,
                              factory=Cuelist)

    def cuelist(self, cuelist_id):
        """Get a cuelist"""
        return self._entity(cuelist_id, factory=Cuelist)

    def remove(self, cuelist_id):
        """Remove a cuelist"""
        return self._remove(cuelist_id)

    def append(self, name="Untitled cuelist"):
        """Create a cuelist"""
        cuelist = self._create(name=name,
                               parent=self._id,
                               entity_type=DNA.TYPE_CUELIST,
                               factory=Cuelist)

        return cuelist


class Cuelist(DNAEntity):
    """Representation of cuelist"""

    def __init__(self, parent):
        """Create a cuelist"""
        super(Cuelist, self).__init__(parent)

    def __len__(self):
        """Return count of cues"""
        return len(self.cues())

    def cues(self):
        """Returns list of all cues in Cuelist"""

        return self._dna_parent._entities(filter_parent=self._id,
                                          filter_type=DNA.TYPE_CUE,
                                          factory=Cue)

    def cue(self, cue_id):
        """Get cue by id

        Args:
            cue_id (int): cue identifier
        """
        return self._dna_parent._entity(cue_id, factory=Cue)

    def append(self, name="Untitled Cue"):
        """Create a new cue and append to the end

        Args:
            name (str): name of cue
        """
        cue = self._dna_parent._create(name=name,
                                       parent=self._id,
                                       entity_type=DNA.TYPE_CUE,
                                       factory=Cue)

        return cue

    def insert(self, index, name="Untitled Cue"):
        """Create cue and insert at given index

        Args:
            name (str): name of cue
            index (int): position index
        """
        pass

    def remove(self, cue_id):
        """Remove entity by id

        Args:
            cue_id (int): DNA entity id
        """
        self._dna_parent._remove(cue_id)

    @staticmethod
    def from_sqlite(parent, row):
        """Parse entity from sqlite"""
        entity = Cuelist(parent=parent)
        entity._parse(row)

        return entity


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

    # private members
    _number = "1"
    _name = "Untitled cue"
    _color = COLOR_DEFAULT
    _pre_wait = 0
    _post_wait = 0
    _follow = FOLLOW_ON

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

    def __init__(self, parent):
        """Create a cue instance

        Args:
            parent (DNA): parent DNA
        """
        super(Cue, self).__init__(parent)

    def insert(self, index):
        """Create and insert a sub cue

        Args:
            index (int): position index
        """
        pass

    def append(self, name):
        """Create and append sub cue

        Args:
            name (str): name of sub cue
        """

        """Create a new cue and append to bottom"""
        cue = self._dna_parent._create(name=name,
                                       parent=self._id,
                                       entity_type=DNA.TYPE_CUE,
                                       factory=Cue)

        return cue

    def _parse(self, row):
        """Parse sqlite row"""
        super(Cue, self)._parse(row)

        self._follow = self.get("follow", self.FOLLOW_OFF)
        self._color = self.get("color", self.COLOR_DEFAULT)
        self._number = self.get("number", self.index)
        self._post_wait = self.get("post-wait", 0)
        self._pre_wait = self.get("pre-wait", 0)

    @staticmethod
    def from_sqlite(parent, row):
        """Parse entity from sqlite"""

        entity = Cue(parent=parent)
        entity._parse(row)

        return entity


class Settings(DNAEntity):
    """Settings object"""

    def __init__(self, parent):
        """Initialize Settings entity

        Args:
            parent (object): parent DNA
        """
        super(Settings, self).__init__(parent)

    @staticmethod
    def from_sqlite(parent, row):
        """Parse entity from sqlite"""
        entity = Settings(parent=parent)
        entity._parse(row)

        return entity

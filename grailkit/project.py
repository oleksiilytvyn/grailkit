# -*- coding: UTF-8 -*-
"""
    grailkit.project
    ~~~~~~~~~~~~~~~~

    Interface to Grail project files
"""
from grailkit.dna import DNA, DNAFile, DNAEntity


class ProjectError(Exception):
    """Base class for all project related exceptions"""
    pass


class Project(DNAFile):
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

    def __init__(self, file_path, create=False):
        """Open or create a project

        Args:
            file_path (str): path to file
            create (bool): create file if not exists
        """

        super(Project, self).__init__(file_path, create=create)

        entity = self._entities(filter_type=DNA.TYPE_SETTINGS,
                                filter_parent=self._id,
                                factory=Settings)

        if create and len(entity) == 0:
            self._create_project()

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

    def _create_project(self):
        # settings
        settings = self.create()
        settings.name = "settings"

        settings.set('display.background', '#000000')

        settings.set('display.text.align', 1)
        settings.set('display.text.valign', 1)
        settings.set('display.text.case', 'uppercase')

        settings.set('display.font.family', 'Helvetica')
        settings.set('display.font.size', '32pt')
        settings.set('display.font.weight', 'normal')
        settings.set('display.font.style', 'normal')
        settings.set('display.font.color', '#FFFFFF')

        settings.set('display.shadow.x', 0)
        settings.set('display.shadow.y', 2)
        settings.set('display.shadow.blur', 10)
        settings.set('display.shadow.color', '#000000')

        settings.set('display.padding.left', 10)
        settings.set('display.padding.right', 10)
        settings.set('display.padding.top', 10)
        settings.set('display.padding.bottom', 10)
        settings.set('display.padding.box', 10)

        settings.set('display.composition.x', 0)
        settings.set('display.composition.y', 0)
        settings.set('display.composition.width', 1920)
        settings.set('display.composition.height', 1080)

        settings.set('display.geometry.x', 1920)
        settings.set('display.geometry.y', 0)
        settings.set('display.geometry.width', 1920)
        settings.set('display.geometry.height', 1080)

        settings.set('display.disabled', False)
        settings.set('display.display', 'DISPLAY//2')
        settings.set('display.testcard', False)
        settings.set('display.fullscreen', True)
        settings.update()

        # project
        project = self.create()
        project.name = "Grail Project"
        project.set('author', 'Alex Litvin')
        project.set('description', 'Simple Grail project for testing purposes')
        project.update()

        # cuelist
        for cuelist_index in range(5):
            cuelist = self.create(parent=project.id)
            cuelist.name = "%d'st Cuelist" % (cuelist_index,)
            cuelist.set('color', '#FF0000')
            cuelist.set('description', 'Simple cuelist')
            cuelist.update()

            for cue_index in range(5):
                cue = self.create(parent=cuelist.id)
                cue.name = "Cue %d in list %d" % (cue_index, cuelist_index)
                cue.set('color', '#00FF00')
                cue.set('continue', 0)
                cue.set('wait_pre', 100)
                cue.set('wait_post', 30)
                cue.update()


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


class SettingsFile(DNA):
    """Represents a flat structure grail file with only properties"""

    def __init__(self, file_path, create=False):
        """Open or create a settings file

        Args:
            file_path (str): path to file
            create (bool): create file if not exists
        """

        super(SettingsFile, self).__init__(file_path, create=create)

    def has(self, key):
        """Check if property exists"""

        return self._has(0, key)

    def get(self, key, default=None):
        """Get a property value"""

        return self._get(0, key, default)

    def set(self, key, value, force_type=None):
        """Set value of property"""

        result = self._set(0, key, value, force_type)
        self._db.commit()

        return result

    def properties(self):

        return self._properties(0)

    def unset(self, key):
        """Remove property"""

        result = self._unset(0, key)
        self._db.commit()

        return result

    def unset_all(self):
        """Remove all properties"""
        
        result = self._unset_all(0)
        self._db.commit()

        return result

    def rename(self, old_key, new_key):
        """Rename property key"""

        result = self._rename(0, old_key, new_key)
        self._db.commit()

        return result

# -*- coding: UTF-8 -*-
"""
    grailkit.project
    ~~~~~~~~~~~~~~~~

    Interface to Grail project files
"""
from grailkit.dna import DNA, DNAFile, CueEntity, CuelistEntity, SettingsEntity


class ProjectError(Exception):
    """Base class for all project related exceptions"""

    pass


class Project(DNAFile):
    """Representation of a project file"""

    _name = "Untitled project"
    _description = ""
    _author = ""
    _created = 0
    _modified = 0
    _id = 0

    @property
    def name(self):
        """Project name"""

        return self._name

    @name.setter
    def name(self, value):
        """Project name setter"""

        self._name = value

    @property
    def description(self):
        """Project description"""

        return self._description

    @description.setter
    def description(self, value):
        """Project description setter"""

        self._description = value

    @property
    def author(self):
        """Project author"""

        return self._author

    @author.setter
    def author(self, value):
        """Project author setter"""

        self._author = value

    @property
    def created(self):
        """Date on witch project was created"""

        return self._created

    @property
    def modified(self):
        """Date of last edit on project"""

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
                                factory=SettingsEntity)

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
                                factory=SettingsEntity)

        if len(entity) == 0:
            entity = self._create(name="Settings",
                                  parent=self._id,
                                  entity_type=DNA.TYPE_SETTINGS,
                                  factory=SettingsEntity)
            return entity

        return entity[0]

    def cuelists(self):
        """Get all cuelists in project"""
        return self._entities(filter_type=DNA.TYPE_CUELIST,
                              filter_parent=self._id,
                              factory=CuelistEntity)

    def cuelist(self, cuelist_id):
        """Get a cuelist"""
        return self._entity(cuelist_id, factory=CuelistEntity)

    def remove(self, cuelist_id):
        """Remove a cuelist"""
        return self._remove(cuelist_id)

    def append(self, name="Untitled cuelist"):
        """Create a cuelist"""
        cuelist = self._create(name=name,
                               parent=self._id,
                               entity_type=DNA.TYPE_CUELIST,
                               factory=CuelistEntity)

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

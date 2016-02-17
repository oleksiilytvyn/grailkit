#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

from grailkit.db import DataBaseHost


class DNAError(Exception):
    """Base class for DNA errors"""
    pass


class DNA:
    """Base class for parsing grail file,
    use this class whe you don't want to show public methods.
    Otherwise use DNAFile class.
    """

    # database handler
    _db = None
    # create file from this query
    _db_create_query = """
        DROP TABLE IF EXISTS properties;
        CREATE TABLE properties(entity INT, key TEXT, value TEXT, type INT);

        DROP TABLE IF EXISTS entities;
        CREATE TABLE entities(id INT PRIMARY KEY, parent INT, type INT, name TEXT,
                              created INT, modified INT, content BLOB, search TEXT);
        """
    # file extension
    _file_extension = ".grail"

    def __init__(self, file_path, create=False):
        """Open a *.grail file

        Args:
            file_path (str): path to file
            create (bool): create file if not exists

        Raises:
            GrailFileError: if file can't be parsed or not exists
        """

        if not self.validate(file_path) and not create:
            raise DNAError("Grail file could not be opened.")
        else:
            self._db = DataBaseHost.get(file_path, query=self._db_create_query, create=create)

    def _entity(self, entity_id):
        """Get entity by `entity_id`

        Args:
            entity_id (int): id of an entity

        Returns:
            DNAEntity with id `entity_id`
        """
        return DNAEntity()

    def _entities(self):
        """Get list of all entities

        Returns:
            list of all entities available
        """
        return []

    def _add(self, entity):
        """Add new entity

        Args:
            entity: DNAEntity object

        Returns:
            updated entity object with assigned id
        """
        return DNAEntity()

    def _remove(self, entity_id):
        """Remove entity by id

        Args:
            entity_id (int): id of an entity
        """
        pass

    def _entity_has_childs(self, entity_id):
        """Check entity child nodes

        Args:
            entity_id (int): id of an entity

        Returns:
            True if entity has child nodes
        """
        return False

    def _entity_childs(self, entity_id):
        """Get child nodes of entity

        Args:
            entity_id (id): id of an entity

        Returns:
            list of child entities
        """
        return []

    def _property(self, entity_id, key, value=None, default=None, force_type=None):
        """Wrap property getter and setter methods

        Args:
            entity_id (int): id of an entity
            key (str): name of property
            value (object): value to assign to property
            default (object): value returned if property is not existed
            force_type (object): set a type of property
        Returns:
            property of an entity
        """
        return default

    def _get_property(self, entity_id, key, default=None):
        """Get property of entity with id `entity_id` and property name `key`

        Args:
            entity_id (int): id of an entity
            key (str): name of property
            default (object): value returned if property is not existed

        Returns:
            Value of property of an entity
        """
        return default

    def _set_property(self, entity_id, key, value, force_type=None):
        """Set a property value of an entity

        Args:
            entity_id (int): id of an entity
            key (str): name of property
            value (object): value to assign to property
            force_type (object): set a type of property
        """
        pass

    def _has_property(self, entity_id, key):
        """Check property existence

        Args:
            entity_id (int): id of an entity
            key (str): name of property

        Returns:
            True if property exists
        """
        pass

    def _properties(self, entity_id):
        """Get list of all properties linked to entity

        Args:
            entity_id (int): id of an entity

        Returns:
            properties list of an entity
        """
        return []

    def _remove_property(self, entity_id, key):
        """Remove property of an entity

        Args:
            entity_id (int): id of an entity
            key (str): name of property

        Returns:
            True if property removed
        """
        return True

    def _remove_properties(self, entity_id):
        """Remove all properties of an entity

        Args:
            entity_id (int): id of an entity

        Returns:
            True if properties was removed
        """
        return True

    def validate(self, file_path):
        """Validate file to be proper grail file

        Args:
            file_path (str): path to file
        """
        if not os.path.isfile(file_path):
            return False

        # if file doesn't have proper extension
        if os.path.splitext(file_path)[1] != self._file_extension:
            return False

        return True


class DNAFile(DNA):
    """Grail file parser"""

    def __init__(self, file_path, create=False):
        """Open a grail file

        Args:
            file_path (str): path to grail file
            create (bool): create file if not exists
        """
        super(DNAFile, self).__init__(file_path, create=create)

        # entities
        self.entity = self._entity
        self.entities = self._entities
        self.add = self._add
        self.remove = self._remove
        self.entity_childs = self._entity_childs
        self.entity_has_childs = self._entity_has_childs

        # properties
        self.property = self._property
        self.has_property = self._has_property
        self.get_property = self._get_property
        self.set_property = self._set_property
        self.properties = self._properties
        self.remove_property = self._remove_property
        self.remove_properties = self._remove_properties


class DNAEntity:
    """Basic entity model, each entity can have many properties + some default fields"""

    TYPE_DEFAULT = 0
    TYPE_PROJECT = 1
    TYPE_LIBRARY = 2
    TYPE_BIBLE = 3
    TYPE_CUE = -1
    TYPE_FILE = -1

    def __init__(self):
        pass

    # properties
    def get(self, key, type=None):
        return ""

    def set(self, key, value, type=None):
        pass

    def has(self, key):
        return True

    def remove(self, key):
        pass

    # fields
    @property
    def id(self):
        return 0

    @property
    def parent(self):
        return 0

    @property
    def name(self):
        return ""

    @property
    def type(self):
        return ""

    @type.setter
    def type(self, type):
        pass

    @property
    def created(self):
        return 0

    @property
    def modified(self):
        return 0

    @property
    def content(self):
        return ""

    @content.setter
    def content(self, content):
        pass

    @property
    def search(self):
        return ""

    @property
    def keywords(self):
        pass

    @keywords.setter
    def keywords(self, keywords):
        pass

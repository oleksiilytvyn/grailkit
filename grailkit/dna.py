#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import json
import time
import sqlite3 as lite

from grailkit.db import DataBaseHost, DataBaseError


class DNAError(DataBaseError):
    """Base class for DNA errors"""
    pass


class DNA:
    """Base class for parsing grail file,
    use this class when you don't want to show public methods.
    Otherwise use DNAFile class.
    """

    # database handler
    _db = None
    # create file from this query
    _db_create_query = """
        DROP TABLE IF EXISTS properties;
        CREATE TABLE properties(entity INT, key TEXT, value TEXT, type INT);

        DROP TABLE IF EXISTS entities;
        CREATE TABLE entities(id INTEGER PRIMARY KEY AUTOINCREMENT, parent INT, type INT, name TEXT,
                              created INT, modified INT, content BLOB, search TEXT, sort_order INT);
        """
    # file extension
    _file_extension = ".grail"

    def __init__(self, file_path, create=False):
        """Open a *.grail file

        Args:
            file_path (str): path to file
            create (bool): create file if not exists

        Raises:
            DNAError: if file can't be parsed or not exists
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

        return self._db.get("""SELECT id, parent, type, name, created, modified, content, search, sort_order
                            FROM entities WHERE id = ?""", (entity_id,),
                            factory=DNAEntity.from_sqlite)

    def _entities(self):
        """Get list of all entities

        Returns:
            list of all entities available
        """

        return self._db.all("""SELECT id, parent, type, name, created, modified, content, search, sort_order
                            FROM entities ORDER BY sort_order ASC""",
                            factory=DNAEntity.from_sqlite)

    def _add(self, entity):
        """Add new entity

        Args:
            entity: DNAEntity object

        Returns:
            updated entity object with assigned id
        """
        cursor = self._db.cursor
        cursor.execute("""INSERT INTO entities
                            (id, parent, type, name, created, modified, content, search, sort_order)
                            VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (entity.parent, entity.type, entity.name, entity.created, entity.modified,
                        json.dumps(entity.content, separators=(',', ':')), entity.search, entity.index))
        self._db.connection.commit()

        return cursor.lastrowid

    def _update(self):
        pass

    def _remove(self, entity_id):
        """Remove entity by id

        Args:
            entity_id (int): id of an entity
        """
        self._db.execute("DELETE FROM entities WHERE id = ?", (entity_id,))
        self._db.execute("DELETE FROM properties WHERE entity = ?", (entity_id,))

        for child in self._entity_childs(entity_id):
            self._remove(child.id)

    def _entity_has_childs(self, entity_id):
        """Check entity child nodes

        Args:
            entity_id (int): id of an entity

        Returns:
            True if entity has child nodes
        """
        parent = self._db.get("SELECT id FROM entities WHERE parent = ?", (entity_id,))

        return not not parent

    def _entity_childs(self, entity_id):
        """Get child nodes of entity

        Args:
            entity_id (id): id of an entity

        Returns:
            list of child entities
        """
        entities = self._db.all("""SELECT id, parent, type, name, created, modified, content, search, sort_order
                                FROM entities
                                WHERE parent = ?
                                ORDER BY sort_order ASC""", (entity_id,),
                                factory=DNAEntity.from_sqlite)

        return entities

    def _get_property(self, entity_id, key, default=None):
        """Get property of entity with id `entity_id` and property name `key`

        Args:
            entity_id (int): id of an entity
            key (str): name of property
            default (object): value returned if property is not existed

        Returns:
            Value of property of an entity
        """

        value = self._db.get("SELECT value FROM `properties` WHERE `entity` = ? AND `key` = ?", (entity_id, key))

        # TO-DO: add type handling
        return value[0] if value else default

    def _set_property(self, entity_id, key, value, force_type=0):
        """Set a property value of an entity

        Args:
            entity_id (int): id of an entity
            key (str): name of property
            value (object): value to assign to property
            force_type (object): set a type of property
        """
        self._db.execute("INSERT OR IGNORE INTO properties(entity, key, value, type) VALUES(?, ?, ?, ?)",
                         (entity_id, key, value, force_type))
        self._db.execute("UPDATE properties SET entity = ?, key = ?, value = ?, type = ? WHERE entity = ? AND key = ?",
                         (entity_id, key, value, force_type, entity_id, key))

        return self._db.cursor.lastrowid

    def _has_property(self, entity_id, key):
        """Check property existence

        Args:
            entity_id (int): id of an entity
            key (str): name of property

        Returns:
            True if property exists
        """

        value = self._db.get("SELECT value FROM `properties` WHERE `entity` = ? AND `key` = ?",
                             (entity_id, key))

        return not not value

    def _properties(self, entity_id):
        """Get list of all properties linked to entity

        Args:
            entity_id (int): id of an entity

        Returns:
            properties list of an entity
        """

        props = self._db.all("SELECT key, value FROM `properties` WHERE `entity` = ?", (entity_id,))

        # TO-DO: add type handling
        return props

    def _remove_property(self, entity_id, key):
        """Remove property of an entity

        Args:
            entity_id (int): id of an entity
            key (str): name of property
        """

        self._db.execute("DELETE FROM properties WHERE entity = ? AND key = ?", (entity_id, key))

    def _remove_properties(self, entity_id):
        """Remove all properties of an entity

        Args:
            entity_id (int): id of an entity
        """
        self._db.execute("DELETE FROM properties WHERE entity = ?", (entity_id,))

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

        try:
            db = DataBaseHost.get(file_path)
            db.all("SELECT name FROM sqlite_master WHERE type='table'")
        except lite.DatabaseError:
            return False

        return True

    def close(self):
        """Close connection"""
        self._db.close()


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
        self.has_property = self._has_property
        self.get_property = self._get_property
        self.set_property = self._set_property
        self.properties = self._properties
        self.remove_property = self._remove_property
        self.remove_properties = self._remove_properties


class DNAEntity:
    """Basic entity model, each entity can have many properties + some default fields"""

    TYPE_ABSTRACT = 0
    TYPE_PROJECT = 1
    TYPE_LIBRARY = 2
    TYPE_BIBLE = 3
    TYPE_CUE = 4
    TYPE_FILE = 5

    TYPES = (
        TYPE_ABSTRACT,
        TYPE_PROJECT,
        TYPE_LIBRARY,
        TYPE_BIBLE,
        TYPE_CUE,
        TYPE_FILE)

    def __init__(self):
        """ """
        self._id = 0
        self._type = None
        self._name = ""
        self._parent = 0
        self._search = ""
        self._content = None
        self._created = int(round(time.time() * 1000))
        self._modified = 0
        self._index = 0

    def __len__(self):
        """
        Returns:
            number of child entities
        """
        pass

    def __iter__(self):
        """Iterate over child items"""
        pass

    def __reversed__(self):
        """Reversed iterator"""
        pass

    # fields
    @property
    def id(self):
        """Entity identifier"""
        return self._id

    @property
    def parent(self):
        """Parent identifier"""
        return self._parent

    @parent.setter
    def parent(self, parent):
        """Set parent identifier"""
        self._parent = parent

    @property
    def name(self):
        """Name of entity"""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def type(self):
        """Entity type"""
        return self._type

    @type.setter
    def type(self, arg_type):
        """Set type of entity

        Args:
            arg_type: type of entity
        """
        self._type = arg_type

    @property
    def created(self):
        """Time in milliseconds when entity was created"""
        return self._created

    @property
    def modified(self):
        """Time in milliseconds when entity was modified last time"""
        return self._modified

    @property
    def content(self):
        """Get contents of item"""
        return self._content

    @content.setter
    def content(self, content):
        """Set content of item"""
        self._content = content

    @property
    def search(self):
        """Search string"""
        return self._search

    @property
    def index(self):
        """Index of entity inside parent entity"""
        return self._index

    @search.setter
    def search(self, value):
        """Search string"""
        self._search = value

    # properties
    def get_property(self, key, default=None):
        return default

    def set_property(self, key, value, type=None):
        pass

    def has_property(self, key):
        return True

    def remove_property(self, key):
        pass

    def items(self):
        """Get list of sub cues

        Returns:
            list of child cues
        """
        return []

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

    def _parse(self, cursor, row):
        """
        Args:
            cursor (sqlite3.Cursor): cursor object
            row (sqlite3.Row): row object
        """

        self._id = row[0]
        self._parent = row[1]
        self._type = row[2]
        self._name = row[3]
        self._created = row[4]
        self._modified = row[5]
        self._content = row[6]
        self._search = row[7]
        self._index = row[8]

    @staticmethod
    def from_sqlite(cursor, row):
        entity = DNAEntity()
        entity._parse(cursor, row)

        return entity

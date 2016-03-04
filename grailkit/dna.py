# -*- coding: UTF-8 -*-

import os
import json
import time
import sqlite3 as lite

from grailkit.db import DataBaseHost, DataBaseError


def millis_now():
    """Returns time in milliseconds since epoch"""
    return int(round(time.time() * 1000))


class DNAError(DataBaseError):
    """Base class for DNA errors"""
    pass


class DNA:
    """Base class for parsing grail file,
    use this class when you don't want to show public methods.
    Otherwise use DNAFile class.
    """

    TYPE_BOOL = 1
    TYPE_INT = 2
    TYPE_FLOAT = 3
    TYPE_STRING = 4
    TYPE_JSON = 6

    _SUPPORTED_TYPES = (TYPE_BOOL, TYPE_INT, TYPE_FLOAT, TYPE_STRING, TYPE_JSON)

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

    def _create(self):
        """Returns new DNAEntity inside this DNA file"""
        return DNAEntity(self)

    def _entity(self, entity_id):
        """Get entity by `entity_id`

        Args:
            entity_id (int): id of an entity

        Returns:
            DNAEntity with id `entity_id`
        """
        raw_entity = self._db.get("""SELECT id, parent, type, name, created, modified, content, search, sort_order
                            FROM entities WHERE id = ?""", (entity_id,))

        return DNAEntity.from_sqlite(self, raw_entity)

    def _entities(self):
        """Get list of all entities

        Returns:
            list of all entities available
        """

        raw_entities = self._db.all("""SELECT id, parent, type, name, created, modified, content, search, sort_order
                            FROM entities ORDER BY sort_order ASC""")

        entities = []

        for raw in raw_entities:
            entities.append(DNAEntity.from_sqlite(self, raw))

        return entities

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
        raw_entities = self._db.all("""SELECT id, parent, type, name, created, modified, content, search, sort_order
                                FROM entities
                                WHERE parent = ?
                                ORDER BY sort_order ASC""", (entity_id,))

        entities = []

        for raw in raw_entities:
            entities.append(DNAEntity.from_sqlite(self, raw))

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

        value = self._db.get("SELECT value, type FROM `properties` WHERE `entity` = ? AND `key` = ?", (entity_id, key))

        return self._read_type(value[0], value[1]) if value else default

    def _set_property(self, entity_id, key, value, force_type=None):
        """Set a property value of an entity

        Args:
            entity_id (int): id of an entity
            key (str): name of property
            value (object): value to assign to property
            force_type (DNA.TYPE): set a type of property
        """

        if force_type is None:
            force_type = self._get_type(value)
        elif force_type not in self._SUPPORTED_TYPES:
            raise DNAError("Property type not supported")

        value = self._write_type(value, force_type)

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

        raw_props = self._db.all("SELECT key, value, type FROM `properties` WHERE `entity` = ?", (entity_id,))
        props = {}

        for prop in raw_props:
            props[prop[0]] = self._read_type(prop[1], prop[2])

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

    def _get_type(self, value):

        builtin_type = type(value)
        arg_type = None

        if builtin_type == str:
            arg_type = self.TYPE_STRING
        elif builtin_type == int:
            arg_type = self.TYPE_INT
        elif builtin_type == float:
            arg_type = self.TYPE_FLOAT
        elif builtin_type == bool:
            arg_type = self.TYPE_BOOL
        elif builtin_type == dict or builtin_type == list:
            arg_type = self.TYPE_JSON

        return arg_type

    def _write_type(self, arg_value, arg_type):

        value = ""

        if arg_type is self.TYPE_JSON:
            value = json.dumps(arg_value)
        elif arg_type in self._SUPPORTED_TYPES and arg_type is not self.TYPE_JSON:
            value = str(arg_value)

        return value

    def _read_type(self, arg_value, arg_type):

        if arg_type is self.TYPE_JSON:
            arg_value = json.loads(arg_value)
        elif arg_type is self.TYPE_INT:
            arg_value = int(arg_value)
        elif arg_type is self.TYPE_FLOAT:
            arg_value = float(arg_value)
        elif arg_type is self.TYPE_BOOL:
            arg_value = bool(arg_value)

        return arg_value

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
        self.create = self._create
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

    # enumerate all types
    TYPES = (
        TYPE_ABSTRACT,
        TYPE_PROJECT,
        TYPE_LIBRARY,
        TYPE_BIBLE,
        TYPE_CUE,
        TYPE_FILE)

    def __init__(self, parent=None):
        """ """
        self._id = 0
        self._type = None
        self._name = ""
        self._parent = 0
        self._search = ""
        self._content = None
        self._created = millis_now()
        self._modified = 0
        self._index = 0

        self._dna_parent = parent

        if parent is None:
            raise DNAError("DNAEntity cannot be created without parent")

    def __len__(self):
        """
        Returns:
            number of child entities
        """
        return 0

    def __iter__(self):
        """Iterate over child items"""
        return iter([])

    # fields
    @property
    def id(self):
        """Entity identifier"""
        return self._id

    @property
    def parent_id(self):
        """Parent identifier"""
        return self._parent

    @parent_id.setter
    def parent_id(self, parent):
        """Set parent identifier"""
        self._parent = parent
        self._modified = millis_now()

    @property
    def name(self):
        """Name of entity"""
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self._modified = millis_now()

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
        self._modified = millis_now()

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
        self._modified = millis_now()

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
        self._modified = millis_now()

    def _parse(self, row):
        """Parse sqlite row into DNAEntity

        Args:
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
    def from_sqlite(parent, row):
        entity = DNAEntity(parent=parent)
        entity._parse(row)

        return entity

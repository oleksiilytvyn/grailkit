# -*- coding: UTF-8 -*-
"""
    grailkit.dna
    ~~~~~~~~~~~~

    Implementation of grail file format.
    This file format used for all internal grail data.
"""
import os
import json
import sqlite3 as lite

from grailkit.db import DataBaseHost, DataBaseError
from grailkit.util import millis_now


class DNAError(DataBaseError):
    """Base class for DNA errors"""

    pass


class DNA:
    """Base class for parsing grail file,
    use this class when you don't want to show public methods.
    Otherwise use DNAFile class.
    """

    # property types
    ARG_BOOL = 1
    ARG_INT = 2
    ARG_FLOAT = 3
    ARG_STRING = 4
    ARG_JSON = 6

    # list all supported types
    _SUPPORTED_TYPES = (ARG_BOOL, ARG_INT, ARG_FLOAT, ARG_STRING, ARG_JSON)

    # types of entities
    TYPE_ABSTRACT = 0
    TYPE_BIBLE = 1
    TYPE_PROJECT = 2
    TYPE_SETTINGS = 3
    TYPE_CUELIST = 4
    TYPE_CUE = 5
    TYPE_LIBRARY = 6
    TYPE_LIBRARY_ITEM = 7
    TYPE_FILE = 8
    TYPE_SONG = 9

    # enumerate all types of entities
    TYPES = (
        TYPE_ABSTRACT,
        TYPE_PROJECT,
        TYPE_LIBRARY,
        TYPE_LIBRARY_ITEM,
        TYPE_BIBLE,
        TYPE_CUE,
        TYPE_FILE,
        TYPE_SETTINGS,
        TYPE_SONG)

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

        self._changed = False
        self._location = file_path

        if not file_path or not self.validate(file_path) and not create:
            raise DNAError("Grail file could not be opened.")
        else:
            self._db = DataBaseHost.get(file_path, query=self._db_create_query, create=create)

    @property
    def location(self):
        """Returns path to file"""
        return self._location

    @property
    def filename(self):
        """Returns path to file"""
        return os.path.splitext(os.path.basename(self._location))[0]

    @property
    def changed(self):
        """Return True if some changes not saved"""
        return self._changed

    def _create(self, name="", parent=0, entity_type=TYPE_ABSTRACT, index=0, factory=None):
        """Returns new DNAEntity inside this DNA file"""

        self._changed = True

        entity = DNAEntity(self)
        entity.parent = parent
        entity.type = entity_type
        entity.index = index
        entity.name = name

        cursor = self._db.cursor
        cursor.execute("""INSERT INTO entities
                            (id, parent, type, name, created, modified, content, search, sort_order)
                            VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (entity.parent, entity.type, entity.name, entity.created, entity.modified,
                        json.dumps(entity.content, separators=(',', ':')), entity.search, entity.index))
        self._db.connection.commit()

        return self._entity(cursor.lastrowid, factory)

    def _entity(self, entity_id, factory=None):
        """Get entity by `entity_id`

        Args:
            entity_id (int): id of an entity
            factory: use another class to create entity

        Returns:
            DNAEntity with id `entity_id`
        """
        raw_entity = self._db.get("""SELECT id, parent, type, name, created, modified, content, search, sort_order
                            FROM entities WHERE id = ?""", (entity_id,))

        if factory:
            return factory.from_sqlite(self, raw_entity)
        else:
            return DNAEntity.from_sqlite(self, raw_entity)

    def _update(self, entity):
        """update entity"""

        self._changed = True

        cursor = self._db.cursor
        cursor.execute("""UPDATE entities SET
                        id = ?, parent = ?, type = ?, name = ?, created = ?, modified = ?, content = ?, search = ?,
                        sort_order = ?
                        WHERE id = ?""",
                       (entity.id, entity.parent_id, entity.type, entity.name, entity.created, entity.modified,
                        json.dumps(entity.content, separators=(',', ':')), entity.search, entity.index, entity.id))

    def _remove(self, entity_id):
        """Remove entity by id

        Args:
            entity_id (int): id of an entity
        """
        self._changed = True

        self._db.execute("DELETE FROM entities WHERE id = ?", (entity_id,))
        self._db.execute("DELETE FROM properties WHERE entity = ?", (entity_id,))
        self._db.connection.commit()

        for child in self._childs(entity_id):
            self._remove(child.id)

    def _entities(self, filter_type=False, filter_parent=False, filter_keyword=False, factory=None):
        """Get list of all entities

        Returns:
            list of all entities available
        """

        where = ""
        args = []

        if filter_keyword:
            keyword = filter_keyword.lstrip().rstrip().lower()
            where = """lowercase(name) LIKE lowercase(?)
                    OR lowercase(search) LIKE lowercase(?)"""
            args.append(keyword)
            args.append(keyword)

        if filter_type is not False or filter_parent is not False:
            where += "WHERE"

        if filter_parent is not False:
            where += " parent = ?" + (" AND " if filter_type else "")
            args.append(filter_parent)

        if filter_type is not False:
            where += " type = ?"
            args.append(filter_type)

        raw_entities = self._db.all(
            """SELECT id, parent, type, name, created, modified, content, search, sort_order
               FROM entities
               %s
               ORDER BY sort_order ASC""" % (where,), args)

        return self.__factory(factory, raw_entities)

    def _has_childs(self, entity_id):
        """Check entity child nodes

        Args:
            entity_id (int): id of an entity

        Returns:
            True if entity has child nodes
        """
        parent = self._db.get("SELECT id FROM entities WHERE parent = ?", (entity_id,))

        return not not parent

    def _childs(self, entity_id, factory=None):
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

        return self.__factory(factory, raw_entities)

    def _get(self, entity_id, key, default=None):
        """Get property of entity with id `entity_id` and property name `key`

        Args:
            entity_id (int): id of an entity
            key (str): name of property
            default (object): value returned if property is not existed

        Returns:
            Value of property of an entity
        """

        value = self._db.get("SELECT value, type FROM `properties` WHERE `entity` = ? AND `key` = ?", (entity_id, key))

        return self.__read_type(value[0], value[1]) if value else default

    def _set(self, entity_id, key, value, force_type=None):
        """Set a property value of an entity

        Args:
            entity_id (int): id of an entity
            key (str): name of property
            value (object): value to assign to property
            force_type (DNA.TYPE): set a type of property
        """
        self._changed = True

        if force_type is None:
            force_type = self.__get_type(value)
        elif force_type not in self._SUPPORTED_TYPES:
            raise DNAError("Property type not supported")

        value = self.__write_type(value, force_type)

        self._db.execute("INSERT OR IGNORE INTO properties(entity, key, value, type) VALUES(?, ?, ?, ?)",
                         (entity_id, key, value, force_type))
        self._db.execute("UPDATE properties SET entity = ?, key = ?, value = ?, type = ? WHERE entity = ? AND key = ?",
                         (entity_id, key, value, force_type, entity_id, key))

        return self._db.cursor.lastrowid

    def _has(self, entity_id, key):
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
            props[prop[0]] = self.__read_type(prop[1], prop[2])

        return props

    def _unset(self, entity_id, key):
        """Remove property of an entity

        Args:
            entity_id (int): id of an entity
            key (str): name of property
        """
        self._changed = True

        self._db.execute("DELETE FROM properties WHERE entity = ? AND key = ?", (entity_id, key))

    def _unset_all(self, entity_id):
        """Remove all properties of an entity

        Args:
            entity_id (int): id of an entity
        """
        self._changed = True

        self._db.execute("DELETE FROM properties WHERE entity = ?", (entity_id,))

    def _rename(self, entity_id, old_key, new_key):
        """Rename property key

        Args:
            entity_id (int): id of an entity
            old_key (str): old property key
            new_key (str): new property key
        """

        self._changed = True

        self._db.execute("UPDATE properties SET key = ? WHERE entity = ? AND key = ?",
                         (new_key, entity_id, old_key))

    def __get_type(self, value):

        builtin_type = type(value)
        arg_type = None

        if builtin_type == str:
            arg_type = self.ARG_STRING
        elif builtin_type == int:
            arg_type = self.ARG_INT
        elif builtin_type == float:
            arg_type = self.ARG_FLOAT
        elif builtin_type == bool:
            arg_type = self.ARG_BOOL
        elif builtin_type == dict or builtin_type == list:
            arg_type = self.ARG_JSON

        return arg_type

    def __write_type(self, arg_value, arg_type):

        value = ""

        if arg_type is self.ARG_JSON:
            value = json.dumps(arg_value)
        elif arg_type in self._SUPPORTED_TYPES and arg_type is not self.ARG_JSON:
            value = str(arg_value)

        return value

    def __read_type(self, arg_value, arg_type):

        if arg_type is self.ARG_JSON:
            arg_value = json.loads(arg_value)
        elif arg_type is self.ARG_INT:
            arg_value = int(arg_value)
        elif arg_type is self.ARG_FLOAT:
            arg_value = float(arg_value)
        elif arg_type is self.ARG_BOOL:
            arg_value = bool(arg_value)

        return arg_value

    def __factory(self, factory, raw_entities):
        """Return list of entities created by factory from raw_entities"""

        entities = []

        # TO-DO: optimise it by using real sqlite factory
        if factory:
            for raw in raw_entities:
                entities.append(factory.from_sqlite(self, raw))
        else:
            for raw in raw_entities:
                entities.append(DNAEntity.from_sqlite(self, raw))

        return entities

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

    def save(self):
        """Save all changes"""

        self._db.commit()
        self._changed = False

    def save_copy(self, file_path):
        """Save a copy of this file"""

        self._db.commit()
        self._changed = False
        self._db.copy(file_path)

    def close(self):
        """Close connection"""

        self._db.close()
        self._changed = False


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
        self.update = self._update
        self.remove = self._remove
        self.childs = self._childs
        self.has_childs = self._has_childs

        # properties
        self.has = self._has
        self.get = self._get
        self.set = self._set
        self.properties = self._properties
        self.unset = self._unset
        self.unset_all = self._unset_all
        self.rename = self._rename


class SettingsFile(DNA):
    """Represents a grail file with properties only"""

    def __init__(self, file_path, create=False):
        """Open or create a settings file

        Args:
            file_path (str): path to file
            create (bool): create file if not exists
        """

        super(SettingsFile, self).__init__(file_path, create=create)

    def has(self, key):
        """Check if property exists

        Args:
            key (str): property key
        Returns: True if property exists
        """

        return self._has(0, key)

    def get(self, key, default=None):
        """Get a property value

        Args:
            key (str): property key
            default (object): Object that will be returned if property doesn't exists
        Returns: property value or default if isn't exists
        """

        return self._get(0, key, default)

    def set(self, key, value, force_type=None):
        """Set value of property

        Args:
            key (str): property key
            value (object): property value object
            force_type: If set to not None, value with this type will be saved
        Returns: True if operation is succeeded
        """

        result = self._set(0, key, value, force_type)
        self._db.commit()

        return result

    def properties(self):
        """Get a all properties

        Returns: dist object of all properties
        """

        return self._properties(0)

    def unset(self, key):
        """Remove property by key value

        Args:
            key (str): property key
        Returns: True if operation is succeeded
        """

        result = self._unset(0, key)
        self._db.commit()

        return result

    def unset_all(self):
        """Remove all properties

        Returns: True if operation succeeded"""

        result = self._unset_all(0)
        self._db.commit()

        return result

    def rename(self, old_key, new_key):
        """Rename property key

        Returns: True if operation is succeeded
        """

        result = self._rename(0, old_key, new_key)
        self._db.commit()

        return result


class DNAEntity:
    """Basic entity model, each entity can have many properties + some default fields"""

    def __init__(self, parent):
        """Entity representation inside DNA

        Args:
            parent (DNA): parent DNA object
        """

        self._id = 0
        self._type = DNA.TYPE_ABSTRACT
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

    @search.setter
    def search(self, value):
        """Search string"""

        self._search = value
        self._modified = millis_now()

    @property
    def index(self):
        """Index of entity inside parent entity"""

        return self._index

    @index.setter
    def index(self, value):
        """Set index of entity

        Args:
            value (int): index value
        """

        self._index = value
        self._modified = millis_now()

    def get(self, key, default=None):
        """Get a property value

        Args:
            key (str): property name
            default (object): return `default` if property doesn't exists
        """

        return self._dna_parent._get(self.id, key, default)

    def set(self, key, value, force_type=None):
        """Set a property

        Args:
            key (str): property name
            value (object): value of property
            force_type: convert value to this type
        """

        self._dna_parent._set(self.id, key, value, force_type)

    def has(self, key):
        """Check if property exists

        Args:
            key (str): property name
        """

        return self._dna_parent._has(self.id, key)

    def unset(self, key):
        """Remove property

        Args:
            key (str): property name
        """

        self._dna_parent._unset(self.id, key)

    def properties(self):
        """Returns list of all properties"""

        return self._dna_parent._properties(self.id)

    def update(self):
        """Update this entity and commit changes to database"""

        self._dna_parent._update(self)

    def _parse(self, row):
        """Parse sqlite row into DNAEntity

        Args:
            row (sqlite3.Row): row object
        """

        self._id = int(row[0])
        self._parent = int(row[1])
        self._type = int(row[2])
        self._name = row[3]
        self._created = int(row[4])
        self._modified = int(row[5])
        self._content = row[6]
        self._search = row[7]
        self._index = int(row[8])

    @staticmethod
    def from_sqlite(parent, row):
        """Parse entity from sqlite"""
        entity = DNAEntity(parent=parent)
        entity._parse(row)

        return entity


class SettingsEntity(DNAEntity):
    """Settings object"""

    def __init__(self, parent):
        """Initialize Settings entity

        Args:
            parent (object): parent DNA object
        """

        super(SettingsEntity, self).__init__(parent)

    @staticmethod
    def from_sqlite(parent, row):
        """Parse entity from sqlite"""

        entity = SettingsEntity(parent=parent)
        entity._parse(row)

        return entity


class SongEntity(DNAEntity):

    def __init__(self, parent):
        super(SongEntity, self).__init__(parent)

        # grail songs unique id
        self._uid = 0
        self._name = "Untitled"
        self._artist = "Unknown"
        self._album = "Unknown"
        self._artwork = None
        self._track = 1
        self._year = 0
        self._genre = "Unknown"
        self._language = "en"
        self._lyrics = ""

    @property
    def year(self):
        """Search string"""

        return self._year

    @year.setter
    def year(self, value):
        """year string"""

        self._year = value
        self._modified = millis_now()

    @property
    def artist(self):
        """Search string"""

        return self._artist

    @artist.setter
    def artist(self, value):
        """year string"""

        self._artist = value
        self._modified = millis_now()

    @property
    def album(self):
        """Search string"""

        return self._album

    @album.setter
    def album(self, value):
        """year string"""

        self._album = value
        self._modified = millis_now()

    @property
    def track(self):
        """Search string"""

        return self._track

    @track.setter
    def track(self, value):
        """year string"""

        self._track = value
        self._modified = millis_now()

    @property
    def genre(self):
        """Search string"""

        return self._genre

    @genre.setter
    def genre(self, value):
        """year string"""

        self._genre = value
        self._modified = millis_now()

    @property
    def language(self):
        """Search string"""

        return self.language

    @language.setter
    def language(self, value):
        """year string"""

        self._language = value
        self._modified = millis_now()

    @property
    def lyrics(self):
        """Search string"""

        return self._lyrics

    @lyrics.setter
    def lyrics(self, value):
        """year string"""

        self._lyrics = value
        self._modified = millis_now()

    def _parse(self, row):
        """Parse sqlite row into SongEntity

        Args:
            row (sqlite3.Row): row object
        """

        super(SongEntity, self)._parse(row)

        # parse contents into song info
        content = json.loads(self._content)

        self._year = content['year']
        self._track = content['track']
        self._album = content['album']
        self._artwork = None
        self._language = content['language']
        self._lyrics = content['lyrics']
        self._genre = content['genre']
        self._artist = content['artist']


class VerseEntity(DNAEntity):

    """Representation of bible verse"""

    pass

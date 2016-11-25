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

#
# Entities
#


class DNAEntity:
    """DNA entity definition class
    Each entity must have fields:
        id (int): identification number of entity;
        type (int): type of entity;
        name (str): name or label of entity;
        parent (int): parent entity identifier;
        search (str): string field that contains info for search;
        content (json): content of entity, can be uniform;
        created (int): time when entity is created;
        modified (int): time whe entity was last time modified;
        index (int): index of entity, in case of ordered lists of entities;
    """

    def __init__(self, parent):
        """Entity representation inside DNA

        Args:
            parent (DNA): parent DNA object
        """

        if parent is None:
            raise DNAError("DNAEntity can't be created without parent")

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
        """Name of entity"""

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

    def remove(self):
        """Remove this entity"""

        self._dna_parent._remove(self._id)

    def _parse(self, row):
        """Parse sqlite row into DNAEntity

        Args:
            row (sqlite3.Row): row object
        """

        self._id = int(row[0])
        self._parent = int(row[1])
        self._type = int(row[2])
        self._name = str(row[3])
        self._created = int(row[4])
        self._modified = int(row[5])
        self._content = row[6]
        self._search = str(row[7])
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
            parent (DNA): parent DNA object
        """

        super(SettingsEntity, self).__init__(parent)

    @staticmethod
    def from_sqlite(parent, row):
        """Parse entity from sqlite"""

        entity = SettingsEntity(parent=parent)
        entity._parse(row)

        return entity


class SongEntity(DNAEntity):
    """Representation of song inside Grail file"""

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

        self._year = int(value)
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

        self._track = int(value)
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

    def update(self):
        """Update song information"""

        self._search = "%s %s %s" % (self._lyrics, self._album, self._artist)
        self._content = {
            'year': self._year,
            'track': self._track,
            'album': self._album,
            'artwork': self._artwork,
            'language': self._language,
            'lyrics': self._lyrics,
            'genre': self._genre,
            'artist': self._artist
            }

        super(SongEntity, self).update()

    def _parse(self, row):
        """Parse sqlite row into SongEntity

        Args:
            row (sqlite3.Row): row object
        """

        super(SongEntity, self)._parse(row)

        # parse contents into song info
        content = json.loads(self._content)

        def json_key(obj, key, default=''):
            if obj:
                return obj[key] if key in obj else default
            else:
                return default

        self._year = int(json_key(content, 'year', 2000))
        self._track = int(json_key(content, 'track', 1))
        self._album = json_key(content, 'album', 'Unknown')
        self._artwork = None
        self._language = json_key(content, 'language', '')
        self._lyrics = json_key(content, 'lyrics', '')
        self._genre = json_key(content, 'genre', 'Unknown')
        self._artist = json_key(content, 'artist', 'Unknown')

    @staticmethod
    def from_sqlite(parent, row):
        """Parse entity from sqlite

        Args:
            parent: parent DNA object
            row: sqlite3 row object
        Returns: entity instance
        """

        entity = SongEntity(parent=parent)
        entity._parse(row)

        return entity


class FileEntity(DNAEntity):

    @staticmethod
    def from_sqlite(parent, row):
        """Parse entity from sqlite

        Args:
            parent: parent DNA object
            row: sqlite3 row object
        Returns: entity instance
        """

        entity = FileEntity(parent=parent)
        entity._parse(row)

        return entity


class CuelistEntity(DNAEntity):
    """Representation of cuelist"""

    def __init__(self, parent):
        """Create a cuelist"""
        super(CuelistEntity, self).__init__(parent)

    def __len__(self):
        """Return count of cues"""
        return len(self.cues())

    def cues(self):
        """Returns list of all cues in Cuelist"""

        return self._dna_parent._entities(filter_parent=self._id,
                                          filter_type=DNA.TYPE_CUE,
                                          factory=CueEntity)

    def cue(self, cue_id):
        """Get cue by id

        Args:
            cue_id (int): cue identifier
        """
        return self._dna_parent._entity(cue_id, factory=CueEntity)

    def append(self, name="Untitled Cue"):
        """Create a new cue and append to the end

        Args:
            name (str): name of cue
        """
        cue = self._dna_parent._create(name=name,
                                       parent=self._id,
                                       entity_type=DNA.TYPE_CUE,
                                       factory=CueEntity)

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
        entity = CuelistEntity(parent=parent)
        entity._parse(row)

        return entity


class CueEntity(DNAEntity):
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
        super(CueEntity, self).__init__(parent)

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

        # Create a new cue and append to bottom
        cue = self._dna_parent._create(name=name,
                                       parent=self._id,
                                       entity_type=DNA.TYPE_CUE,
                                       factory=CueEntity)

        return cue

    def _parse(self, row):
        """Parse sqlite row

        Args:
            row: sqlite3 row object
        """

        super(CueEntity, self)._parse(row)

        self._follow = self.get("follow", self.FOLLOW_OFF)
        self._color = self.get("color", self.COLOR_DEFAULT)
        self._number = self.get("number", self.index)
        self._post_wait = self.get("post-wait", 0)
        self._pre_wait = self.get("pre-wait", 0)

    @staticmethod
    def from_sqlite(parent, row):
        """Parse entity from sqlite

        Args:
            parent: parent DNA object
            row: sqlite3 row object
        Returns: entity instance
        """

        entity = CueEntity(parent=parent)
        entity._parse(row)

        return entity

#
# Files
#


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
    TYPE_BIBLE = 10
    TYPE_VERSE = 11
    TYPE_BOOK = 12
    TYPE_PROJECT = 20
    TYPE_SETTINGS = 21
    TYPE_CUELIST = 22
    TYPE_CUE = 23
    TYPE_LIBRARY = 24
    TYPE_FILE = 25
    TYPE_SONG = 26

    # enumerate all types of entities
    TYPES = (
        TYPE_ABSTRACT,
        TYPE_BIBLE,
        TYPE_VERSE,
        TYPE_BOOK,
        TYPE_PROJECT,
        TYPE_SETTINGS,
        TYPE_CUELIST,
        TYPE_CUE,
        TYPE_LIBRARY,
        TYPE_FILE,
        TYPE_SONG
        )

    TYPES_FACTORIES = {
        TYPE_ABSTRACT: DNAEntity,
        # TYPE_BIBLE: DNAEntity,
        # TYPE_VERSE: DNAEntity,
        # TYPE_BOOK: DNAEntity,
        # TYPE_PROJECT: DNAEntity,
        TYPE_SETTINGS: SettingsEntity,
        TYPE_CUELIST: CuelistEntity,
        TYPE_CUE: CueEntity,
        # TYPE_LIBRARY: DNAEntity,
        TYPE_FILE: FileEntity,
        TYPE_SONG: SongEntity
        }

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
        """Return True if changes not saved"""

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
            DNAEntity with id `entity_id` if entity exists otherwise returns Null
        """
        raw_entities = self._db.all("""SELECT id, parent, type, name, created, modified, content, search, sort_order
                            FROM entities WHERE id = ?""", (entity_id,))
        entities = self.__factory(factory, raw_entities)

        return entities[0] if len(entities) > 0 else None

    def _update(self, entity):
        """update entity

        Args:
            entity (DNAEntity): entity object
        """

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

    def _entities(self, filter_type=False, filter_parent=False, filter_keyword=False,
                  sort=False, reverse=False, offset=0, limit=0, factory=None):
        """Get list of all entities

        Args:
            filter_type (int): filter by type of entity
            filter_parent (int): filter by id of parent entity
            filter_keyword (str): filter by name
            sort (str): property to sort by
            reverse (bool): reverse order of items
            offset (int): offset a result set
            limit (int): limit result set
            factory (object): factory object

        Returns:
            list of all entities available
        """

        where = []
        args = []

        if filter_keyword:
            keyword = "%" + str(filter_keyword).lstrip().rstrip().lower() + "%"
            where.append(""" lowercase(name) LIKE lowercase(?)
                    OR lowercase(search) LIKE lowercase(?)""")
            args.append(keyword)
            args.append(keyword)

        if filter_parent is not False:
            where.append(" parent = ?")
            args.append(filter_parent)

        if filter_type is not False:
            where.append(" type = ?")
            args.append(filter_type)

        # To-do: implement item sorting

        sql = """
                SELECT id, parent, type, name, created, modified, content, search, sort_order
                FROM entities
                %s
                ORDER BY %s %s
                """ % ('WHERE' + ' AND '.join(where) if len(where) > 0 else '',
                       sort if isinstance(sort, str) else "sort_order",
                       "DESC" if reverse else "ASC")

        if limit > 0:
            sql += " LIMIT ? "
            args.append(limit)

        if offset > 0:
            sql += " OFFSET ? "
            args.append(offset)

        raw_entities = self._db.all(sql, args)

        return self.__factory(factory, raw_entities)

    def _has_childs(self, entity_id):
        """Check entity child nodes

        Args:
            entity_id (int): id of an entity

        Returns:
            True if entity has child nodes
        """
        parent = self._db.get("SELECT id FROM entities WHERE parent = ?", (entity_id,))

        return bool(parent)

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
        Returns:
            id of last inserted row
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

        return bool(value)

    def _properties(self, entity_id):
        """Get list of all properties linked to entity

        Args:
            entity_id (int): id of an entity

        Returns:
            properties list of an entity
        """

        # to-do: use factory to speed up this query
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
        """Get type of value

        Args:
            value: any object
        Returns:
            argument type
        """

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
        """Create a string representation of value given

        Args:
            arg_value: any object
            arg_type: type of object to convert to

        Returns:
            string representation of value
        """

        value = ""

        if arg_type is self.ARG_JSON:
            value = json.dumps(arg_value)
        elif arg_type in self._SUPPORTED_TYPES and arg_type is not self.ARG_JSON:
            value = str(arg_value)

        return value

    def __read_type(self, arg_value, arg_type):
        """Parse string from db into correct object

        Args:
            arg_value: raw value
            arg_type: value type

        Returns:
            object from raw value
        """

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
        """Return list of entities created by factory from raw_entities

        Args:
            factory: object from which entities will be created
            raw_entities: sqlite3 rows
        """

        entities = []

        # TO-DO: optimise it by using real sqlite factory
        if factory:
            for raw in raw_entities:
                entities.append(factory.from_sqlite(self, raw))
        else:
            for raw in raw_entities:
                factory_entity = self.__get_factory(raw['type'])
                entities.append(factory_entity.from_sqlite(self, raw))

        return entities

    def __get_factory(self, entity_type):
        """Map types to entities

        Args:
            entity_type (int): type of entity defined by type field
        Returns:
            DNAEntity or DNAEntity subclass corresponding to type as defined in DNA.TYPES_FACTORIES
        """

        return DNA.TYPES_FACTORIES[entity_type] if entity_type in DNA.TYPES_FACTORIES else DNAEntity

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
        """Save a copy of this file

        Args:
            file_path (str): path to file
        """

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

#
# Project
#


class ProjectError(DNAError):
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
        settings = self._create(entity_type=DNA.TYPE_SETTINGS)
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
        project = self._create(entity_type=DNA.TYPE_PROJECT)
        project.name = "Grail Project"
        project.set('author', 'Alex Litvin')
        project.set('description', 'Simple Grail project for testing purposes')
        project.update()

        # cuelist
        for cuelist_index in range(5):
            cuelist = self.append("%d'st Cuelist" % (cuelist_index,))
            cuelist.set('color', '#FF0000')
            cuelist.set('description', 'Simple cuelist')
            cuelist.update()

            for cue_index in range(5):
                cue = self._create(parent=cuelist.id, entity_type=DNA.TYPE_CUE)
                cue.name = "Cue %d in list %d" % (cue_index, cuelist_index)
                cue.set('color', '#00FF00')
                cue.set('continue', 0)
                cue.set('wait_pre', 100)
                cue.set('wait_post', 30)
                cue.update()

#
# Library
#


class LibraryError(DNAError):
    """Library error of any kind"""

    pass


class Library(DNA):
    """Manage library file"""

    # file extension
    _file_extension = ".grail-library"

    def __init__(self, file_path, create=False):
        """Open or create a project

        Args:
            file_path (str): path to file
        """
        super(Library, self).__init__(file_path, create=create)

        if not self.root() and create:
            self._create("Grail Library",
                         parent=0,
                         entity_type=DNA.TYPE_LIBRARY)

        if not self.root():
            raise LibraryError("Library entity not found in file %s" % (file_path,))

    def create(self, name, entity_type=DNA.TYPE_ABSTRACT, factory=None):
        """Create new library entity

        Returns: new item
        """

        item = self._create(name,
                            parent=self.root().id,
                            entity_type=entity_type,
                            factory=factory)

        return item

    def root(self):
        """Get a library entity

        Returns: root item of library
        """

        root = self._entities(filter_type=DNA.TYPE_LIBRARY, filter_parent=0)

        return root[0] if len(root) > 0 else None

    def remove(self, entity_id):
        """Remove entity from library

        Args:
            entity_id (int): id of entity
        """

        self._remove(entity_id)

    def remove_all(self):
        """Remove all entities from library"""

        for entity in self.items():
            self._remove(entity.id)

    def items(self, filter_type=False, filter_keyword=False, sort='name', reverse=False, offset=0, limit=0):
        """Returns list of library items

        Args:
            filter_type: limit result set by type, pass False to disable filter
            filter_keyword (str): limit result set by keyword, pass False to disable filter
            sort (str): sort field
            reverse (bool): reverse results order
            offset (int): start index
            limit (int): limit items result set
        """

        return self._entities(
            filter_type=filter_type,
            filter_parent=self.root().id,
            filter_keyword=filter_keyword,
            sort=sort,
            reverse=reverse,
            offset=offset,
            limit=limit)

    def item(self, entity_id):
        """Return library item by id

        Args:
            entity_id (int): entity identifier
        """

        return self._entity(entity_id)

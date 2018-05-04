# -*- coding: UTF-8 -*-
"""
    grailkit.dna
    ~~~~~~~~~~~~

    Implementation of grail file format.
    This file format used for all internal grail data structures.

    :copyright: (c) 2018 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import os
import json
import sqlite3 as lite

from grailkit.core import Signal
from grailkit.db import DataBaseHost, DataBaseError
from grailkit.util import millis_now, default_key

# todo: Add ability to change nodes without executing SQL queries, as each change generates events in current model


class DNAError(DataBaseError):
    """Base class for DNA errors"""

    pass


class DNAEntity:
    """DNA entity definition class

    Each entity must have following fields:
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
        """DNA entity representation.
        This class provides methods and properties for easier management of entities an their properties

        Args:
            parent (DNA): parent DNA object
        """

        if not isinstance(parent, DNA):
            raise DNAError("DNAEntity can't be created without parent DNA. Given %s" % str(parent))

        self._id = 0
        self._type = DNA.TYPE_ABSTRACT
        self._name = ""
        self._parent = 0
        self._search = ""
        self._content = None
        self._created = millis_now()
        self._modified = 0
        self._index = 0
        self._dna = parent

    def __len__(self):
        """Returns number of properties"""

        return len(self.properties())

    def __bool__(self):
        """Boolean representation"""

        return True

    @property
    def id(self):
        """Returns entity identifier number"""

        return self._id

    @property
    def dna(self):
        """Returns parent DNA object, where this entity belongs"""

        return self._dna

    @property
    def parent(self):
        """Returns parent entity"""

        return self._dna._entity(self._parent)

    @property
    def parent_id(self):
        """Returns parent entity identifier"""

        return self._parent

    @parent_id.setter
    def parent_id(self, value):
        """Set parent identifier

        Args:
            value (int): identifier
        Raises:
            ValueError: if parent is not int
        """

        if not isinstance(value, int):
            raise ValueError('Parent id must be int')

        self._parent = value
        self._changed()

        self._dna._update_field(self, 'parent')

    @property
    def name(self):
        """Name of entity"""

        return self._name

    @name.setter
    def name(self, name):
        """Name of entity"""

        self._name = name
        self._changed()

        self._dna._update_field(self, 'name')

    @property
    def type(self):
        """Entity type"""

        return self._type

    @type.setter
    def type(self, value):
        """Set type of entity

        Args:
            value: type of entity
        Raises:
            ValueError: if given value is not int
        """

        if not isinstance(value, int):
            raise ValueError('Type must be int')

        self._type = value
        self._changed()

        self._dna._update_field(self, 'type')

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
        """Set content of item

        Args:
            content (object): contents object
        """

        self._content = content
        self._changed()

        self._dna._update_field(self, 'content')

    @property
    def search(self):
        """Search string"""

        return self._search

    @search.setter
    def search(self, value):
        """Set value of search field

        Args:
            value (str): search string
        Raises:
            ValueError: if given value is not string
        """

        if not isinstance(value, str):
            raise ValueError('Search value must be string')

        self._search = str(value)
        self._changed()

        self._dna._update_field(self, 'search')

    @property
    def index(self):
        """Index inside parent entity"""

        return self._index

    @index.setter
    def index(self, value):
        """Set index of entity

        Args:
            value (int): index value
        """

        if not isinstance(value, int):
            raise ValueError('Index value must be int')

        self._index = value
        self._changed()

        self._dna._update_field(self, 'sort_order')

    def get(self, key, default=None):
        """Get a property value

        Args:
            key (str): property name
            default (object): return `default` if property doesn't exists
        """

        return self._dna._get(self.id, key, default)

    def set(self, key, value, force_type=None):
        """Set a property

        Args:
            key (str): property name
            value (object): value of property
            force_type: convert value to this type
        """

        self._dna._set(self.id, key, value, force_type)

    def has(self, key):
        """Check if property exists

        Args:
            key (str): property name
        """

        return self._dna._has(self.id, key)

    def rename(self, old_key, new_key):
        """Rename property

        Args:
            old_key (str): old property name
            new_key (str): new property name
        """

        return self._dna._rename(self.id, old_key, new_key)

    def unset(self, key):
        """Remove property

        Args:
            key (str): property name
        """

        self._dna._unset(self.id, key)

    def properties(self):
        """Returns list of all properties"""

        return self._dna._properties(self.id)

    def update(self):
        """Force entity update and commit changes to database"""

        self._dna._update(self)

    def delete(self):
        """Delete this entity from DNA"""

        self._dna._remove(self._id)

    def create(self, name, entity_type=None, index=-1, properties=None, factory=None):
        """Create new child entity

        Args:
            name (str): name of entity
            entity_type (int): entity type
            index (int): index where entity will be inserted
            properties (dict): properties list
            factory: factory
        """

        return self._dna._create(name=name,
                                 parent=self._id,
                                 entity_type=entity_type,
                                 index=index,
                                 properties=properties,
                                 factory=factory)

    def remove(self, entity):
        """Remove first entity if given `entity` is children

        Args:
            entity (DNAEntity): entity to be deleted
        """

        self._dna._remove(entity.id, parent=self.id)

    def insert(self, index, entity, factory=None):
        """Create new entity and insert as child item

        Args:
            index (int): index where to insert
            entity (DNAEntity): entity object
            factory: object factory
        """

        return self._dna._copy(entity,
                               parent=self._id,
                               index=index,
                               factory=factory)

    def append(self, entity, factory=None):
        """Create and append new entity

        Args:
            entity (DNAEntity): entity to append
            factory: object factory
        """

        return self._dna._copy(entity, parent=self._id, factory=factory)

    def clear(self):
        """Remove all child entities"""

        self._dna._remove_childs(self._id)

    def childs(self):
        """Returns list of all child entities"""

        return self._dna._childs(self._id)

    def has_childs(self):
        """Returns True if this entity has childs"""

        return self._dna._has_childs(self._id)

    def reverse(self):
        """Sort child entities in reverse order"""

        self._dna._sort(self._id, key='sort_order', reverse=True)

    def sort(self, key=None, reverse=False):
        """Reorder child entities

        Args:
            key (str): database key to sort by
            reverse (bool): reverse sorting
        """

        self._dna._sort(self._id, key=key, reverse=reverse)

    def _changed(self):
        """Called when property is modified"""

        self._modified = millis_now()
        self._dna._update_field(self, 'modified')

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
        self._content = None
        self._search = str(row[7])
        self._index = int(row[8] or 0)

        if row[6]:
            try:
                self._content = json.loads(str(row[6]))
            except ValueError:
                pass

    @classmethod
    def from_sqlite(cls, parent, row):
        """Parse entity from sqlite"""

        entity = cls(parent=parent)
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
        """Year of song release"""

        return self._year

    @year.setter
    def year(self, value):
        """Set year

        Args:
            value (int): year
        """

        self._year = int(value)
        self._modified = millis_now()

    @property
    def artist(self):
        """Artist name"""

        return self._artist

    @artist.setter
    def artist(self, value):
        """Set artist

        Args:
            value (str): artist name
        """

        self._artist = value
        self._modified = millis_now()

    @property
    def album(self):
        """Album name"""

        return self._album

    @album.setter
    def album(self, value):
        """Set album name

        Args:
            value (str): album name
        """

        self._album = value
        self._modified = millis_now()

    @property
    def track(self):
        """Track number"""

        return self._track

    @track.setter
    def track(self, value):
        """Set track number

        Args:
            value (int): track number
        """

        self._track = int(value)
        self._modified = millis_now()

    @property
    def genre(self):
        """Genre name"""

        return self._genre

    @genre.setter
    def genre(self, value):
        """Set genre

        Args:
            value (str): genre name
        """

        self._genre = value
        self._modified = millis_now()

    @property
    def language(self):
        """Language code of lyrics"""

        return self._language

    @language.setter
    def language(self, value):
        """Set language

        Args:
            value (str): language code
        """

        self._language = value
        self._modified = millis_now()

    @property
    def lyrics(self):
        """Lyrics text"""

        return self._lyrics

    @lyrics.setter
    def lyrics(self, value):
        """Set lyrics text

        Args:
            value (str): new lyrics
        """

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

        content = self._content

        self._year = int(default_key(content, 'year', default=2000))
        self._track = int(default_key(content, 'track', default=1))
        self._album = default_key(content, 'album', 'Unknown')
        self._artwork = None
        self._language = default_key(content, 'language', '')
        self._lyrics = default_key(content, 'lyrics', '')
        self._genre = default_key(content, 'genre', 'Unknown')
        self._artist = default_key(content, 'artist', 'Unknown')


class FileEntity(DNAEntity):
    """Representation of file inside DNA file"""

    SEEK_SET = 0
    SEEK_CUR = 1
    SEEK_END = 2

    def __init__(self, parent):
        super(FileEntity, self).__init__(parent)

        self._offset = 0

    @property
    def content(self):
        """Get file contents"""

        return self._content.encode('utf-8')

    @content.setter
    def content(self, value):
        """Set file contents

        Args:
            value (bytes): new file contents
        """

        if type(value) != bytes:
            raise DNAError('File contents must be bytes object')

        self._content = value.decode('utf-8')

    def read(self, size=0):
        """Read contents of file, if buffer_size is 0 or None returns whole file

        Args:
            size (int): number of bytes to read
        """

        if size == 0 or size is None:
            return self.content

        self._offset += size
        return self.content[self._offset - size:self._offset]

    def write(self, data):
        """Write data at cursor position"""

        content = self.content

        self._content = (content[0:self._offset] + data + content[self._offset + len(data):]).decode('utf-8')
        self._offset += len(data)

    def truncate(self, size=0):
        """Truncates the file's size. If the optional size argument is present,
        the file is truncated to that size.

        Args:
            size (int): size of resulting file
        """

        self._content = self.content[0:size].decode('utf-8')

    def seek(self, offset, whence=SEEK_SET):
        """Sets the file's current position

        Args:
            offset (int): new position
            whence (int): how to calculate offset - from begging, current position or end of contents
        """

        if whence == self.SEEK_SET:
            self._offset = offset
        elif whence == self.SEEK_CUR:
            self._offset += offset
        elif whence == self.SEEK_END:
            self._offset = len(self.content) - offset

    def tell(self):
        """Returns current stream position"""

        return self._offset

    def _parse(self, row):
        """"""

        super(FileEntity, self)._parse(row)

        self._content = (self._content or '')


class CuelistEntity(DNAEntity):
    """Representation of cuelist"""

    def __init__(self, parent):
        """Create a cuelist"""
        super(CuelistEntity, self).__init__(parent)

    def __len__(self):
        """Return number of cues"""

        return len(self.cues())

    def cues(self):
        """Returns list of all cues in Cuelist"""

        return self._dna._entities(filter_parent=self._id)

    def cue(self, cue_id):
        """Get cue by id

        Args:
            cue_id (int): cue identifier
        """

        return self._dna._entity(cue_id)

    def create(self, name, entity_type=None, index=-1, properties=None, factory=None):
        """Create entity with DNA.TYPE_CUE by default

        Args:
            name (str): name of entity
            entity_type (int): entity type
            index (int): index where entity will be inserted
            properties (dict): properties list
            factory: factory
        """

        if entity_type is None:
            entity_type = DNA.TYPE_CUE

        super(CuelistEntity, self).create(name, entity_type, index=-1, properties=properties, factory=factory)


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

    COLORS = (COLOR_DEFAULT,
              COLOR_RED,
              COLOR_ORANGE,
              COLOR_YELLOW,
              COLOR_GREEN,
              COLOR_BLUE,
              COLOR_PURPLE,
              COLOR_GRAY)

    COLOR_NAMES = (
        'Default',
        'Red',
        'Orange',
        'Yellow',
        'Green',
        'Blue',
        'Purple',
        'Gray'
        )

    def __init__(self, parent):
        """Create a cue instance

        Args:
            parent (DNA): parent DNA
        """
        super(CueEntity, self).__init__(parent)

    @property
    def number(self):
        """Identifier of cue assigned by user"""

        return self.get("number", default=self.index)

    @number.setter
    def number(self, value):
        """Set number

        Args:
            value (str): cue number
        Raises:
            ValueError: if given value is not string
        """

        if not isinstance(value, str):
            raise ValueError('Cue number must be string, \'%s\' given' % str(value))

        self.set("number", value)

    @property
    def color(self):
        """any text that describe cue"""

        return self.get("color", default=self.COLOR_DEFAULT)

    @color.setter
    def color(self, value):
        """Set color of cue

        Args:
            value (str): cue color
        """

        if not isinstance(value, str):
            raise ValueError('Cue color must be string in #000000 format, \'%s\' given' % str(value))

        self.set('color', value)

    @property
    def pre_wait(self):
        """Wait before execution of cue"""

        return self.get("pre-wait", default=0)

    @pre_wait.setter
    def pre_wait(self, value):
        """Set pre wait

        Args:
            value (float, int): pre wait in seconds
        Raises:
            ValueError if given value is not float or int
        """

        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError('Given value must be of int or float type')

        self.set('pre-wait', value, force_type=DNA.ARG_FLOAT)

    @property
    def post_wait(self):
        """Wait after execution of cue"""

        return self.get("post-wait", default=0)

    @post_wait.setter
    def post_wait(self, value):
        """Set post wait time

        Args:
            value (float, int): post wait in seconds
        Raises:
            ValueError if given value is not float or int
        """

        if not (isinstance(value, int) or isinstance(value, float)):
            raise ValueError('Given value must be of int or float type')

        self.set('post-wait', value, force_type=DNA.ARG_FLOAT)

    @property
    def follow(self):
        """Execute next cue after this finishes, move cursor to next or do nothing."""

        return self.get("follow", default=self.FOLLOW_OFF)

    @follow.setter
    def follow(self, value):
        """Set follow mode

        Args:
            value (int): follow mode
        Raises:
            ValueError if value is not one of (FOLLOW_OFF, FOLLOW_ON, FOLLOW_CONTINUE)
        """

        if value not in self.FOLLOW_TYPE:
            raise ValueError('Follow type is not supported')

        self.set("follow", value)

    def create(self, name, entity_type=None, index=-1, properties=None, factory=None):
        """Create entity with DNA.TYPE_CUE by default

        Args:
            name (str): name of entity
            entity_type (int): entity type
            index (int): index where entity will be inserted
            properties (dict): properties list
            factory: factory
        """

        if entity_type is None:
            entity_type = DNA.TYPE_CUE

        super(CueEntity, self).create(name, entity_type, index=-1, properties=properties, factory=factory)


class DNA:
    """Base class for parsing grail files,
    use this class when you don't want to expose internal methods.
    Otherwise use DNAFile class.
    Please don't use this class directly.
    """

    # property types
    ARG_NONE = 0
    ARG_BOOL = 1
    ARG_INT = 2
    ARG_FLOAT = 3
    ARG_STRING = 4
    ARG_JSON = 6

    # list all supported types
    _SUPPORTED_ARGS = (ARG_NONE, ARG_BOOL, ARG_INT, ARG_FLOAT, ARG_STRING, ARG_JSON)

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
    TYPE_LAYOUT = 31
    TYPE_VIEW = 32

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
        TYPE_SONG,
        TYPE_LAYOUT,
        TYPE_VIEW
        )

    # types and their default factories
    TYPES_FACTORIES = {
        TYPE_ABSTRACT: DNAEntity,
        TYPE_SETTINGS: SettingsEntity,
        TYPE_CUELIST: CuelistEntity,
        TYPE_CUE: CueEntity,
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
        """Open a *.grail file for read and write

        Args:
            file_path (str): path to file
            create (bool): create file if not exists

        Raises:
            DNAError: if file can't be parsed or not exists
        """

        # signals
        self.property_changed = Signal(int, str, str)
        self.entity_changed = Signal(int)
        self.entity_removed = Signal(int)
        self.entity_added = Signal(int)

        self._changed = False
        self._location = file_path

        if not self.validate(file_path) and not create:
            raise DNAError("Grail file '%s' could not be opened." % file_path)
        else:
            self._db = DataBaseHost.get(file_path, query=self._db_create_query, create=create)

    @property
    def location(self):
        """Returns path to file"""

        return self._location

    @property
    def filename(self):
        """Returns file name"""

        return os.path.splitext(os.path.basename(self._location))[0]

    @property
    def changed(self):
        """Return True if changes not saved"""

        return self._changed

    def save(self):
        """Save all changes"""

        self._db.commit()
        self._changed = False

    def save_copy(self, file_path, create=True):
        """Save a copy of this file to `file_path` location

        Args:
            file_path (str): path to copy of current file
            create (bool): If True file will be created
        """

        self.save()
        self._db.copy(file_path, create=create)

    def close(self):
        """Close connection"""

        self._db.close()
        self._changed = False

    def _create(self, name="", parent=0, entity_type=None, index=-1, properties=None, factory=None):
        """Returns new DNAEntity inside this DNA file

        Args:
            name (str): entity name
            parent (int): parent id
            entity_type (int, None): entity type
            index (int): index of insertion
            properties (dict, None): dict with entity properties
            factory: object creation factory
        Returns:
            DNAEntity by default or if `factory` given returns object created by factory
        """

        self._changed = True

        if entity_type not in DNA.TYPES:
            entity_type = DNA.TYPE_ABSTRACT

        cursor = self._db.cursor
        sql_values = [parent,
                      entity_type,
                      name,
                      millis_now(),
                      millis_now(),
                      json.dumps(None, separators=(',', ':')),
                      '',
                      index]

        if index >= 0:
            # realign sort_order field
            cursor.execute("""UPDATE entities
                              SET sort_order = sort_order + 1
                              WHERE sort_order >= ? AND parent = ?""", (index, parent))
            # insert
            cursor.execute("""INSERT INTO entities
                          (id, parent, type, name, created, modified, content, search, sort_order)
                          VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)""", sql_values)
        else:
            sql_values[7] = parent
            # append item with max(sort_order) + 1 index or 0 if it first child entity
            cursor.execute("""INSERT INTO entities
                          (id, parent, type, name, created, modified, content, search, sort_order)
                          VALUES (NULL, ?, ?, ?, ?, ?, ?, ?,
                          (SELECT IFNULL(MAX(sort_order) + 1, 0) FROM entities WHERE parent = ?))
                           """, sql_values)

        self._db.connection.commit()

        entity_id = cursor.lastrowid

        if properties and len(properties) > 0:
            for key, value in properties.items():
                force_type = self._get_type(value)
                self._db.execute("INSERT OR IGNORE INTO properties(entity, key, value, type) VALUES(?, ?, ?, ?)",
                                 (entity_id, key, self._write_type(value, force_type), force_type))

        entity = self._entity(entity_id, factory)

        # emit entity changed
        self.entity_changed.emit(entity.id)
        self.entity_added.emit(entity.id)

        return entity

    def _copy(self, entity, name=None, parent=None, entity_type=None, index=-1, factory=None):
        """Create copy of given entity and override properties if needed

        Args:
            entity (DNAEntity): entity to be copied
            name (str): override name of entity
            parent (int): override entity parent
            entity_type (int): override entity type
            index (int): override entity index
            factory: create entity using this factory
        """

        name = name if name else entity.name
        parent = parent if parent else entity.parent_id
        entity_type = entity_type if entity_type else entity.type

        cursor = self._db.cursor
        sql_values = [parent,
                      entity_type,
                      name,
                      millis_now(),
                      millis_now(),
                      json.dumps(entity.content, separators=(',', ':')),
                      entity.search,
                      index]

        if index >= 0:
            # realign sort_order field
            cursor.execute("""UPDATE entities
                              SET sort_order = sort_order + 1
                              WHERE sort_order >= ? AND parent = ?""", (index, parent))
            # insert
            cursor.execute("""INSERT INTO entities
                          (id, parent, type, name, created, modified, content, search, sort_order)
                          VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)""", sql_values)
        else:
            sql_values[7] = parent
            # append item with max(sort_order) + 1 index or 0 if it first child entity
            cursor.execute("""INSERT INTO entities
                          (id, parent, type, name, created, modified, content, search, sort_order)
                          VALUES (NULL, ?, ?, ?, ?, ?, ?, ?,
                          (SELECT IFNULL(MAX(sort_order) + 1, 0) FROM entities WHERE parent = ?))
                           """, sql_values)

        self._db.connection.commit()

        copy_id = cursor.lastrowid

        for key, value in entity.properties().items():
            force_type = self._get_type(value)
            self._db.execute("INSERT OR IGNORE INTO properties(entity, key, value, type) VALUES(?, ?, ?, ?)",
                             (copy_id, key, self._write_type(value, force_type), force_type))

        entity = self._entity(copy_id, factory=factory)
        self.entity_added.emit(entity.id)

        return entity

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
        entities = self._factory(factory, raw_entities)

        return entities[0] if len(entities) > 0 else None

    def _entities(self, filter_type=None, filter_parent=None, filter_keyword=None,
                  sort=None, reverse=False, offset=0, limit=0, factory=None):
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
            list of all entities available regarding filter arguments
        """

        where = []
        args = []

        if filter_parent:
            where.append(" parent = ?")
            args.append(filter_parent)

        if filter_type:
            where.append(" type = ?")
            args.append(filter_type)

        if filter_keyword:
            keyword = "%" + str(filter_keyword).lstrip().rstrip().lower() + "%"
            where.append(""" lowercase(name) LIKE lowercase(?)
                    OR lowercase(search) LIKE lowercase(?)""")
            args.append(keyword)
            args.append(keyword)

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

        return self._factory(factory, raw_entities)

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
                        json.dumps(entity._content, separators=(',', ':')), entity.search, entity.index, entity.id))

        self.entity_changed.emit(entity.id)

    def _update_field(self, entity, field):
        """Update entity field

        Args:
            entity (DNAEntity): entity to be changed
            field (str): database field to be updated
        """

        self._changed = True

        if field not in ('parent', 'type', 'name', 'created', 'modified', 'content', 'search', 'sort_order'):
            raise ValueError('Given field "%s" not supported' % str(field))

        if field in ('type', 'name', 'created', 'modified', 'search'):
            value = getattr(entity, field)
        elif field == 'parent':
            value = entity.parent_id
        elif field == 'content':
            value = json.dumps(entity.content, separators=(',', ':'))
        elif field == 'sort_order':
            value = entity.index
        else:
            value = ''

        cursor = self._db.cursor
        cursor.execute("""UPDATE entities SET %s = ? WHERE id = ?""" % field, (value, entity.id))

        self.entity_changed.emit(entity.id)

    def _remove(self, entity_id, parent=None):
        """Remove entity by id

        Args:
            entity_id (int): id of an entity
            parent (int): parent entity id
        """

        if parent:
            entity = self._db.get("SELECT parent FROM entities WHERE id = ? AND parent = ?", (entity_id, parent))
            parent_id = entity[0] if entity else None

            # return False since there is no entity to remove
            if not entity:
                return False
        else:
            parent_id = self._db.get("SELECT parent FROM entities WHERE id = ?", (entity_id,))
            parent_id = parent_id[0] if parent_id else None

        self._changed = True

        self._db.execute("DELETE FROM entities WHERE id = ?", (entity_id,))
        self._db.execute("DELETE FROM properties WHERE entity = ?", (entity_id,))
        self._db.connection.commit()

        # emit entity changed signal
        # emit parent id, as we can't use removed entity
        self.entity_removed.emit(parent_id)

        self._remove_childs(entity_id)

        return True

    def _remove_childs(self, entity_id):
        """Remove child entities

        Args:
            entity_id (int): id of DNAEntity
        """

        for child in self._childs(entity_id):
            self._remove(child.id)

    def _sort(self, entity_id, key=None, reverse=False):
        """Sort child entities

        Args:
            entity_id (int): entity id
            key: sort field
            reverse (bool): reverse order or not
        """

        entities = self._entities(filter_parent=entity_id, sort=key, reverse=reverse)

        for index, entity in enumerate(entities):
            self._db.execute("""UPDATE entities SET sort_order = ? WHERE id = ?""", (index, entity.id))

        self._db.commit()

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

        return self._factory(factory, raw_entities)

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

        return self._read_type(value[0], value[1]) if value else default

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
            force_type = self._get_type(value)
        elif force_type not in self._SUPPORTED_ARGS:
            raise DNAError("Property type not supported")

        value = self._write_type(value, force_type)

        self._db.execute("INSERT OR IGNORE INTO properties(entity, key, value, type) VALUES(?, ?, ?, ?)",
                         (entity_id, key, value, force_type))
        self._db.execute("UPDATE properties SET entity = ?, key = ?, value = ?, type = ? WHERE entity = ? AND key = ?",
                         (entity_id, key, value, force_type, entity_id, key))

        self.property_changed.emit(entity_id, key, value)

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

    def _contains(self, entity_id, child_id):
        """Check if entity contains a child

        Args:
            entity_id (int): entity id
            child_id (int): child entity id
        """

        value = False
        raw_childs = self._db.all("SELECT id FROM entities WHERE parent = ?", (entity_id,))

        for child in raw_childs:
            if child[0] == child_id:
                return True

            value = self._contains(child[0], child_id)

        return value

    def _properties(self, entity_id):
        """Get list of all properties linked to entity

        Args:
            entity_id (int): id of an entity

        Returns:
            properties list of an entity
        """

        props = self._db.all("SELECT key, value, type FROM `properties` WHERE `entity` = ?", (entity_id,))

        return {prop[0]: self._read_type(prop[1], prop[2]) for prop in props}

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

        # emit property changed signal
        self.property_changed.emit(entity_id, new_key, self._get(entity_id, new_key))

    def _factory(self, factory, raw_entities):
        """Return list of entities created by factory from raw_entities

        Args:
            factory: object from which entities will be created
            raw_entities: sqlite3 rows
        """

        entities = []

        for raw in raw_entities:
            factory_entity = factory if factory else self._get_factory(raw['type'])
            entities.append(factory_entity.from_sqlite(self, raw))

        return entities

    @classmethod
    def validate(cls, file_path):
        """Validate file to be proper grail file

        Args:
            file_path (str): path to file
        """

        # check file existence
        if not os.path.isfile(file_path):
            return False

        # check file extension
        if os.path.splitext(file_path)[1] != cls._file_extension:
            return False

        # try to open sqlite database
        try:
            db = DataBaseHost.get(file_path)
            db.all("SELECT name FROM sqlite_master WHERE type='table'")
        except lite.DatabaseError:
            return False

        return True

    @classmethod
    def _get_factory(cls, entity_type):
        """Map types to entities

        Args:
            entity_type (int): type of entity defined by type field
        Returns:
            DNAEntity or DNAEntity subclass corresponding to type as defined in DNA.TYPES_FACTORIES
        """

        return cls.TYPES_FACTORIES[entity_type] if entity_type in cls.TYPES_FACTORIES else DNAEntity

    @classmethod
    def _get_type(cls, value):
        """Get type of value

        Args:
            value: any object
        Returns:
            argument type
        """

        builtin_type = type(value)
        arg_type = cls.ARG_NONE

        if builtin_type == str:
            arg_type = cls.ARG_STRING
        elif builtin_type == int:
            arg_type = cls.ARG_INT
        elif builtin_type == float:
            arg_type = cls.ARG_FLOAT
        elif builtin_type == bool:
            arg_type = cls.ARG_BOOL
        elif builtin_type == dict or builtin_type == list:
            arg_type = cls.ARG_JSON

        return arg_type

    @classmethod
    def _write_type(cls, arg_value, arg_type):
        """Create a string representation of value given

        Args:
            arg_value: any object
            arg_type: type of object to convert to

        Returns:
            string representation of value that will be written to database
        """

        if arg_type == cls.ARG_JSON:
            value = json.dumps(arg_value)
        elif arg_value is True:
            value = 'True'
        elif arg_value is False:
            value = 'False'
        elif arg_type in cls._SUPPORTED_ARGS and arg_type != cls.ARG_JSON:
            value = str(arg_value)
        else:
            value = 'None'

        return value

    @classmethod
    def _read_type(cls, arg_value, arg_type):
        """Parse string from db into correct object

        Args:
            arg_value: raw value
            arg_type: value type

        Returns:
            object from raw value
        """

        if arg_type == cls.ARG_JSON:
            arg_value = json.loads(arg_value)
        elif arg_type == cls.ARG_INT:
            arg_value = int(arg_value)
        elif arg_type == cls.ARG_FLOAT:
            arg_value = float(arg_value)
        elif arg_type == cls.ARG_BOOL:
            arg_value = arg_value == 'True'
        elif arg_type == cls.ARG_NONE:
            arg_value = None

        return arg_value


class DNAProxy:
    """This class gives public access to hidden methods of DNA"""

    def __init__(self, dna):
        """Args:
            dna (DNA): reference to DNA
        """

        self._dna_ref = dna

    def create(self, *args, **kwargs):
        """Create entity"""
        return self._dna_ref._create(*args, **kwargs)

    def copy(self, *args, **kwargs):
        """Copy existing entity"""
        return self._dna_ref._copy(*args, **kwargs)

    def entity(self, *args, **kwargs):
        """Returns entity by id"""
        return self._dna_ref._entity(*args, **kwargs)

    def entities(self, *args, **kwargs):
        """Returns list of entities"""
        return self._dna_ref._entities(*args, **kwargs)

    def update(self, *args, **kwargs):
        """Update entity"""
        return self._dna_ref._update(*args, **kwargs)

    def remove(self, *args, **kwargs):
        """Remove entity by id"""
        return self._dna_ref._remove(*args, **kwargs)

    def childs(self, *args, **kwargs):
        """Returns list of child entities"""
        return self._dna_ref._childs(*args, **kwargs)

    def has_childs(self, *args, **kwargs):
        """Returns Tru if entity has childs"""
        return self._dna_ref._has_childs(*args, **kwargs)

    def contains(self, *args, **kwargs):
        """Check if entity contains an child with given id"""
        return self._dna_ref._contains(*args, **kwargs)

    def has(self, *args, **kwargs):
        """Check if property exists"""
        return self._dna_ref._has(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Get property value"""
        return self._dna_ref._get(*args, **kwargs)

    def set(self, *args, **kwargs):
        """Set property value"""
        return self._dna_ref._set(*args, **kwargs)

    def rename(self, *args, **kwargs):
        """Rename property name"""
        return self._dna_ref._rename(*args, **kwargs)

    def unset(self, *args, **kwargs):
        """Remove property"""
        return self._dna_ref._unset(*args, **kwargs)

    def unset_all(self, *args, **kwargs):
        """Remove all properties"""
        return self._dna_ref._unset_all(*args, **kwargs)

    def properties(self, *args, **kwargs):
        """Returns dict of properties"""
        return self._dna_ref._properties(*args, **kwargs)


class DNAFile(DNA, DNAProxy):
    """Interface to Grail-file with public methods"""

    def __init__(self, file_path, create=False):
        """Open a grail file

        Args:
            file_path (str): path to grail file
            create (bool): create file if not exists
        """
        DNA.__init__(self, file_path, create=create)
        DNAProxy.__init__(self, self)


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
        Returns:
            True if property exists
        """

        return self._has(0, key)

    def get(self, key, default=None):
        """Get a property value

        Args:
            key (str): property key
            default (object): Object that will be returned if property doesn't exists
        Returns:
            property value or default if isn't exists
        """

        return self._get(0, key, default)

    def set(self, key, value, force_type=None):
        """Set value of property

        Args:
            key (str): property key
            value (object): property value object
            force_type: If set to not None, value with this type will be saved
        Returns:
            True if operation is succeeded
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
        Returns:
            True if operation is succeeded
        """

        self._unset(0, key)
        self._db.commit()

        return True

    def unset_all(self):
        """Remove all properties

        Returns:
            True if operation succeeded
        """

        self._unset_all(0)
        self._db.commit()

        return True

    def rename(self, old_key, new_key):
        """Rename property key

        Args:
            old_key (str): current property key
            new_key (str): new property key

        Returns:
            True if operation is succeeded
        """

        self._rename(0, old_key, new_key)
        self._db.commit()

        return True


class ProjectError(DNAError):
    """Base class for all project related exceptions"""

    pass


class Project(DNA):
    """Representation of a project file"""

    def __init__(self, file_path, create=False):
        """Open or create a project

        Args:
            file_path (str): path to file
            create (bool): create file if not exists
        """

        super(Project, self).__init__(file_path, create=create)

        self._dna_proxy = DNAProxy(self)
        self._project = 0

        root = self._root()

        if not create and not root:
            raise ProjectError('Unable to open project. Root entity not found.')

        # create project if there is no project entity
        if create and not root:
            self._create_project()

        self._id = self._root().id

    def __len__(self):
        """Get number of cuelist in project"""

        return len(self.cuelists())

    @property
    def dna(self):
        """Get a proxy for dna"""

        return self._dna_proxy

    @property
    def name(self):
        """Project name"""

        return self._root().name

    @name.setter
    def name(self, value):
        """Project name setter

        Args:
            value (str): new project name
        """

        self._root().name = value

    @property
    def description(self):
        """Project description"""

        return self._root().get('description', default='Grail project')

    @description.setter
    def description(self, value):
        """Project description setter

        Args:
            value (str): new project description
        """

        self._root().set('description', value)

    @property
    def author(self):
        """Project author"""

        return self._root().get('author', default='Grail')

    @author.setter
    def author(self, value):
        """Project author setter

        Args:
            value (str): new project author
        """

        self._root().set('author', value)

    @property
    def created(self):
        """Date on witch project was created"""

        return self._root().created

    @property
    def modified(self):
        """Date of last edit on project"""

        return self._root().modified

    def settings(self):
        """Get a setting entity"""

        entity = self._entities(filter_type=DNA.TYPE_SETTINGS,
                                filter_parent=self._id,
                                factory=SettingsEntity)

        if len(entity) == 0:
            entity = self._create(name="Settings",
                                  parent=self._id,
                                  entity_type=DNA.TYPE_SETTINGS,
                                  factory=SettingsEntity)
            return entity
        else:
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

    def create(self, name="Untitled cuelist"):
        """Create a cuelist"""

        return self._create(name=name, parent=self._id, entity_type=DNA.TYPE_CUELIST, factory=CuelistEntity)

    def _root(self):
        """Returns root project entity"""

        if self._project:
            return self._project

        root = self._entities(filter_type=DNA.TYPE_PROJECT, filter_parent=0)
        root = root[0] if len(root) > 0 else None
        self._project = root

        return root

    def _create_project(self):
        """Create project entities"""

        self._project = self._create(name='Untitled project',
                                     parent=0,
                                     entity_type=DNA.TYPE_PROJECT,
                                     properties={
                                      'author': 'Grail',
                                      'description': 'Grail project'
                                     })
        self._id = self._project._id
        self._create(name="settings", entity_type=DNA.TYPE_SETTINGS, parent=self._id)


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

        self._root = None
        self._dna_proxy = DNAProxy(self)

        if not self.root() and create:
            self._create("Grail Library", parent=0, entity_type=DNA.TYPE_LIBRARY)

        if self.root() is None:
            raise LibraryError("Library entity not found in file %s" % (file_path,))

    @property
    def dna(self):
        """Get a proxy for dna"""

        return self._dna_proxy

    def create(self, name, entity_type=DNA.TYPE_ABSTRACT, factory=None):
        """Create new library entity

        Returns: new item
        """

        item = self._create(name,
                            parent=self.root().id,
                            entity_type=entity_type,
                            factory=factory)

        return item

    def copy(self, entity):
        """Copy existing entity into library

        Args:
            entity (DNAEntity): entity to be copied
        """

        self._copy(entity)

    def root(self):
        """Get a library entity

        Returns: root item of library
        """

        if self._root:
            return self._root

        root = self._entities(filter_type=DNA.TYPE_LIBRARY, filter_parent=0)
        root = root[0] if len(root) > 0 else None
        self._root = root

        return root

    def remove(self, entity_id):
        """Remove entity from library

        Args:
            entity_id (int): id of entity
        """

        self._remove(entity_id)

    def clear(self):
        """Remove all entities from library"""

        for entity in self.items():
            self._remove(entity.id)

    def items(self, filter_type=None, filter_keyword=None, sort='name', reverse=False, offset=0, limit=0):
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

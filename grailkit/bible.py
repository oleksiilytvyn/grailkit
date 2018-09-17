# -*- coding: UTF-8 -*-
"""
    grailkit.bible
    ~~~~~~~~~~~~~~

    Implements access to bible files.

    Grail bible format consists of standard grail DNA format plus
    two additional tables: `books` and `verses`

    SQL structure:

    .. code:: sql

        CREATE TABLE books(id INTEGER PRIMARY KEY AUTOINCREMENT, osisid TEXT, name TEXT, title TEXT, abbr TEXT );
        CREATE TABLE verses( osisid TEXT, book INT, chapter INT, verse INT, text TEXT );

    :copyright: (c) 2018 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import os
import re
import glob
import json
import sqlite3

from grailkit import PATH_SHARED
from grailkit.util import copy_file, default_key, file_exists
from grailkit.dna import DNA


def verse_factory(cursor, row):
    """Parse sqlite row into Verse object

    Args:
        cursor (sqlite3.Cursor): sqlite3 cursor
        row (sqlite3.Row): row data

    Returns:
        Verse object parsed from sqlite row
    """

    return Verse.from_sqlite(row)


def book_factory(cursor, row):
    """Parse sqlite row into Book object

    Args:
        cursor (sqlite3.Cursor): sqlite3 cursor
        row (sqlite3.Row): row data

    Returns:
        Book object parsed from sqlite row
    """

    return Book.from_sqlite(row)


class BibleError(Exception):
    """Base error thrown when a bible could to be read."""

    pass


class Verse:
    """Representation of Bible verse"""

    def __init__(self):
        """Create verse"""

        self._osisid = ""
        self._book = ""
        self._book_id = 1
        self._chapter = 1
        self._verse = 1
        self._text = ""

    @property
    def type(self):
        """DNA type (int)"""

        return DNA.TYPE_VERSE

    @property
    def book(self):
        """Book name (str)"""

        return self._book

    @property
    def book_id(self):
        """Book id (int)"""

        return self._book_id

    @property
    def chapter(self):
        """Chapter number (int)"""

        return self._chapter

    @property
    def verse(self):
        """Verse number (int)"""

        return self._verse

    @property
    def reference(self):
        """Returns complete reference string

        Examples:
            Genesis 1:1
            1 Corinthians 2:12
        """

        return "%s %d:%d" % (self._book, self._chapter, self._verse)

    @property
    def text(self):
        """Text of verse"""

        return self._text

    def parse(self, row):
        """Parse sqlite row into verse"""

        self._book = row[5]
        self._book_id = row[1]
        self._chapter = row[2]
        self._verse = row[3]
        self._text = row[4]
        self._osisid = row[0]

    @staticmethod
    def from_sqlite(row):
        """Parse sqlite row and return Verse

        Args:
            row: sqlite3 row

        Returns:
            Verse parsed from given sqlite row
        """

        verse = Verse()
        verse.parse(row)

        return verse


class Book:
    """Representation of bible book"""

    def __init__(self):
        """Create book"""

        self._id = 0
        self._abbr = ""
        self._name = ""
        self._title = ""
        self._osisid = ""

    @property
    def type(self):
        """DNA type (int)"""

        return DNA.TYPE_BOOK

    @property
    def id(self):
        """Book abbreviations (str)"""

        return self._id

    @property
    def abbr(self):
        """Book abbreviations (str)"""

        return self._abbr

    @property
    def name(self):
        """Name of book (str)"""

        return self._name

    @property
    def title(self):
        """Full name of book, it might be bigger than name"""

        return self._title

    @property
    def osisid(self):
        """OSIS identifier, can be used for cross-referencing"""

        return self._osisid

    def parse(self, row):
        """Parse sqlite row and fill Book"""

        self._id = row[0]
        self._abbr = row[4]
        self._name = row[2]
        self._title = row[3]
        self._osisid = row[1]

    @staticmethod
    def from_sqlite(row):
        """Parse sqlite row and return Book

        Args:
            row: sqlite row

        Returns:
            Book
        """

        book = Book()
        book.parse(row)

        return book


class BibleInfo:
    """Read only representation of bible file"""

    def __init__(self):
        """Create a object"""

        self._file = ""
        self._date = ""
        self._title = ""
        self._subject = ""
        self._language = ""
        self._publisher = ""
        self._copyright = ""
        self._identifier = ""
        self._description = ""

        self._version = 1

    @property
    def file(self):
        """File location"""

        return self._file

    @property
    def date(self):
        """Date of publication"""

        return self._date

    @property
    def title(self):
        """Bible title"""

        return self._title

    @property
    def subject(self):
        """Subject of a bible"""

        return self._subject

    @property
    def language(self):
        """Language of bible"""

        return self._language

    @property
    def publisher(self):
        """Publisher information"""

        return self._publisher

    @property
    def copyright(self):
        """Copyright information"""

        return self._copyright

    @property
    def identifier(self):
        """Bible identifier, must be unique"""

        return self._identifier

    @property
    def description(self):
        """A little description of Bible"""

        return self._description

    @property
    def version(self):
        """Schema version number"""

        return self._version

    @staticmethod
    def from_json(data):
        """Fill properties from json string

        Args:
            data (dict): parsed json object
        Returns:
            BibleInfo object
        """

        info = BibleInfo()

        info._file = default_key(data, 'file', '')
        info._date = default_key(data, 'date')
        info._title = default_key(data, 'title')
        info._subject = default_key(data, 'subject')
        info._language = default_key(data, 'language')
        info._publisher = default_key(data, 'publisher')
        info._copyright = default_key(data, 'copyright')
        info._identifier = default_key(data, 'identifier')
        info._description = default_key(data, 'description')

        return info


class Bible(DNA):
    """Representation of grail bible file.
    This class gives you read only access to file
    """

    # file extension
    _file_extension = ".grail-bible"

    def __init__(self, file_path):
        """Read grail bible file into Bible class

        Args:
            file_path (str): file location

        Raises:
            DNAError if file does not exists
        """

        super(Bible, self).__init__(file_path, create=False)

        # read bible info
        self._date = self._get(0, "date", default="")
        self._title = self._get(0, "title", default="Untitled")
        self._subject = self._get(0, "subject", default="")
        self._language = self._get(0, "language", default="unknown")
        self._publisher = self._get(0, "publisher", default="Unknown Publisher")
        self._copyright = self._get(0, "copyright", default="copyright information unavailable")
        self._identifier = self._get(0, "identifier", default="NONE")
        self._description = self._get(0, "description", default="")

        self._version = self._get(0, "version", default=1)

    @property
    def date(self):
        """Date of publication"""

        return self._date

    @property
    def title(self):
        """Bible title"""

        return self._title

    @property
    def subject(self):
        """Subject of a bible"""

        return self._subject

    @property
    def language(self):
        """Language of bible"""

        return self._language

    @property
    def publisher(self):
        """Publisher information"""

        return self._publisher

    @property
    def copyright(self):
        """Copyright information"""

        return self._copyright

    @property
    def identifier(self):
        """Bible identifier, must be unique"""

        return self._identifier

    @property
    def description(self):
        """A little description of Bible"""

        return self._description

    @property
    def version(self):
        """Schema version number"""

        return self._version

    def books(self):
        """Returns list of all books"""

        return self._db.all("""SELECT 
            `books`.`id`,
            `books`.`osisid`,
            `books`.`name`,
            `books`.`title`,
            `books`.`abbr`
            FROM books""", factory=book_factory)

    def book(self, book):
        """Returns single book

        Args:
            book (int): book id
        """

        return self._db.get("""SELECT
            `books`.`id`,
            `books`.`osisid`,
            `books`.`name`,
            `books`.`title`,
            `books`.`abbr` FROM books WHERE id = ?""", (book,), factory=book_factory)

    def chapter(self, book, chapter):
        """Returns all verses in chapter

        Args:
            book (int): book id
            chapter (int): chapter id
        """

        return self._db.all("""SELECT 
                `verses`.`osisid`,
                `verses`.`book`,
                `verses`.`chapter`,
                `verses`.`verse`,
                `verses`.`text`,
                `books`.`name` as book_name
            FROM verses
            LEFT JOIN `books` ON `verses`.`book` = `books`.`id`
            WHERE `verses`.`book` = ? AND `verses`.`chapter` = ?
            ORDER BY `verses`.`verse` ASC""", (book, chapter), factory=verse_factory)

    def verse(self, book, chapter, verse):
        """Returns single verse

        Args:
            book (int): book id
            chapter (int): chapter id
            verse (int): verse number
        """

        return self._db.get("""SELECT 
                                `verses`.`osisid`,
                                `verses`.`book`,
                                `verses`.`chapter`,
                                `verses`.`verse`,
                                `verses`.`text`,
                                `books`.`name` as book_name
                            FROM verses
                            LEFT JOIN `books` ON `verses`.`book` = `books`.`id`
                            WHERE `verses`.`book` = ? AND `verses`.`chapter` = ? AND `verses`.`verse` = ?""",
                            (book, chapter, verse), factory=verse_factory)

    def count_verses(self, book, chapter):
        """Returns number of verses in chapter

        Args:
            book (int): book id
            chapter (int): chapter id
        """

        return self._db.get("SELECT COUNT(*) as count FROM verses WHERE book = ? AND chapter = ?",
                            (book, chapter))["count"]

    def count_chapters(self, book):
        """Returns number of chapters in book

        Args:
            book (int): book id
        """

        return self._db.get("SELECT COUNT(*) as count FROM verses WHERE book = ? AND verse = 1",
                            (book,))["count"]

    def match_book(self, keyword):
        """Find books by keyword

        Args:
            keyword (str): search phrase
        """

        keyword = "%" + keyword + "%"

        return self._db.all("""SELECT
                            `books`.`id`,
                            `books`.`osisid`,
                            `books`.`name`,
                            `books`.`title`,
                            `books`.`abbr`
                            FROM books
                            WHERE
                             lowercase(`title`) LIKE lowercase( ? )
                             OR lowercase(`short`) LIKE lowercase( ? )
                             OR lowercase(`full`) LIKE lowercase( ? )
                            """, (keyword, keyword, keyword), factory=book_factory)

    def match_reference(self, keyword, limit=3):
        """find verse by keyword

        Args:
            keyword (str): keywords
            limit (int): limit results
        """

        # default values
        chapter = 1
        verse = 1
        keyword = keyword.lstrip().rstrip().lower()

        # match book
        match = re.search(r'([0-9]+)$', keyword)
        # match book and chapter
        match_chapter = re.search(r'([0-9]+)([\D])([0-9]+)$', keyword)
        # match book, chapter and verse
        match_verse = re.search(r'([0-9]+)([\D])([0-9]+)-([0-9]+)$', keyword)

        if match_verse:
            chapter = match_verse.group(1)
            verse = match_verse.group(3)
            keyword = re.sub(r'([0-9]+)([\D])([0-9]+)-([0-9]+)$', '', keyword)
        elif match_chapter:
            chapter = match_chapter.group(1)
            verse = match_chapter.group(3)
            keyword = re.sub(r'([0-9]+)([\D])([0-9]+)$', '', keyword)
        elif match:
            chapter = match.group(1)
            keyword = re.sub(r'([0-9]+)$', '', keyword)

        keyword = "%" + keyword.lstrip().rstrip() + "%"
        chapter = int(chapter)
        verse = int(verse)

        return self._db.all("""SELECT
                                `verses`.`osisid`,
                                `verses`.`book`,
                                `verses`.`chapter`,
                                `verses`.`verse`,
                                `verses`.`text`,
                                `books`.`name` as book_name
                            FROM verses
                            LEFT JOIN `books` ON `verses`.`book` = `books`.`id`
                            WHERE
                                (lowercase(`books`.`title`) LIKE ?
                                OR lowercase(`books`.`name`) LIKE ?
                                OR lowercase(`books`.`abbr`) LIKE ?)
                                AND `verses`.`chapter` = ?
                                AND `verses`.`verse` = ?
                            LIMIT ?""",
                            (keyword, keyword, keyword, chapter, verse, limit), factory=verse_factory)

    def match_text(self, text, limit=3):
        """Search for text occurrences

        Args:
            text (str): search string
            limit (int): limit results
        """

        keyword = "%" + text.lstrip().rstrip().lower() + "%"

        return self._db.all("""SELECT 
                                `verses`.`osisid`,
                                `verses`.`book`,
                                `verses`.`chapter`,
                                `verses`.`verse`,
                                `verses`.`text`,
                                `books`.`name` as book_name
                               FROM verses 
                               LEFT JOIN `books` ON `verses`.`book` = `books`.`id`
                               WHERE lowercase(`verses`.`text`) LIKE ? LIMIT ?""",
                            (keyword, limit), factory=verse_factory)

    def json_info(self):
        """Create json information string"""

        data = {
            "file": self._location,
            "date": self._date,
            "title": self._title,
            "subject": self._subject,
            "language": self._language,
            "publisher": self._publisher,
            "copyright": self._copyright,
            "identifier": self._identifier,
            "description": self._description
            }

        return json.dumps(data)


class BibleHostError(Exception):
    """BibleHost errors"""

    pass


class BibleHost:
    """Manage all installed bibles."""

    # location of shared folder
    _location = os.path.join(PATH_SHARED, "bibles/")

    # list of available bibles
    _list = {}

    @classmethod
    def setup(cls):
        """Gather information about installed bibles.
        Call this method before use of BibleHost."""

        cls._list = {}

        for f in glob.glob(cls._location + "*.json"):
            file = open(f, "r")
            info = BibleInfo.from_json(json.load(file))
            file.close()

            cls._list[info.identifier] = info

    @classmethod
    def list(cls):
        """List all installed bibles

        Returns:
            list of BibleInfo objects
        """

        return cls._list

    @classmethod
    def info(cls, bible_id):
        """Get a bible info object

        Args:
            bible_id (str): bible identifier
        Returns:
            Bible object if exists otherwise None
        """

        if bible_id in cls._list:
            return cls._list[bible_id]

        return None

    @classmethod
    def get(cls, bible_id):
        """Get a Bible by identifier

        Args:
            bible_id (str): bible identifier string
        Returns:
            Bible object if bible exists under given identifier
        """

        bible = cls.info(bible_id)

        return Bible(bible.file) if bible else None

    @classmethod
    def install(cls, file_path, replace=False):
        """Install bible from file, grail-bible format only

        Args:
            file_path (str): path to bible file
            replace (bool): if bible already installed replace it by another version
        Returns:
            True if installed or False if bible
        Raises:
            BibleHostError raised if bible identifier already exists
        """

        if not cls.verify(file_path):
            raise BibleHostError("Unable to install bible from file \"%s\" due to file corruption." % file_path)

        try:
            bible = Bible(file_path)
            bible.close()
            bible_path = os.path.join(cls._location, bible.identifier + '.grail-bible')
        except (BibleError, sqlite3.OperationalError):
            raise BibleHostError("Unable to install bible from file \"%s\"."
                                 "File may be corrupted or in wrong format." % file_path)

        if cls.info(bible.identifier) and not replace:
            raise BibleHostError("Bible %s (%s) already installed" % (bible.title, bible.identifier,))

        # just copy file to new location
        copy_file(file_path, bible_path)
        installed_bible = Bible(bible_path)

        # create a description file
        cls._create_descriptor(installed_bible)
        cls.setup()

        return True

    @classmethod
    def uninstall(cls, bible_id):
        """Uninstall bible by id

        Args:
            bible_id (str): bible identifier
        """

        if bible_id in cls._list:
            del cls._list[bible_id]

        os.remove(os.path.join(cls._location, bible_id + ".json"))
        os.remove(os.path.join(cls._location, bible_id + ".grail-bible"))

    @classmethod
    def verify(cls, file_path):
        """Check file to be valid grail-bible file

        Args:
            file_path (str): path to bible file
        Returns:
            True if bible file is valid
        """

        if not file_exists(file_path):
            return False

        return True

    @classmethod
    def _create_descriptor(cls, bible):
        """Create a description file for a bible

        Args:
            bible (Bible): bible object
        """

        data = bible.json_info()

        file = open(os.path.join(cls._location, bible.identifier + ".json"), "w")
        file.write(data)
        file.close()

        bible_info = BibleInfo()
        bible_info.from_json(json.loads(data))

        cls._list[bible_info.identifier] = bible_info

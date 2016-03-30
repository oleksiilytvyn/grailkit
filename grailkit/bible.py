# -*- coding: UTF-8 -*-
"""
    grailkit.bible
    ~~~~~~~~~~~~~~

    Implements access to bible files.

    Grail bible format consists of standart grail DNA format plus
    two additional tables: `books` and `verses`

    Sql structure:

    .. code:: sql

        CREATE TABLE books(id INTEGER PRIMARY KEY AUTOINCREMENT, osisid TEXT, name TEXT, title TEXT, abbr TEXT );
        CREATE TABLE verses( osisid TEXT, book INT, chapter INT, verse INT, text TEXT );
"""
import os
import re

from grailkit.dna import DNA


def verse_factory(cursor, row):
    return Verse.from_sqlite(row)


def book_factory(cursor, row):
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
    def book(self):
        """Book name"""
        return self._book

    @property
    def book_id(self):
        """Book id (int)"""
        return self._book

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
        """Returns complete reference text

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
    def id(self):
        """Book abbreviations"""
        return self._id

    @property
    def abbr(self):
        """Book abbreviations"""
        return self._abbr

    @property
    def name(self):
        """Name of book"""
        return self._name

    @property
    def title(self):
        """Full name of book, it might be bigger than name"""
        return self._title

    @property
    def osisid(self):
        """OASIS identifier, can be used for cross-referencing"""
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
    def date(self):
        """Date"""
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
        """Schema version nubmer"""
        return self._version

    def from_json(self, data):
        """Fill properties from json string"""

        self._date = data.date
        self._title = data.title
        self._subject = data.subject
        self._language = data.language
        self._publisher = data.publisher
        self._copyright = data.copyright
        self._identifier = data.identifier
        self._description = data.description


class Bible(DNA):
    """Representation of grail bible file.
    This class gives you read only access to file
    """

    # file extension
    _file_extension = ".grail-bible"

    def __init__(self, file_path):
        """Read grail bible format into Bible class"""

        self._db_create_query += """
            DROP TABLE IF EXISTS books;
            CREATE TABLE books(id INTEGER PRIMARY KEY AUTOINCREMENT, osisid TEXT, name TEXT, title TEXT, abbr TEXT );

            DROP TABLE IF EXISTS verses;
            CREATE TABLE verses( osisid TEXT, book INT, chapter INT, verse INT, text TEXT );
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
        """Date"""
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
        """Returns single book"""

        return self._db.get("""SELECT
            `books`.`id`,
            `books`.`osisid`,
            `books`.`name`,
            `books`.`title`,
            `books`.`abbr` FROM books WHERE id = ?""", (book,), factory=book_factory)

    def chapter(self, book, chapter):
        """Returns all verses in chapter"""

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
        """Returns single verse"""

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
        """Returns number of verses in chapter"""

        return self._db.get("SELECT COUNT(*) as count FROM verses WHERE book = ? AND chapter = ?",
                            (book, chapter))["count"]

    def count_chapters(self, book):
        """Returns number of chapters in book"""

        return self._db.get("SELECT COUNT(*) as count FROM verses WHERE book = ? AND verse = 1",
                            (book,))["count"]

    def match_book(self, keyword):
        """find book by keyword"""

        keyword = "%" + keyword + "%"

        return self._db.all("""SELECT
                            `books`.`id`,
                            `books`.`osisid`,
                            `books`.`name`,
                            `books`.`title`,
                            `books`.`abbr`
                            FROM books
                            WHERE
                             lowercase(title) LIKE lowercase( ? )
                             OR lowercase(short) LIKE lowercase( ? )
                             OR lowercase(full) LIKE lowercase( ? )
                            """, (keyword, keyword, keyword), factory=book_factory)

    def match_reference(self, keyword):
        """find verse by keyword

        Args:
            keyword (str): keywords
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
        match_verse = re.search(r'([0-9]+)([\D])([0-9]+)\-([0-9]+)$', keyword)

        if match_verse:
            chapter = match_verse.group(1)
            verse = match_verse.group(3)
            keyword = re.sub(r'([0-9]+)([\D])([0-9]+)\-([0-9]+)$', '', keyword)
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
                            LIMIT 3""",
                            (keyword, keyword, keyword, chapter, verse), factroy=verse_factory)


class BibleHost:
    """Manage all installed bibles. Not implemented"""

    LOCATION = ".grail/bibles/"

    @staticmethod
    def list():
        """List all installed bibles"""

        items = []

        return items

    @staticmethod
    def get(bible_id):
        """Get a bible object"""

        path = BibleHost.LOCATION + "%s.json" % (bible_id,)

        if os.path.exists(path) and os.path.isfile(path):
            info = BibleInfo()
            info.from_json(path)

            return info
        else:
            return None

    @staticmethod
    def install(file_path):
        """Install bible from file, it can be any format file supported by parsers"""

        # check file
        # create a description file
        # copy file

        pass

    @staticmethod
    def uninstall(bible_id):
        """Uninstall bible by id"""

        # remove description file
        # remove grail-bible file

        pass

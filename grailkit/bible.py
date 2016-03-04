# -*- coding: UTF-8 -*-

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

    _osisid = ""

    _book = ""
    _book_id = 1
    _chapter = 1
    _verse = 1

    _text = ""

    def __init__(self):
        pass

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
        """Returns complete reference text"""
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
            Verse
        """
        verse = Verse()
        verse.parse(row)

        return verse


class Book:
    """Representation of bible book"""

    _id = 0
    _abbr = ""
    _name = ""
    _title = ""
    _osisid = ""

    def __init__(self):
        pass

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
    """Object that represents a bible file but don't have access to file"""

    _date = ""
    _title = ""
    _subject = ""
    _language = ""
    _publisher = ""
    _copyright = ""
    _identifier = ""
    _description = ""

    _version = 1

    # database handler
    _db = None

    def __init__(self, file_path):
        pass

    @property
    def date(self):
        return self._date

    @property
    def title(self):
        return self._title

    @property
    def subject(self):
        return self._subject

    @property
    def language(self):
        return self._language

    @property
    def publisher(self):
        return self._publisher

    @property
    def copyright(self):
        return self._copyright

    @property
    def identifier(self):
        return self._identifier

    @property
    def description(self):
        return self._description

    @property
    def version(self):
        """Schema version nubmer"""
        return self._version


class Bible(DNA):
    """Representation of grail bible file.
    This class gives you read only access to file
    """

    # create file from this query
    # TO-DO: extend query from DNA class
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
        self._date = self._get_property(0, "date", default="")
        self._title = self._get_property(0, "title", default="Untitled")
        self._subject = self._get_property(0, "subject", default="")
        self._language = self._get_property(0, "language", default="unknown")
        self._publisher = self._get_property(0, "publisher", default="Unknown Publisher")
        self._copyright = self._get_property(0, "copyright", default="copyright information unavailable")
        self._identifier = self._get_property(0, "identifier", default="NONE")
        self._description = self._get_property(0, "description", default="")

        self._version = self._get_property(0, "version", default=1)

    @property
    def date(self):
        return self._date

    @property
    def title(self):
        return self._title

    @property
    def subject(self):
        return self._subject

    @property
    def language(self):
        return self._language

    @property
    def publisher(self):
        return self._publisher

    @property
    def copyright(self):
        return self._copyright

    @property
    def identifier(self):
        return self._identifier

    @property
    def description(self):
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
        """find verse by keyword"""

        # default values
        chapter = 1
        verse = 1

        keyword = keyword.lstrip().rstrip().lower()

        # match book
        match = re.search(r'([0-9]+)$', keyword)
        # match book and chapter
        match_chapter = re.search(r'([0-9]+)([\D]{1})([0-9]+)$', keyword)
        # match book, chapter and verse
        match_verse = re.search(r'([0-9]+)([\D]{1})([0-9]+)\-([0-9]+)$', keyword)

        if match_verse:
            chapter = match_verse.group(1)
            verse = match_verse.group(3)
            keyword = re.sub(r'([0-9]+)([\D]{1})([0-9]+)\-([0-9]+)$', '', keyword)
        elif match_chapter:
            chapter = match_chapter.group(1)
            verse = match_chapter.group(3)
            keyword = re.sub(r'([0-9]+)([\D]{1})([0-9]+)$', '', keyword)
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

    @staticmethod
    def list():
        """List all installed bibles"""
        return []

    @staticmethod
    def get(id):
        """Get a bible object"""
        return Bible()

    @staticmethod
    def install(file):
        """Install bible from file, it can be any format file supported by parsers"""
        pass

    @staticmethod
    def uninstall(id):
        """Uninstall bible by id"""
        pass


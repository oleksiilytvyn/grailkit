#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
import sqlite3 as lite

from grailkit.db import DataBaseHost


def verse_factory(cursor, row):
    return Verse(row, cursor)


def book_factory(cursor, row):
    return Book(row, cursor)


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

    def __init__(self, row=None, cursor=None):
        if row is not None:
            self.parse(row)
        else:
            raise BibleError("Could not create Verse, sqlite row is not defined.")

    @property
    def book(self):
        return self._book

    @property
    def book_id(self):
        return self._book

    @property
    def chapter(self):
        return self._chapter

    @property
    def verse(self):
        return self._verse

    @property
    def reference(self):
        """Returns complete reference text"""
        return "%s %d:%d" % (self._book, self._chapter, self._verse)

    @property
    def text(self):
        return self._text

    def parse(self, row):
        self._book = row[5]
        self._book_id = row[1]
        self._chapter = row[2]
        self._verse = row[3]
        self._text = row[4]
        self._osisid = row[0]


class Book:
    """Representation of bible book"""

    _id = 0
    _abbr = ""
    _name = ""
    _title = ""
    _osisid = ""

    def __init__(self, row=None, cursor=None):
        if row:
            self.parse(row, cursor)

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

    def parse(self, row, cursor):
        self._id = row[0]
        self._abbr = row[4]
        self._name = row[2]
        self._title = row[3]
        self._osisid = row[1]


class BibleInfo:
    """Object that represents a bible file but dont have access to file"""

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


class Bible:
    """Representation of grail bible file.
    This class gives you read only access to file
    """

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
        """Read grail bible format into Bible class"""

        if not Bible.validate(file_path):
            raise BibleError("Bible file could not be opened.")
        else:
            self._db = DataBaseHost.get(file_path)

        # read bible info
        self._date = self._get_property("date", "")
        self._title = self._get_property("title", "")
        self._subject = self._get_property("subject", "")
        self._language = self._get_property("language", "")
        self._publisher = self._get_property("publisher", "")
        self._copyright = self._get_property("copyright", "")
        self._identifier = self._get_property("identifier", "")
        self._description = self._get_property("description", "")

        self._version = self._get_property("version", 1)

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

    def books(self):
        """Returns list of all books"""
        self._set_factory(book_factory)

        return self._db.all("""SELECT 
            `books`.`id`,
            `books`.`osisid`,
            `books`.`name`,
            `books`.`title`,
            `books`.`abbr`
            FROM books""")

    def book(self, book):
        """Returns single book"""
        self._set_factory(book_factory)

        return self._db.get("""SELECT
            `books`.`id`,
            `books`.`osisid`,
            `books`.`name`,
            `books`.`title`,
            `books`.`abbr` FROM books WHERE id = ?""", (book,))

    def chapter(self, book, chapter):
        """Returns all verses in chapter"""
        self._set_factory(verse_factory)

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
            ORDER BY `verses`.`verse` ASC""", (book, chapter))

    def verse(self, book, chapter, verse):
        """Returns single verse"""
        self._set_factory(verse_factory)

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
                            (book, chapter, verse))

    def count_verses(self, book, chapter):
        """Returns number of verses in chapter"""
        self._set_factory()

        return self._db.get("SELECT COUNT(*) as count FROM verses WHERE book = ? AND chapter = ?",
                            (book, chapter))["count"]

    def count_chapters(self, book):
        """Returns number of chapters in book"""
        self._set_factory()

        return self._db.get("SELECT COUNT(*) as count FROM verses WHERE book = ? AND verse = 1",
                            (book,))["count"]

    def match_book(self, keyword):
        """find book by keyword"""
        self._set_factory(book_factory)

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
            """, (keyword, keyword, keyword))

    def match_reference(self, keyword):
        """find verse by keyword"""
        self._set_factory(verse_factory)

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
                            (keyword, keyword, keyword, chapter, verse))

    def _set_factory(self, factory=lite.Row):
        """Set sqlite row factory"""
        self._db.connection.row_factory = factory

    def _get_property(self, key, default=""):
        """Get info property"""
        self._set_factory()

        value = self._db.get("SELECT key, value from properties WHERE key = ?", (key,))

        return value["value"] if value else default

    @staticmethod
    def validate(file_path):
        """Check file to be valid grail bible file format

        Args:
            file_path (str): pat to bible file
        """
        # return True
        # if file not exists
        if not os.path.isfile(file_path):
            return False

        # if file doesn't have proper extension
        if os.path.splitext(file_path)[1] != '.grail-bible':
            return False

        # check if file have proper structure
        try:
            connection = lite.connect(file_path)
            connection.row_factory = lite.Row
            c = connection.cursor()
            flag = True

            c.execute("""SELECT name 
                FROM sqlite_master 
                WHERE type='table' AND name in ('books', 'verses', 'properties')
                ORDER BY name ASC""")
            tables = c.fetchall()

            if [table['name'] for table in tables] != ['books', 'properties', 'verses']:
                flag = False

            c.execute("""SELECT 
                    `properties`.`key`,
                    `properties`.`value`,
                    `properties`.`type`
                FROM properties LIMIT 1""")
            record = c.fetchone()

            if record.keys() != ['key', 'value', 'type']:
                flag = False

            c.execute("""SELECT 
                    `books`.`id`,
                    `books`.`osisid`,
                    `books`.`name`,
                    `books`.`title`,
                    `books`.`abbr`
                FROM books LIMIT 1""")
            record = c.fetchone()

            if record.keys() != ['id', 'osisid', 'name', 'title', 'abbr']:
                flag = False

            c.execute("""SELECT 
                    `verses`.`osisid`,
                    `verses`.`book`,
                    `verses`.`chapter`,
                    `verses`.`verse`,
                    `verses`.`text`
                FROM verses LIMIT 1""")
            record = c.fetchone()

            if record.keys() != ['osisid', 'book', 'chapter', 'verse', 'text']:
                flag = False

            c.execute("SELECT key, value from properties WHERE key = ?", ('version',))

            # check version
            if int(c.fetchone()['value']) != 1:
                flag = False

            connection.close()

            return flag
        except:
            return False


class BibleHost:
    """Manage all installed bibles"""

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


class Parser:
    """Parse other file formats into grail bible format. Not implemented"""
    pass


class OSISParser(Parser):
    """Parse OSIS bible. Not implemented"""
    pass


class SwordParser(Parser):
    """Parse Sword bible. Not implemented"""
    pass


class CSVParser(Parser):
    """Parse CSV bible. Not implemented"""
    pass

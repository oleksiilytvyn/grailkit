#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3 as lite
from db import DataBase, DataBaseHost


def verse_factory( cursor, row ):
  return Verse( row, cursor )


def book_factory( cursor, row ):
  return Book( row, cursor )


class BibleError(Exception):
  """Base error thrown when a bible could to be read."""
  pass


class Verse:
  """Representation of Bible verse"""

  _osisid = ""
  
  _book = ""
  _chapter = 1
  _verse = 1

  _text = ""

  def __init__( self, row = None, cursor = None ):
    if row is not None:
      self.parse( row )
    else:
      raise BibleError("Could not create Verse, sqlite row is not defined.")

  @property
  def book( self ):
    return self._book

  @property
  def chapter( self ):
    return self._chapter

  @property
  def verse( self ):
    return self._verse

  @property
  def reference( self ):
    """Returns complete reference text"""
    return "%s %d:%d" % (self._book, self._chapter, self._verse)

  @property
  def text( self ):
    return self._text

  def parse( self, row ):
    self._book = row[0]
    self._chapter = row[1]
    self._verse = row[2]
    self._text = row[3]
    self._osisid = ""


class Book:
  """Representation of bible book"""

  _id = 0
  _abbr = ""
  _name = ""
  _title = ""
  _osisid = ""

  def __init__( self, row = None, cursor = None ):
    if row:
      self.parse( row, cursor )

  @property
  def id( self ):
    """Book abbreviations"""
    return self._id

  @property
  def abbr( self ):
    """Book abbreviations"""
    return self._abbr

  @property
  def name( self ):
    """Name of book"""
    return self._name

  @property
  def title( self ):
    """Full name of book, it might be bigger than name"""
    return self._title

  @property
  def osisid( self ):
    """OASIS identifier, can be used for cross-referencing"""
    return self._osisid

  def parse( self, row, cursor ):
    self._id = row[0]
    self._abbr = row[3]
    self._name = row[1]
    self._title = row[2]
    self._osisid = ""


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

  def __init__( self, file_path ):
    """Read grail bible format into Bible class"""
    
    if not Bible.validate( file_path ):
      raise BibleError("Bible file coud not be opened.")
    else:
      self._db = DataBaseHost.get( file_path )

    # read bible info
    self._date = self._get_property("date", "")
    self._title = self._get_property("title", "")
    self._subject = self._get_property("subject", "")
    self._language = self._get_property("language", "")
    self._publisher = self._get_property("publisher", "")
    self._copyright = self._get_property("copyright", "")
    self._identifier = self._get_property("identifier", "")
    self._description = self._get_property("description", "")

  @property
  def date( self ):
    return self._date

  @property
  def title( self ):
    return self._title

  @property
  def subject( self ):
    return self._subject

  @property
  def language( self ):
    return self._language

  @property
  def publisher( self ):
    return self._publisher

  @property
  def copyright( self ):
    return self._copyright

  @property
  def identifier( self ):
    return self._identifier

  @property
  def description( self ):
    return self._description

  def books( self ):
    """Returns list of all books"""
    self._set_factory( book_factory )

    return self._db.all("SELECT * FROM books")

  def book( self, book ):
    """Returns single book"""
    self._set_factory( book_factory )

    return self._db.get("SELECT * FROM books WHERE id = ?", (book, ))

  def chapter( self, book, chapter ):
    """Returns all verses in chapter"""
    self._set_factory( verse_factory )

    return self._db.all("SELECT * FROM verses WHERE book = ? AND chapter = ? ORDER BY verse ASC", (book, chapter))

  def verse( self, book, chapter, index ):
    """Returns single verse"""
    self._set_factory( verse_factory )

    return self._db.get("SELECT * FROM verses WHERE book = ? AND chapter = ? AND verse = ?", (book, chapter, index))

  def count_verses( self, book, chapter ):
    """Returns number of verses in chapter"""
    self._set_factory()

    return self._db.get("SELECT COUNT(*) as count FROM verses WHERE book = ? AND chapter = ?", (book, chapter))["count"]

  def count_chapters( self, book ):
    """Returns number of chapters in book"""
    self._set_factory()

    return self._db.get("SELECT COUNT(*) as count FROM verses WHERE book = ? AND verse = 1", (book, ))["count"]

  def match_book( self, keyword ):
    """find book by keyword"""
    self._set_factory( book_factory )

    keyword = "%" + keyword + "%"

    return self._db.all("""
            SELECT * FROM books
            WHERE
             lowercase(title) LIKE lowercase( ? )
             OR lowercase(short) LIKE lowercase( ? )
             OR lowercase(full) LIKE lowercase( ? )
            """, (keyword, keyword, keyword ))

  def match_reference( self, keyword ):
    """find verse by keyword"""
    self._set_factory( verse_factory )

    return []

  def _set_factory( self, factory = lite.Row ):
    """Set sqlite row factory"""
    self._db.connection.row_factory = factory

  def _get_property( self, key, default = "" ):
    """Get info property"""
    self._set_factory()

    value = self._db.get("SELECT key, value from info WHERE key = ?", (key, ))

    return value["value"] if value else default

  @staticmethod
  def validate( file_path ):
    """Check file to be valid grail bible file format"""
    return True


class BibleHost:
  """Mange bible versions"""
  pass

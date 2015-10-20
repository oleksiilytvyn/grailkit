#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from db import DataBase, DataBaseHost


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

  def __init__( self, row = None ):
    if row not None:
      self.parse( row )

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
    self._book = row["book"]
    self._chapter = row["chapter"]
    self._verse = row["verse"]
    self._osisid = row["reference"]


class Book:
  """Representation of bible book"""

  _name = ""
  _osisid = ""

  def __init__( self, row = None ):
    pass

  @property
  def name( self ):
    return self._name


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

  _connection = None

  def __init__( self, file_path ):
    """Read grail bible format into Bible class"""
    
    if not Bible.validate( file_path ):
      raise BibleError("Bible file coud not be opened.")

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
    return [Book()]

  def book( self, book ):
    """Returns single book"""
    return Book()

  def chapter( self, book, chapter ):
    """Returns all verses in chapter"""
    return [Verse()]

  def verse( self, book, chapter, index ):
    """Returns single verse"""
    return Verse()

  def count_verses( self, book, chapter ):
    """Returns number of verses in chapter"""
    return 0

  def count_chapters( self, book ):
    """Returns number of chapters in book"""
    return 0

  def match_book( self, keyword ):
    """find book by keyword"""
    return [Book()]

  def match_reference( self, keyword ):
    """find verse by keyword"""
    return [Verse()]

  @staticmethod
  def validate( file_path ):
    """Check file to be valid grail bible file format"""
    return True

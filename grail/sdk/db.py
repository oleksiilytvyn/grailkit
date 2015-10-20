#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3 as lite
import os

class DataBase:
  """SQLite database wrapper"""

  _connection = None

  def __init__( self, file_path, file_copy = False, query = False, query_data = tuple(), create = True ):
    """Create SQLite database wraper

    Args:
      - file_path: database file path
      - query: execute query if file_path not exists
      - file_copy: copy file if file_path not exists
    """
    directory = os.path.dirname(os.path.realpath( file_path ))
    execute_query = False

    if not os.path.exists( directory ):
      os.makedirs( directory )

    if not os.path.isfile( file_path ):
      if file_copy:
        copy_file( file_copy, file_path )
      else:
        open( file_path, 'w+' )
        execute_query = True

    self._connection = lite.connect( file_path )
    self._connection.row_factory = lite.Row

    def lowercase( char ):
      return char.lower()

    def searchprep( char ):
      char = re.sub(r'[\[\_\]\.\-\,\!\(\)\"\'\:\;]', '', char)

      return char.lower()

    self._connection.create_function("lowercase", 1, lowercase)
    self._connection.create_function("searchprep", 1, searchprep)

    if execute_query and query:
      self.cursor.execute(query, query_data)

  @property
  def connection():
    """Returns sqlite3 connection"""
    return self._connection

  @property
  def cursor():
    """Returns sqlite3 connection cursor"""
    return self._connection.cursor()

  def get( self, query, data ):
    """Execute query and return first record"""
    cursor = self.cursor
    cursor.execute(query, data)

    return cursor.fetchone()

  def all( self, query, data ):
    """Execute query and return all records"""
    cursor = self.cursor
    cursor.execute(query, data)

    return cursor.fetchall()

  def close( self ):
    """Close connection"""
    self._connection.commit()
    self._connection.close()

class DataBaseHost:

  _list = {}

  @staticmethod
  def get( file_path ):
    """Get databse"""
    
    if file_path in DataBaseHost._list:
      db = DataBaseHost._list[ file_path ]
    else:
      db = DataBase( file_path )

    return db

  @staticmethod
  def close():
    """Close all connections"""
    for key in DataBaseHost._list:
      DataBaseHost._list[ key ].close()

    return True

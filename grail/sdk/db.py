#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sqlite3 as lite


class DataBase:
  """SQLite database wrapper"""

  _connection = None

  def __init__( self, file_path, file_copy = False, query = False, create = True ):
    """Create SQLite database wraper

    Args:
      - file_path: database file path
      - file_copy: copy file if file_path not exists
      - query: execute query if file_path not exists
      - create: create database file or not
    """
    directory = os.path.dirname(os.path.realpath( file_path ))
    execute_query = False

    if not create and (not os.path.exists( directory ) or
       not os.path.isfile( file_path )):
      raise Exception("Database file not exists. Unable to open sqlite file.")

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
      self.cursor.executescript(query)

  @property
  def connection( self ):
    """Returns sqlite3 connection"""
    return self._connection

  @property
  def cursor( self ):
    """Returns sqlite3 connection cursor"""
    return self._connection.cursor()

  def get( self, query, data=tuple() ):
    """Execute query and return first record"""
    cursor = self.cursor
    cursor.execute(query, data)

    return cursor.fetchone()

  def all( self, query, data=tuple() ):
    """Execute query and return all records"""
    cursor = self.cursor
    cursor.execute(query, data)

    return cursor.fetchall()

  def close( self ):
    """Close connection"""
    self._connection.commit()
    self._connection.close()


class DataBaseHost:
  """Host all sqlite database connections"""

  _list = {}

  @staticmethod
  def get( file_path, file_copy = False, query = False, create = True  ):
    """Get databse"""
    
    file_path = os.path.abspath(file_path)

    if file_path in DataBaseHost._list:
      db = DataBaseHost._list[ file_path ]
    else:
      db = DataBase( file_path, file_copy, query, create )
      DataBaseHost._list[ file_path ] = db

    return db

  @staticmethod
  def close():
    """Close all connections"""
    for key in DataBaseHost._list:
      DataBaseHost._list[ key ].close()

    return True

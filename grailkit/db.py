# -*- coding: UTF-8 -*-
"""
    grailkit.db
    ~~~~~~~~~~~

    Simplified interface to sqlite database
"""
import os
import re
import sqlite3 as lite

from grailkit import util


def create_factory(object_def, cursor, row):
    """Create factory

    Args:
        object_def: callable object
        cursor (sqlite3.Cursor): database cursor
        row (sqlite3.Row): database row object
    Returns:
        instance of `object_def`
    """
    return object_def(row, cursor)


class DataBaseError(Exception):
    """Base class for DataBase Errors"""
    pass


class DataBase:
    """SQLite database wrapper"""

    # sqlite connection handler
    _connection = None

    def __init__(self, file_path, file_copy=False, query="", create=False):
        """Create SQLite database wrapper

        Args:
            file_path (str): database file path
            file_copy (str): copy file if file_path not exists
            query (str): execute query if file_path not exists
            create (bool): create database file or not
        """

        directory = os.path.dirname(os.path.realpath(file_path))
        execute_query = False

        if not create and (not os.path.exists(directory) or
           not os.path.isfile(file_path)):
            raise DataBaseError("Database file not exists. Unable to open sqlite file.")

        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.isfile(file_path):
            if file_copy:
                util.copy_file(file_copy, file_path)
            else:
                open(file_path, 'w+')
                execute_query = True

        self._connection = lite.connect(file_path)
        self._connection.row_factory = lite.Row

        def lowercase(char):
            return char.lower()

        def search_strip(char):
            char = re.sub(r'[\[_\]\.\-,!\(\)\"\':;]', '', char)
            char = re.sub('[\s+]', '', char)

            return char.lower()

        self._connection.create_function("lowercase", 1, lowercase)
        self._connection.create_function("search_strip", 1, search_strip)

        if execute_query and query:
            self.cursor.executescript(query)

    @property
    def connection(self):
        """Returns sqlite3 connection"""

        return self._connection

    @property
    def cursor(self):
        """Returns sqlite3 connection cursor"""

        return self._connection.cursor()

    def get(self, query, data=tuple(), factory=None):
        """Execute query and return first record

        Args:
            query (str): SQL query string
            data (tuple): tuple of data
            factory: sqlite row factory
        Returns:
            first row
        """

        if factory:
            self.set_factory(factory)

        cursor = self.cursor
        cursor.execute(query, data)

        result = cursor.fetchone()
        self.set_factory()

        return result

    def all(self, query, data=tuple(), factory=None):
        """Execute query and return all records

        Args:
            query (str): SQL query string
            data (tuple): tuple of data
            factory: sqlite row factory for this query only
        Returns:
            list of fetched rows
        """

        if factory:
            self.set_factory(factory)

        cursor = self.cursor
        cursor.execute(query, data)

        result = cursor.fetchall()
        self.set_factory()

        return result

    def execute(self, query, data=tuple()):
        """Execute query

        Args:
            query (str): SQL query string
            data (tuple): tuple of data
        """

        cursor = self.cursor
        cursor.execute(query, data)

    def set_factory(self, factory=lite.Row):
        """Set sqlite row factory

        Args:
            factory (sqlite3.Row): factory object
        """

        self.connection.row_factory = factory

    def close(self):
        """Close connection"""

        self._connection.commit()
        self._connection.close()


class DataBaseHost:
    """Host all sqlite database connections"""

    # list of all connected databases
    _list = {}

    @staticmethod
    def get(file_path, file_copy=False, query="", create=True):
        """Get database object

        Args:
            file_path (str): path to database file
            file_copy (str): copy file from `file_copy` if `file_path` not exists
            query (str): execute query if file `file_path` not exists
            create (bool): create database file or not
        Returns
            DataBase object if open or opens database and returns it.
        """

        file_path = os.path.abspath(file_path)

        if file_path in DataBaseHost._list:
            db = DataBaseHost._list[file_path]
        else:
            db = DataBase(file_path, file_copy, query, create)
            DataBaseHost._list[file_path] = db

        return db

    @staticmethod
    def close():
        """Close all connections"""

        for key in DataBaseHost._list:
            DataBaseHost._list[key].close()

        return True

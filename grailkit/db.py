# -*- coding: UTF-8 -*-
"""
    grailkit.db
    ~~~~~~~~~~~

    Simplified interface to SQLite database

    :copyright: (c) 2018 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import os
import re
import sqlite3
import logging

from grailkit import util


logging.getLogger(__name__).addHandler(logging.NullHandler())


def create_factory(object_def, cursor, row):
    """Create object factory

    Args:
        object_def (callable): callable object
        cursor (sqlite3.Cursor): database cursor
        row (sqlite3.Row): database row object
    Returns:
        instance of `object_def`
    """

    if not object_def or not callable(object_def):
        raise DataBaseError("Can't create factory with given object. Object is not callable or not exists.")

    return object_def(row, cursor)


class DataBaseError(Exception):
    """Base class for DataBase Errors"""

    pass


class DataBase:
    """SQLite database wrapper"""

    # sqlite connection handler
    _connection = None

    def __init__(self, file_path, file_copy=False, query="", create=False):
        """Create SQLite database wrapper.
        Also define custom functions sql `lowercase` an `search_strip`.

        Args:
            file_path (str): database file path
            file_copy (str): copy file if file_path not exists
            query (str): execute query if file_path not exists
            create (bool): create database file or not
        """

        directory = os.path.dirname(os.path.realpath(file_path))
        execute_query = False

        if not create and not util.file_exists(file_path):
            raise DataBaseError("Database file not exists. Unable to open sqlite file @ %s." % file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.isfile(file_path):
            if file_copy:
                util.copy_file(file_copy, file_path)
            else:
                file_handle = open(file_path, 'w+')
                file_handle.close()
                execute_query = True

        self._connection = sqlite3.connect(file_path)
        self._connection.row_factory = sqlite3.Row
        self._location = file_path

        def lowercase(char):
            """Lover string

            Args:
                char (str): string to process
            """
            return char.lower()

        def search_strip(char):
            """Prepare string for search

            Args:
                char (str): string to process
            """
            char = re.sub(r'[\[_\].\-,!()\"\':;]', '', char)
            char = re.sub('[\s+]', '', char)

            return char.lower()

        self._connection.create_function("lowercase", 1, lowercase)
        self._connection.create_function("search_strip", 1, search_strip)

        if execute_query and query:
            self.cursor.executescript(query)

        DataBaseHost.add(self)

    @property
    def connection(self):
        """Returns sqlite3 connection object"""

        return self._connection

    @property
    def cursor(self):
        """Returns sqlite3 connection cursor"""

        return self._connection.cursor()

    @property
    def location(self):
        """Returns location of database file"""

        return self._location

    def get(self, query, data=tuple(), factory=None):
        """Execute query and return first record

        Args:
            query (str): SQL query string
            data (tuple): tuple of data
            factory (callable): sqlite row factory
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
            factory (callable): sqlite row factory for this query only
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
        """Execute many sql queries at once

        Args:
            query (str): SQL query string
            data (tuple): tuple of data
        """

        cursor = self.cursor
        cursor.execute(query, data)

    def set_factory(self, factory=sqlite3.Row):
        """Set sqlite row factory function.
        If you call `set_factory` without arguments default factory will be used

        Example:
            def string_factory(cursor, row):
                return [str(value) for value in row]

        Args:
            factory (callable): factory object
        """

        self._connection.row_factory = factory

    def copy(self, file_path, create=False):
        """Copy database to new file location

        Args:
            file_path (str): path to new file
            create (bool): create file if not exists
        """

        directory = os.path.dirname(os.path.realpath(file_path))

        if not file_path:
            raise ValueError('Path to the file is invalid')

        if not create and not util.file_exists(file_path):
            raise DataBaseError('Unable to copy database, file %s not exists.' % file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.isfile(file_path):
            file_handle = open(file_path, 'w+')
            file_handle.close()

        db = sqlite3.connect(file_path)
        query = "".join(line for line in self._connection.iterdump())

        db.executescript(query)
        db.commit()
        db.close()

    def commit(self):
        """Commit changes to database"""

        self._connection.commit()

    def close(self):
        """Commit changes to database and close connection"""

        try:
            self._connection.commit()
        except sqlite3.ProgrammingError:
            logging.info("Unable to commit into %s, connection was closed" % (self._location, ))

        # close if this connection is not used by others
        if not DataBaseHost.has(self._location):
            self._connection.close()


class DataBaseHost:
    """Host all sqlite database connections"""

    # list of all connected databases
    _list = {}

    @classmethod
    def get(cls, file_path, file_copy=False, query="", create=True):
        """Get DataBase object

        Args:
            file_path (str): path to database file
            file_copy (str): copy file from `file_copy` if `file_path` not exists
            query (str): execute query if file `file_path` not exists
            create (bool): create database file or not
        Returns:
            DataBase object if opened or opens database and returns it.
        """

        file_path = os.path.abspath(file_path)

        if file_path in DataBaseHost._list:
            db = cls._list[file_path]
        else:
            db = DataBase(file_path, file_copy, query, create)
            cls._list[file_path] = db

        return db

    @classmethod
    def add(cls, db_ref):
        """Add DataBase object to list if not exists

        Args:
            db_ref (DataBase): reference to database error
        Raises:
            DataBaseError: If wrong object were passed
        """

        if not db_ref or not isinstance(db_ref, DataBase):
            raise DataBaseError("DataBase object doesn't exists or it's not an instance of DataBase class.")

        file_path = os.path.abspath(db_ref.location)

        if file_path not in cls._list:
            cls._list[db_ref.location] = db_ref

    @classmethod
    def has(cls, file_path):
        """Returns True if `file_path` in list of opened connections

        Args:
            file_path (str): file location
        """

        return os.path.abspath(file_path) in cls._list

    @staticmethod
    def close():
        """Close all connections

        Returns:
            bool: True if all connections closed successfully
        """

        for key in DataBaseHost._list:
            DataBaseHost._list[key].close()

        return True

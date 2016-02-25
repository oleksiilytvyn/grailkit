#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

import os
import shutil
import tempfile
import grailkit.db as db
import sqlite3 as sqlite

QUERY_CREATE = """CREATE TABLE `test` (`key` TEXT NOT NULL, `value` TEXT, PRIMARY KEY(key));"""
QUERY_INSERT = """INSERT INTO `test` VALUES('key', 'value')"""
QUERY_GET = """SELECT * FROM `test`"""
QUERY_MULTIPLE = """
    create table person(
        firstname,
        lastname,
        age
    );

    create table book(
        title,
        author,
        published
    );

    insert into book(title, author, published)
    values (
        'Dirk Gently''s Holistic Detective Agency',
        'Douglas Adams',
        1987
    );
    """
QUERY_INSERT_MULTIPLE = """
    INSERT INTO `test` ('key', 'value') VALUES
        ('one', 'first'),
        ('two', 'second'),
        ('three', 'third');
    """


class TestGrailkitDB(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.res_dir = os.path.abspath(__file__[:-3])

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_db_create(self):
        """Test database create"""

        db_path = os.path.join(self.test_dir, 'test.sqlite')
        db_obj = db.DataBase(db_path, query=QUERY_CREATE, create=True)
        db_obj.close()

        self.assertTrue(os.path.isfile(db_path))

    def test_db_open(self):
        """Test database open"""

        db_path = os.path.join(self.res_dir, 'regular.sqlite')
        db_obj = db.DataBase(db_path)
        db_obj.close()

        self.assertTrue(True)

    def test_db_open_not_exists(self):
        """Test database open if file not exists"""

        db_path = os.path.join(self.res_dir, 'file_not_exists.sqlite')

        self.assertRaises(db.DataBaseError, db.DataBase, db_path)

    def test_db_open_corrupt(self):
        """Test database open if file corrupted"""

        db_path = os.path.join(self.res_dir, 'file_not_exists.sqlite')

        self.assertRaises(db.DataBaseError, db.DataBase, db_path)

    def test_db_connection(self):
        db_path = os.path.join(self.res_dir, 'regular.sqlite')
        db_obj = db.DataBase(db_path)

        self.assertTrue(isinstance(db_obj.connection, sqlite.Connection))

        db_obj.close()

    def test_db_cursor(self):
        db_path = os.path.join(self.res_dir, 'regular.sqlite')
        db_obj = db.DataBase(db_path)

        self.assertTrue(isinstance(db_obj.cursor, sqlite.Cursor))

        db_obj.close()

    def test_db_get(self):

        db_path = os.path.join(self.test_dir, 'get.sqlite')
        db_obj = db.DataBase(db_path, create=True)

        db_obj.execute(QUERY_CREATE)
        db_obj.execute(QUERY_INSERT)
        res = db_obj.get(QUERY_GET)

        self.assertEqual(res[0], 'key')
        self.assertEqual(res[1], 'value')

        self.assertEqual(res['key'], 'key')
        self.assertEqual(res['value'], 'value')

        db_obj.close()

    def test_db_all(self):

        db_path = os.path.join(self.test_dir, 'get.sqlite')
        db_obj = db.DataBase(db_path, create=True)

        db_obj.execute(QUERY_CREATE)
        db_obj.execute(QUERY_INSERT_MULTIPLE)

        res = db_obj.all(QUERY_GET)

        self.assertEqual(res[0][0], 'one')
        self.assertEqual(res[0][1], 'first')

        self.assertEqual(res[1][0], 'two')
        self.assertEqual(res[1][1], 'second')

        self.assertEqual(res[2][0], 'three')
        self.assertEqual(res[2][1], 'third')

        db_obj.close()

    def test_execute(self):

        db_path = os.path.join(self.test_dir, 'execute.sqlite')
        db_obj = db.DataBase(db_path, create=True)

        db_obj.execute(QUERY_CREATE)
        db_obj.execute(QUERY_INSERT)

        self.assertTrue(isinstance(db_obj.cursor, sqlite.Cursor))
        self.assertRaises(sqlite.Warning, db_obj.execute, QUERY_MULTIPLE)

        db_obj.close()


if __name__ == "__main__":
    unittest.main()

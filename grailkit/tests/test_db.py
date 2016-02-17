#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

import os
import shutil
import tempfile
import grailkit.db as db

QUERY_CREATE = """CREATE TABLE `test` (`key` TEXT NOT NULL, `value` TEXT, PRIMARY KEY(key));"""


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

if __name__ == "__main__":
    unittest.main()

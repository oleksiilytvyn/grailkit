# -*- coding: UTF-8 -*-

import unittest

import os
import shutil
import tempfile

import grailkit.bible as bible


class TestGrailkitBible(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.res_dir = os.path.abspath(__file__[:-3])

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_open(self):
        """Test reading from bible file"""

        path = os.path.join(self.res_dir, "bible-en-kjv.grail-bible")
        db_obj = bible.Bible(path)

        self.assertEqual(db_obj.title, "King James Version")
        self.assertEqual(db_obj.copyright, "We believe that this Bible is found in the Public Domain.")
        self.assertEqual(db_obj.version, '1')
        self.assertEqual(db_obj.verse(1, 1, 1).text, "In the beginning God created the heaven and the earth.")

        # get non existed verse
        self.assertEqual(db_obj.verse(512, 1, 1), None)

        db_obj.close()

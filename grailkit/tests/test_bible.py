# -*- coding: UTF-8 -*-
"""
    grailkit.tests.test_bible
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for bible module

    :copyright: (c) 2018 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import unittest

import os
import shutil
import tempfile

import grailkit.dna as dna
import grailkit.bible as bible


class TestGrailkitBible(unittest.TestCase):

    def setUp(self):
        """Create a temporary directory"""

        self.test_dir = tempfile.mkdtemp()
        self.res_dir = os.path.abspath(__file__[:-3])

    def tearDown(self):
        """Remove the directory after the test"""

        shutil.rmtree(self.test_dir)

    def test_open(self):
        """Test reading from bible file"""

        path = os.path.join(self.res_dir, "bible-en-kjv.grail-bible")
        db_obj = bible.Bible(path)
        db_obj.close()

    def test_open_corrupted(self):
        """Test opening corrupted bible file"""

        with self.assertRaises(dna.DNAError):
            path = os.path.join(self.res_dir, "bible-ru-rst.grail-bible")
            db_obj = bible.Bible(path)
            db_obj.close()

    def test_properties(self):
        """Test Bible properties and methods"""

        path = os.path.join(self.res_dir, "bible-en-kjv.grail-bible")
        db_obj = bible.Bible(path)

        # test bible properties
        self.assertEqual(db_obj.title, "King James Version")
        self.assertEqual(db_obj.version, '1')
        self.assertEqual(db_obj.copyright, "We believe that this Bible is found in the Public Domain.")
        self.assertEqual(db_obj.description, 'In 1604, King James I of England authorized that a new translation of '
                                             'the Bible into English be started. It was finished in 1611, just 85 '
                                             'years after the first translation of the New Testament into English '
                                             'appeared (Tyndale, 1526). The Authorized Version, or King James Version, '
                                             'quickly became the standard for English-speaking Protestants. '
                                             'Its flowing language and prose rhythm has had a profound influence on '
                                             'the literature of the past 300 years.')
        self.assertEqual(db_obj.date, '2009-01-23')
        self.assertEqual(db_obj.language, 'en')
        self.assertEqual(db_obj.location, path)
        self.assertEqual(db_obj.identifier, 'kjv')

        db_obj.close()

    def test_methods(self):
        """Test Bible instance methods"""

        path = os.path.join(self.res_dir, "bible-en-kjv.grail-bible")
        db_obj = bible.Bible(path)

        # get verse
        self.assertEqual(db_obj.verse(1, 1, 1).text, "In the beginning God created the heaven and the earth.")

        # get non existed verse
        self.assertEqual(db_obj.verse(512, 1, 1), None)

        self.assertTrue(isinstance(db_obj.json_info(), str))
        self.assertEqual(len(db_obj.books()), 66)
        self.assertTrue(isinstance(db_obj.book(1), bible.Book))

        db_obj.close()

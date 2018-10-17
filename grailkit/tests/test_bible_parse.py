# -*- coding: UTF-8 -*-
"""
    grailkit.tests.test_bible_parse
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for bible_parse module

    :copyright: (c) 2018 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import unittest

import os
import shutil
import tempfile

import grailkit.bible as bible
import grailkit.bible_parse as parse


class TestGrailkitBible(unittest.TestCase):

    def setUp(self):
        """Create a temporary directory"""

        self.test_dir = tempfile.mkdtemp()
        self.res_dir = os.path.abspath(__file__[:-3])

    def tearDown(self):
        """Remove the directory after the test"""

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_parse(self):
        """Try to parse file"""

        with self.assertRaises(NotImplementedError):
            file_in = os.path.join(self.res_dir, "bible-ru-rst.osis")
            file_out = os.path.join(self.test_dir, "bible-en-kjv.grail-bible")

            parse.Parser(file_in, file_out)

    def test_parse_non_existed(self):
        """Test opening of non-existed file"""

        with self.assertRaises(bible.BibleError):
            file_in = os.path.join(self.res_dir, "bible-en-kjv.osis")
            file_out = os.path.join(self.test_dir, "bible-en-kjv.grail-bible")

            parse.Parser(file_in, file_out)

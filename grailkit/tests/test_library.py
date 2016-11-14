# -*- coding: UTF-8 -*-

import unittest

import os
import json
import shutil
import tempfile

import grailkit
from grailkit.dna import DNA
from grailkit.library import Library


class TestGrailkitProject(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.res_dir = os.path.abspath(__file__[:-3])

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_library(self):
        path = os.path.join(self.test_dir, 'library.grail')
        lib = Library(path, create=True)

        for i in range(10):
            lib.create("Item #%d" % (i,), entity_type=DNA.TYPE_FILE)

        song = lib.create("First song", entity_type=DNA.TYPE_SONG)
        song.lyrics = "Hello world!"
        song.genre = "Experimental"

        found = lib.items(filter_keyword="song")

        self.assertEqual(len(lib.items()), 11)
        self.assertEqual(found[0].name, "First song")
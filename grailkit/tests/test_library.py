# -*- coding: UTF-8 -*-

import unittest

import os
import shutil
import tempfile

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
            lib.create("Item #%d" % (i,))

        found = lib.find(keyword="5")

        self.assertEqual(len(lib.items()), 10)
        self.assertEqual(found[0].name, "Item #5")

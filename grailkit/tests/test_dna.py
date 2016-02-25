#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

import os
import shutil
import tempfile
import grailkit.dna as dna


class TestGrailkitDNA(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.res_dir = os.path.abspath(__file__[:-3])

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_dna_create(self):
        pass

    def test_dna_open(self):
        pass

    def test_dna_corrupted(self):
        pass

    def test_dna_property(self):
        pass

    def test_dna_entity(self):
        pass

    def test_dna_has_childs(self):
        pass

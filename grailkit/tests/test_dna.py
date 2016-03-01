#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

import os
import shutil
import tempfile

import grailkit.dna as dna
import grailkit.db as db


class TestGrailkitDNA(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.res_dir = os.path.abspath(__file__[:-3])

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_dna_create(self):

        db_path = os.path.join(self.test_dir, 'test.grail')
        db_obj = dna.DNAFile(db_path, create=True)
        db_obj.close()

        self.assertTrue(os.path.isfile(db_path))

    def test_dna_open(self):
        pass

    def test_dna_corrupted(self):

        db_path = os.path.join(self.res_dir, 'corrupted.grail')

        self.assertRaises(db.DataBaseError, dna.DNAFile, db_path)

    def test_dna_property(self):

        db_path = os.path.join(self.test_dir, 'test.grail')
        db_obj = dna.DNAFile(db_path, create=True)

        # test property insertion
        db_obj.set_property(0, "name", "java")
        self.assertEqual(db_obj.get_property(0, "name"), "java")

        # test property update
        db_obj.set_property(0, "name", "vala")
        self.assertEqual(db_obj.get_property(0, "name"), "vala")

        # get non existent property
        self.assertEqual(db_obj.get_property(0, "non-existent"), None)

        db_obj.close()

    def test_dna_entity(self):

        entity1 = dna.DNAEntity()
        entity1.name = "project"
        entity1.parent = 0

        entity2 = dna.DNAEntity()
        entity2.content = [0, 2, 3]
        entity2.name = "cuelist"
        entity2.parent = 1
        entity2.search = "cuelist 1 (0 2 3)"

        db_path = os.path.join(self.test_dir, 'entity.grail')
        db_obj = dna.DNAFile(db_path, create=True)

        eid1 = db_obj.add(entity1)
        print(eid1, db_obj.entity(eid1))

        eid2 = db_obj.add(entity2)
        print(eid2, db_obj.entity(eid2))

        db_obj.set_property(eid1, "author", "Alex Litvin")
        db_obj.set_property(eid1, "description", "testing DNA file")

        db_obj.set_property(eid2, "author", "Alex Litvin")
        db_obj.set_property(eid2, "description", "simple cuelist")
        db_obj.set_property(eid2, "color", "#f00")

        self.assertTrue(db_obj.entity_has_childs(eid1))
        self.assertFalse(db_obj.entity_has_childs(eid2))

        print("entities:")
        for entity in db_obj.entities():
            print(entity)

        print("entity 1 properties")
        for prop in db_obj.properties(eid1):
            print(list(prop))

        print("entity 2 properties")
        for prop in db_obj.properties(eid2):
            print(list(prop))

        db_obj.close()

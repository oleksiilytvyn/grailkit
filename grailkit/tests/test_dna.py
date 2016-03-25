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
        db_obj.set(0, "name", "java")
        self.assertEqual(db_obj.get(0, "name"), "java")

        # test property update
        db_obj.set(0, "name", "vala")
        self.assertEqual(db_obj.get(0, "name"), "vala")

        # get non existent property
        self.assertEqual(db_obj.get(0, "non-existent"), None)

        db_obj.close()

    def test_dna_entity(self):

        db_path = os.path.join(self.test_dir, 'entity.grail')
        db_obj = dna.DNAFile(db_path, create=True)

        entity1 = db_obj.create(name="project", parent=0)
        entity1.update()

        entity2 = db_obj.create(name="cuelist", parent=entity1.id)
        entity2.content = [0, 2, 3]
        entity2.search = "cuelist 1 (0 2 3)"
        entity2.update()

        eid1 = entity1.id
        eid2 = entity2.id

        db_obj.set(eid1, "author", "Alex Litvin")
        db_obj.set(eid1, "description", "testing DNA file")

        db_obj.set(eid2, "author", "Alex Litvin")
        db_obj.set(eid2, "description", "simple cuelist")
        db_obj.set(eid2, "length", 2)
        db_obj.set(eid2, "ratio", 3.1516)
        db_obj.set(eid2, "list", [1, 2, 3, 4])

        self.assertEqual(type(db_obj.get(eid2, 'length')), int)
        self.assertEqual(type(db_obj.get(eid2, 'ratio')), float)
        self.assertEqual(type(db_obj.get(eid2, 'list')), list)

        self.assertTrue(db_obj.has_childs(eid1))
        self.assertFalse(db_obj.has_childs(eid2))

        self.assertEqual(len(db_obj.entities()), 2)
        self.assertEqual(len(db_obj.properties(eid1)), 2)
        self.assertEqual(len(db_obj.properties(eid2)), 5)

        db_obj.close()

    def test_dna_fill(self):

        db_path = os.path.join(self.test_dir, 'entity.grail')
        dna_file = dna.DNAFile(db_path, create=True)

        # settings
        settings = dna_file.create()
        settings.name = "settings"

        settings.set('display.background', '#000000')

        settings.set('display.text.align', 1)
        settings.set('display.text.valign', 1)
        settings.set('display.text.case', 'uppercase')

        settings.set('display.font.family', 'Helvetica')
        settings.set('display.font.size', '32pt')
        settings.set('display.font.weight', 'normal')
        settings.set('display.font.style', 'normal')
        settings.set('display.font.color', '#FFFFFF')

        settings.set('display.shadow.x', 0)
        settings.set('display.shadow.y', 2)
        settings.set('display.shadow.blur', 10)
        settings.set('display.shadow.color', '#000000')

        settings.set('display.padding.left', 10)
        settings.set('display.padding.right', 10)
        settings.set('display.padding.top', 10)
        settings.set('display.padding.bottom', 10)
        settings.set('display.padding.box', 10)

        settings.set('display.composition.x', 0)
        settings.set('display.composition.y', 0)
        settings.set('display.composition.width', 1920)
        settings.set('display.composition.height', 1080)

        settings.set('display.geometry.x', 1920)
        settings.set('display.geometry.y', 0)
        settings.set('display.geometry.width', 1920)
        settings.set('display.geometry.height', 1080)

        settings.set('display.disabled', False)
        settings.set('display.display', 'DISPLAY//2')
        settings.set('display.testcard', False)
        settings.set('display.fullscreen', True)
        settings.update()

        # project
        project = dna_file.create()
        project.name = "Grail Project"
        project.set('author', 'Alex Litvin')
        project.set('description', 'Simple Grail project for testing purposes')
        project.update()

        # cuelist
        for cuelist_index in range(5):
            cuelist = dna_file.create(parent=project.id)
            cuelist.name = "%d'st Cuelist" % (cuelist_index,)
            cuelist.set('color', '#FF0000')
            cuelist.set('description', 'Simple cuelist')
            cuelist.update()

            for cue_index in range(5):
                cue = dna_file.create(parent=cuelist.id)
                cue.name = "Cue %d in list %d" % (cue_index, cuelist_index)
                cue.set('color', '#00FF00')
                cue.set('continue', 0)
                cue.set('wait_pre', 100)
                cue.set('wait_post', 30)
                cue.update()

        self._print_childs(dna_file, 0)

    def _print_childs(self, db, parent, indent=''):

        for entity in db.entities(filter_parent=parent):

            print('\n' + indent + '@', entity.id, entity.name, entity)

            for key in entity.properties():
                print(indent + "-", key, ':', entity.get(key))

            self._print_childs(db, entity.id, indent+'  ')

# -*- coding: UTF-8 -*-

import unittest

import os
import shutil
import tempfile

import grailkit.dna as dna
import grailkit.db as db


class TestGrailkitDNA(unittest.TestCase):

    def setUp(self):
        """Create a temporary directory"""

        self.test_dir = tempfile.mkdtemp()
        self.res_dir = os.path.abspath(__file__[:-3])

    def tearDown(self):
        """Remove the directory after the test"""

        shutil.rmtree(self.test_dir)

    def test_dna_signal(self):
        """Test DNASignal class"""

        self.called_counter = 0

        def slot(counter):
            self.called_counter += 1

        signal = dna.DNASignal(int)
        signal.connect(slot)
        signal.emit(self.called_counter)

        signal.connect(slot, name='slot')
        signal.emit(self.called_counter, name='slot')
        signal.emit(self.called_counter)

        self.assertEqual(len(signal), 2)
        self.assertEqual(self.called_counter, 4)

    def test_dna_create(self):

        db_path = os.path.join(self.test_dir, 'test.grail')
        db_obj = dna.DNAFile(db_path, create=True)
        db_obj.close()

        self.assertTrue(os.path.isfile(db_path))

    def test_dna_open(self):

        db_path = os.path.join(self.res_dir, 'dna.grail')
        db_obj = dna.DNAFile(db_path)
        db_obj.close()

        self.assertTrue(os.path.isfile(db_path))
        self.assertEquals(db_obj.location, db_path)

    def test_dna_corrupted(self):
        """Try to load corrupted DNA file"""

        db_path = os.path.join(self.res_dir, 'corrupted.grail')

        self.assertRaises(db.DataBaseError, dna.DNAFile, db_path)

    def test_dna_property(self):
        """Test properties handling"""

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
        """Test DNAEntity methods"""

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

        self.assertEqual(db_obj.has(eid1, 'author'), True)
        self.assertEqual(db_obj.has(eid1, 'not-existed-property'), False)
        self.assertEqual(len(db_obj.entities()), 2)
        self.assertEqual(len(db_obj.properties(eid1)), 2)
        self.assertEqual(len(db_obj.properties(eid2)), 5)

        db_obj.close()

    def test_dna_fill(self):
        """Test DNA file entities creation"""

        db_path = os.path.join(self.test_dir, 'entity.grail')
        dna_file = dna.DNAFile(db_path, create=True)

        # settings
        settings = dna_file.create(name="settings")

        settings.set('display.background', '#000000')

        settings.set('display.text.align', 1)
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
        project = dna_file.create(name="Grail Project")
        project.set('author', 'Alex Litvin')
        project.set('description', 'Simple Grail project for testing purposes')
        project.update()

        # cuelist
        for cuelist_index in range(5):
            cuelist = dna_file.create(name="%d'st Cuelist" % (cuelist_index,), parent=project.id)
            cuelist.set('color', '#FF0000')
            cuelist.set('description', 'Simple cuelist')
            cuelist.update()

            for cue_index in range(5):
                cue = dna_file.create(name="Cue %d in list %d" % (cue_index, cuelist_index), parent=cuelist.id)
                cue.set('color', '#00FF00')
                cue.set('continue', 0)
                cue.set('wait_pre', 100)
                cue.set('wait_post', 30)
                cue.update()

    def test_dna_copy(self):
        """Test entity copy"""

        db_path = os.path.join(self.test_dir, 'entity.grail')
        dna_file = dna.DNAFile(db_path, create=True)

        entity = dna_file.create(name="Hello world!", index=3)
        entity.set('property', True)
        entity.set('color', '#dedede')

        copy = dna_file.copy(entity, name="Hello Again!")

        self.assertEqual(len(entity.properties()), len(copy.properties()))
        self.assertEqual(len(dna_file.entities()), 2)

        dna_file.close()

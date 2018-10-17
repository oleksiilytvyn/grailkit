# -*- coding: UTF-8 -*-
"""
    grailkit.tests.test_dna
    ~~~~~~~~~~~~~~~~~~~~~~~

    Tests for dna module

    :copyright: (c) 2018 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import unittest

import os
import shutil
import tempfile

import grailkit.dna as dna
import grailkit.db as db
import grailkit.core as core


class TestGrailkitDNA(unittest.TestCase):

    def setUp(self):
        """Create a temporary directory"""

        self.test_dir = tempfile.mkdtemp()
        self.res_dir = os.path.abspath(__file__[:-3])

    def tearDown(self):
        """Remove the directory after the test"""

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_dna_signal(self):
        """Test DNASignal class"""

        bucket = []

        def slot(ref):
            """Regular slot callback"""

            ref.append('regular slot')

        def named_slot(ref):
            """Named slot callback"""

            ref.append('named slot')

        class T:
            """Test class"""

            def foo(self, ref):
                """Class slot callback"""

                ref.append('class slot %s' % str(self))

        t = T()

        signal = core.Signal(list)
        signal.connect(slot)
        signal.connect(named_slot, name='slot')
        signal.connect(lambda ref: bucket.append('lambda slot'))
        signal.connect(t.foo)
        signal.emit(bucket)

        # two signals called at once
        self.assertEqual(len(bucket), 4)

        signal.emit(bucket, name='slot')

        # last called slot is named
        self.assertEqual(bucket[4], 'named slot')

        # count signals
        self.assertEqual(len(signal), 4)

        signal.disconnect(named_slot)
        signal.emit(bucket)
        signal.emit(bucket, name='slot')

        # count signals an calls
        self.assertEqual(len(signal), 4)
        self.assertEqual(len(bucket), 10)

    def test_dna_create(self):
        """Test creation of new DNA file"""

        db_path = os.path.join(self.test_dir, 'test.grail')
        db_obj = dna.DNAFile(db_path, create=True)
        db_obj.close()

        self.assertTrue(os.path.isfile(db_path))

    def test_dna_open(self):
        """Test opening of regular DNA file"""

        db_path = os.path.join(self.res_dir, 'dna.grail')
        db_obj = dna.DNAFile(db_path)
        db_obj.close()

        self.assertTrue(os.path.isfile(db_path))
        self.assertEqual(db_obj.location, db_path)

    def test_dna_corrupted(self):
        """Try to load corrupted DNA file"""

        db_path = os.path.join(self.res_dir, 'corrupted.grail')

        self.assertRaises(db.DataBaseError, dna.DNAFile, db_path)

    def test_dna_property(self):
        """Test DNA properties handling"""

        db_path = os.path.join(self.test_dir, 'test.grail')
        ref = dna.DNAFile(db_path, create=True)

        # set
        ref.set(0, 'language', 'python 3')
        ref.set(0, 'version', 3.4)
        ref.set(0, 'object', {'key': 'value'})
        ref.set(0, 'happy', True)
        ref.set(0, 'unhappy', False)
        ref.set(0, 'none-value', None)

        # get
        self.assertEqual(ref.get(0, 'language'), 'python 3')
        self.assertEqual(ref.get(0, 'version'), 3.4)
        self.assertEqual(ref.get(0, 'object'), {'key': 'value'})
        self.assertEqual(ref.get(0, 'happy'), True)
        self.assertEqual(ref.get(0, 'non-existed'), None)
        self.assertEqual(ref.get(0, 'non-existed', default='default'), 'default')
        self.assertEqual(ref.get(0, 'unhappy'), False)
        self.assertEqual(ref.get(0, 'none-value'), None)

        # has
        self.assertTrue(ref.has(0, 'version'))
        self.assertFalse(ref.has(0, 'non-existed'))

        # properties
        props = ref.properties(0)

        self.assertEqual(len(props), 6)
        self.assertEqual(props['version'], 3.4)

        # rename
        ref.rename(0, 'language', 'lang')
        self.assertTrue(ref.has(0, 'lang'))
        self.assertFalse(ref.has(0, 'language'))

        # unset
        ref.unset(0, 'happy')

        self.assertEqual(len(ref.properties(0)), 5)

        # unset_all
        ref.unset_all(0)

        self.assertEqual(len(ref.properties(0)), 0)

        ref.close()

    def test_dna_property_types(self):
        """Test DNA properties types"""

        db_path = os.path.join(self.test_dir, 'test.grail')
        ref = dna.DNAFile(db_path, create=True)

        ref.set(0, 'none', None)
        ref.set(0, 'bool', True)
        ref.set(0, 'bool-false', False)
        ref.set(0, 'string', 'Hello World!')
        ref.set(0, 'integer', 255)
        ref.set(0, 'float', 3.1415)
        ref.set(0, 'list', [1, 2, 3, 4, 5])
        ref.set(0, 'dict', {'property': 'value'})

        self.assertEqual(type(ref.get(0, 'none')), type(None))
        self.assertEqual(type(ref.get(0, 'bool')), bool)
        self.assertEqual(type(ref.get(0, 'bool-false')), bool)
        self.assertEqual(type(ref.get(0, 'string')), str)
        self.assertEqual(type(ref.get(0, 'integer')), int)
        self.assertEqual(type(ref.get(0, 'float')), float)
        self.assertEqual(type(ref.get(0, 'list')), list)
        self.assertEqual(type(ref.get(0, 'dict')), dict)

        ref.close()

    def test_dna_entity(self):
        """Test DNAEntity methods"""

        db_path = os.path.join(self.test_dir, 'entity.grail')
        ref = dna.DNAFile(db_path, create=True)

        project = ref.create(name="project", entity_type=dna.DNA.TYPE_PROJECT)

        self.assertEqual(project.type, dna.DNA.TYPE_PROJECT)

        cuelist = project.create(name="cuelist")
        cuelist.content = [0, 2, 3]
        cuelist.search = "cuelist 1 (0 2 3)"

        self.assertEqual(cuelist.parent_id, project.id)

        eid1 = project.id
        eid2 = cuelist.id

        project.set("author", "Alex Litvin")
        project.set("description", "testing DNA file")

        cuelist.set("author", "Alex Litvin")
        cuelist.set("description", "simple cuelist")
        cuelist.set("length", 2)
        cuelist.set("ratio", 3.1516)
        cuelist.set("list", [1, 2, 3, 4])

        # check properties types
        self.assertEqual(type(cuelist.get('length')), int)
        self.assertEqual(type(cuelist.get('ratio')), float)
        self.assertEqual(type(cuelist.get('list')), list)

        self.assertTrue(ref.has_childs(eid1))
        self.assertFalse(ref.has_childs(eid2))

        self.assertEqual(project.has('author'), True)
        self.assertEqual(project.has('not-existed-property'), False)
        self.assertEqual(len(ref.entities()), 2)
        self.assertEqual(len(ref.properties(eid1)), 2)
        self.assertEqual(len(ref.properties(eid2)), 5)

        entity1 = ref.create(name="Entity 1", parent=10, properties={'key': 'value 1'})
        entity2 = ref.create(name="Entity 2", parent=10, properties={'key': 'value 2'})
        entity3 = ref.create(name="Entity 3", parent=10, properties={'key': 'value 3'})

        cuelist.append(entity1)
        cuelist.insert(0, entity2)
        cuelist.append(entity3)

        childs = cuelist.childs()

        self.assertEqual(len(childs), 3)
        self.assertEqual(childs[0].name, 'Entity 2')
        self.assertEqual(childs[1].name, 'Entity 1')
        self.assertEqual(childs[2].name, 'Entity 3')

        cuelist.remove(childs[0])
        cuelist.delete()

        ref.close()

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

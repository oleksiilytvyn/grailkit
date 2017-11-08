# -*- coding: UTF-8 -*-
"""
    grailkit.tests.test_util
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for util module

    :copyright: (c) 2017 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import unittest

import os
import time
import json
import shutil
import tempfile

from grailkit import util


class TestGrailkitCore(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_get_app_path(self):
        """Test app path"""

        self.assertIsInstance(util.application_location(), str)
        self.assertTrue(len(util.application_location()) > 0)

    def test_get_data_path(self):
        """Test path of data folder"""

        app = 'APP_NAME'

        self.assertIsInstance(util.data_location(app), str)
        self.assertTrue(util.data_location(app).index(app) >= 0)

    def test_copy_file(self):
        """Test file copy if file exists"""

        path_a = os.path.join(self.test_dir, 'test.txt')
        path_b = os.path.join(self.test_dir, 'copy/test.txt')

        # create file
        f = open(path_a, 'w')
        f.write('The owls are not what they seem')
        f.close()

        # copy file
        util.copy_file(path_a, path_b)

        self.assertTrue(os.path.isfile(path_b))

    def test_copy_file_not_exists(self):
        """Test file copy if file not exists"""

        path_a = os.path.join(self.test_dir, 'file_not_exists.txt')
        path_b = os.path.join(self.test_dir, 'copy/test.txt')

        # copy file
        util.copy_file(path_a, path_b)

        self.assertFalse(os.path.isfile(path_b))

    def test_millis_now(self):
        """Test millis_now functionality"""

        self.assertAlmostEqual(util.millis_now(), int(round(time.time() * 1000)), places=4)

    def test_json_key(self):
        """Test default_key function"""

        data = {
            'property': 'value'
            }

        class ObjectDef(object):
            """Object with property"""

            property = 'value'

        obj_data = ObjectDef()
        obj_data.property = 'value'

        self.assertEqual(util.default_key(data, 'property'), 'value')
        self.assertEqual(util.default_key(data, 'non_existed_property', 'value'), 'value')
        self.assertEqual(util.default_key(json.loads('{"key": "value"}'), 'key'), 'value')
        self.assertEqual(util.default_key(json.loads('{"key": "value"}'), 'no_key'), None)
        self.assertEqual(util.default_key(obj_data, 'property'), 'value')

        # other data types
        self.assertEqual(util.default_key(None, 'property'), None)
        self.assertEqual(util.default_key([], 'property'), None)
        self.assertEqual(util.default_key('string', 'property'), None)
        self.assertEqual(util.default_key(json.dumps('{"key": "value"}'), 'key'), None)

    def test_builtin(self):
        """Test is_builtin"""

        # Basic types will pass
        self.assertTrue(util.is_builtin(bool))
        self.assertTrue(util.is_builtin(int))
        self.assertTrue(util.is_builtin(float))
        self.assertTrue(util.is_builtin(complex))
        self.assertTrue(util.is_builtin(str))
        self.assertTrue(util.is_builtin(dict))
        self.assertTrue(util.is_builtin(list))
        self.assertTrue(util.is_builtin(set))
        self.assertTrue(util.is_builtin(frozenset))
        self.assertTrue(util.is_builtin(tuple))
        self.assertTrue(util.is_builtin(bytes))
        self.assertTrue(util.is_builtin(bytearray))

        # Check by value
        self.assertTrue(util.is_builtin(True))
        self.assertTrue(util.is_builtin(False))
        self.assertTrue(util.is_builtin([1, 2, 3]))
        self.assertTrue(util.is_builtin((1, 2, 3)))
        self.assertTrue(util.is_builtin({'a': 1, 'b': 2}))

        # Not a type
        self.assertFalse(util.is_builtin(None))


if __name__ == "__main__":
    unittest.main()

# -*- coding: UTF-8 -*-

import unittest

import os
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

    def test_get_app(self):
        """Test app path"""

        script_path = util.path_app()
        self_path = os.path.abspath('./grailkit/tests')

        self.assertEqual(script_path, self_path)

    def test_copy(self):
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

    def test_copy_not_exists(self):
        """Test file copy if file not exists"""

        path_a = os.path.join(self.test_dir, 'file_not_exists.txt')
        path_b = os.path.join(self.test_dir, 'copy/test.txt')

        # copy file
        util.copy_file(path_a, path_b)

        self.assertFalse(os.path.isfile(path_b))

if __name__ == "__main__":
    unittest.main()

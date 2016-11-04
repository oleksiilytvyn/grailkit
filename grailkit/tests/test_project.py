# -*- coding: UTF-8 -*-

import unittest

import os
import shutil
import tempfile

from grailkit.project import Project, Cuelist, Cue
from grailkit.dna import SettingsEntity


class TestGrailkitProject(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.res_dir = os.path.abspath(__file__[:-3])

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_create_project(self):
        path = os.path.join(self.test_dir, 'project.grail')
        proj = Project(path, create=True)

        props = proj.settings()
        props.set("display", "DISPLAY2")
        props.set("background", "#000000")
        props.set("cuelist", 2)
        props.set("osc-enabled", True)

        self.assertEqual(props.get("display"), "DISPLAY2")
        self.assertEqual(props.get("background"), "#000000")
        self.assertEqual(props.get("cuelist"), 2)
        self.assertEqual(props.get("osc-enabled"), True)

        cuelist = proj.append("Test Cuelist")

        self.assertEqual(cuelist.name, "Test Cuelist")
        self.assertEqual(len(proj), 1)

        cuelist.append("Cue")

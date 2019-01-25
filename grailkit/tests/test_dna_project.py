# -*- coding: UTF-8 -*-
"""
    grailkit.tests.test_dna_project
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for dna project classes

    :copyright: (c) 2017-2019 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import unittest

import os
import shutil
import tempfile

from grailkit.dna import DNA, Project


class TestGrailkitProject(unittest.TestCase):

    def setUp(self):
        """Create a temporary directory"""

        self.test_dir = tempfile.mkdtemp()
        self.res_dir = os.path.abspath(__file__[:-3])

    def tearDown(self):
        """Remove the directory after the test"""

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_create_project(self):

        path = os.path.join(self.test_dir, 'project.grail')
        project = Project(path, create=True)

        project.name = 'Testing'
        self.assertEqual(project.name, 'Testing')

        project.description = 'Testing description'
        self.assertEqual(project.description, 'Testing description')

        props = project.settings()
        props.set("display", "DISPLAY2")
        props.set("background", "#000000")
        props.set("cuelist", 2)
        props.set("osc-enabled", True)

        self.assertEqual(props.get("display"), "DISPLAY2")
        self.assertEqual(props.get("background"), "#000000")
        self.assertEqual(props.get("cuelist"), 2)
        self.assertEqual(props.get("osc-enabled"), True)

        cuelist = project.create(name='cuelist')

        self.assertEqual(cuelist.type, DNA.TYPE_CUELIST)

        cuelists = project.cuelists()

        self.assertEqual(cuelists[0].name, 'cuelist')
        self.assertEqual(cuelists[0].type, DNA.TYPE_CUELIST)

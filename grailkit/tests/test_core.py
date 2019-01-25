# -*- coding: UTF-8 -*-
"""
    grailkit.tests.test_db
    ~~~~~~~~~~~~~~~~~~~~~~

    Tests for core module

    :copyright: (c) 2017-2019 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""
import types

import unittest
from unittest.mock import Mock

from grailkit.core import *


class TestGrailkitCore(unittest.TestCase):

    def test_signal(self):
        """Test Signal"""

        func = Mock()

        signal = Signal(str, list)
        signal.connect(func)
        signal.emit('Hello')

        func.assert_called_with('Hello')

    def test_signal_types(self):
        """Test signal types template"""

        class A:
            """Test class"""

            def __init__(self):
                pass

        class B(A):
            """Test class with dependency on A"""

            def __init__(self):
                super(B, self).__init__()

        self.assertEqual(Signal(int, str, float).template, '<int>, <str>, <float>')
        self.assertEqual(Signal(int, int, int).template, '<int>, <int>, <int>')
        self.assertEqual(Signal(dict, list).template, '<dict>, <list>')
        self.assertEqual(Signal(bytes).template, '<bytes>')
        self.assertEqual(Signal({}).template, '<dict>')
        self.assertEqual(Signal(A, B).template, '<A>, <B>')
        self.assertEqual(Signal(types.FunctionType, types.FunctionType).template, '<function>, <function>')

    def test_signalable(self):
        """Test database create"""

        func = Mock()

        signals = Signalable()
        signals.connect('/first', func)
        signals.emit('/first', 'Python')
        signals.emit('/second', 3)

        func.assert_called_with('Python')

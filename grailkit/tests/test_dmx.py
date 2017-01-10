# -*- coding: UTF-8 -*-

import unittest
from grailkit.dmx import DMXFrame, DMXDevice


class TestDMX(unittest.TestCase):

    def test_frame(self):

        # frame instantiation with data
        frame = DMXFrame([1, 2, 3, 4, 5])

        self.assertEqual(frame[0], 1)
        self.assertEqual(frame[2], 3)
        self.assertEqual(frame[4], 5)

        # frame without data
        frame = DMXFrame()
        self.assertEqual(frame[0], 0)

    def test_frame_assignment(self):

        frame = DMXFrame()
        frame[511] = 125

        self.assertEqual(frame[511], 125)

        del frame[511]
        self.assertEqual(frame[511], 0)

        with self.assertRaises(ValueError):
            frame[123] = 'string'

        with self.assertRaises(IndexError):
            frame[532] = 3

    def test_frame_representation(self):

        frame = DMXFrame()

        self.assertEqual(bytes(frame), b'\x00' * 512)
        self.assertEqual(str(frame), str(b'\x00' * 512))
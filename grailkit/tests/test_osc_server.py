# -*- coding: UTF-8 -*-
"""
Tests for OSCServer class.

:copyright: (c) 2017-2020 by Oleksii Lytvyn (http://alexlitvin.name).
:license: MIT, see LICENSE for more details.
"""

import unittest
from threading import Timer

from grailkit import osc


class TestServer(osc.OSCServer):

    def __init__(self, *args, **kwargs):
        super(TestServer, self).__init__(*args, **kwargs)

        self.log = []

    def handle(self, address, message, date):
        self.log.append((address, message, date))


def _send_messages():

    client = osc.OSCClient('127.0.0.1', 31338)

    for value in ["This is example string", 123, True, bytes("utf-8 text", "utf-8")]:
        msg = osc.OSCMessage(address="/debug")
        msg.add(value)

        client.send(msg)

    client.close()


class TestOSCServer(unittest.TestCase):

    def setUp(self):

        self.server = TestServer('127.0.0.1', 31338)

        t = Timer(2.0, self._close_server)
        t.start()

        t2 = Timer(1.0, _send_messages)
        t2.start()

        self.server.serve_forever()

    def tearDown(self):
        pass

    def _close_server(self):

        self.server.shutdown()
        self.server.server_close()

    def test_receive(self):

        addr = self.server.log[0][0]

        self.assertEqual(addr[0], '127.0.0.1')
        self.assertEqual(len(self.server.log), 4)
        self.assertEqual(self.server.log[0][1].address, "/debug")

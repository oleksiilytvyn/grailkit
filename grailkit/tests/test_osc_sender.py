# -*- coding: UTF-8 -*-
"""
Tests for OSCClient class, socket binding and sending message.

:copyright: (c) 2017-2020 by Oleksii Lytvyn.
:license: MIT, see LICENSE for more details.
"""

import unittest

from grailkit import osc


class TestOSCSender(unittest.TestCase):

    @unittest.mock.patch('socket.socket')
    def test_send(self, mock_socket_ctor):
        mock_socket = mock_socket_ctor.return_value

        msg = osc.OSCMessage(address='/test')

        client = osc.OSCClient('::1', 31337)
        client.send(msg)

        self.assertTrue(mock_socket.sendto.called)
        mock_socket.sendto.assert_called_once_with(msg.build().dgram, ('::1', 31337))


if __name__ == "__main__":
    unittest.main()

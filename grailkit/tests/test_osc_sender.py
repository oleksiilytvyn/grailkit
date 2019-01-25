# -*- coding: UTF-8 -*-
"""
    grailkit.tests.test_osc_sender
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for OSCClient class, socket binding and sending message

    :copyright: (c) 2017-2019 by Oleksii Lytvyn.
    :license: MIT, see LICENSE for more details.
"""

import unittest
from grailkit import osc


try:
    from unittest import mock
except ImportError:
    import mock


class TestOSCSender(unittest.TestCase):

    @mock.patch('socket.socket')
    def test_send(self, mock_socket_ctor):
        mock_socket = mock_socket_ctor.return_value

        msg = osc.OSCMessage(address='/test')

        client = osc.OSCClient('::1', 31337)
        client.send(msg)

        self.assertTrue(mock_socket.sendto.called)
        mock_socket.sendto.assert_called_once_with(msg.build().dgram, ('::1', 31337))


if __name__ == "__main__":
    unittest.main()

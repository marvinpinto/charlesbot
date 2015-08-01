import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from asynctest.mock import MagicMock


class TestPrintRoomMembership(asynctest.TestCase):

    @asynctest.ignore_loop
    def test_print_room_membership_empty_dict(self):
        with patch('charlesbot.plugins.broadcast_message.BroadcastMessage.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.broadcast_message import BroadcastMessage
            mock_init.return_value = None
            slack_client = MagicMock()
            t_bm = BroadcastMessage(slack_client)
            t_bm.sc = slack_client
            t_bm.log = MagicMock()
            t_bm.room_membership = {}
            t_bm.print_room_membership()
            self.assertEqual(t_bm.log.mock_calls, [call('Currently in: ')])

    @asynctest.ignore_loop
    def test_print_room_membership_single(self):
        with patch('charlesbot.plugins.broadcast_message.BroadcastMessage.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.broadcast_message import BroadcastMessage
            mock_init.return_value = None
            slack_client = MagicMock()
            t_bm = BroadcastMessage(slack_client)
            t_bm.sc = slack_client
            t_bm.log = MagicMock()
            t_bm.room_membership = {"1234": "fun"}
            t_bm.print_room_membership()
            self.assertEqual(t_bm.log.mock_calls, [call('Currently in: fun')])

    @asynctest.ignore_loop
    def test_print_room_membership_multiple(self):
        with patch('charlesbot.plugins.broadcast_message.BroadcastMessage.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.broadcast_message import BroadcastMessage
            mock_init.return_value = None
            slack_client = MagicMock()
            t_bm = BroadcastMessage(slack_client)
            t_bm.sc = slack_client
            t_bm.log = MagicMock()
            t_bm.room_membership = {"1234": "fun", "4567": "funner"}
            t_bm.print_room_membership()
            self.assertEqual(
                t_bm.log.mock_calls,
                [call('Currently in: fun, funner')]
            )

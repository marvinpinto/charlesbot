import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from asynctest.mock import MagicMock


class TestRemoveFromRoom(asynctest.TestCase):

    def test_remove_not_in_any_rooms(self):
        with patch('charlesbot.plugins.broadcast_message.BroadcastMessage.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.broadcast_message import BroadcastMessage
            mock_init.return_value = None
            slack_client = asynctest.MagicMock()
            with patch('charlesbot.plugins.broadcast_message.filter_message_types') as mock_filter:  # NOQA
                mock_filter.return_value = True
                t_bm = BroadcastMessage(slack_client)
                t_bm.sc = slack_client
                t_bm.log = MagicMock()
                t_bm.print_room_membership = MagicMock()
                t_bm.room_membership = {}
                msg = {
                    "type": "channel_left",
                    "channel": "C024BE91L"
                }
                yield from t_bm.remove_from_room(msg)
                self.assertEqual(t_bm.log.mock_calls, [])
                self.assertEqual(t_bm.room_membership, {})

    def test_remove_bogus_room(self):
        with patch('charlesbot.plugins.broadcast_message.BroadcastMessage.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.broadcast_message import BroadcastMessage
            mock_init.return_value = None
            slack_client = asynctest.MagicMock()
            with patch('charlesbot.plugins.broadcast_message.filter_message_types') as mock_filter:  # NOQA
                mock_filter.return_value = True
                t_bm = BroadcastMessage(slack_client)
                t_bm.sc = slack_client
                t_bm.log = MagicMock()
                t_bm.print_room_membership = MagicMock()
                t_bm.room_membership = {"5678": "funner"}
                msg = {
                    "type": "channel_left",
                    "channel": "1234"
                }
                yield from t_bm.remove_from_room(msg)
                self.assertEqual(t_bm.log.mock_calls, [])
                self.assertEqual(t_bm.room_membership, {"5678": "funner"})

    def test_remove_in_one_room(self):
        with patch('charlesbot.plugins.broadcast_message.BroadcastMessage.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.broadcast_message import BroadcastMessage
            mock_init.return_value = None
            slack_client = asynctest.MagicMock()
            with patch('charlesbot.plugins.broadcast_message.filter_message_types') as mock_filter:  # NOQA
                mock_filter.return_value = True
                t_bm = BroadcastMessage(slack_client)
                t_bm.sc = slack_client
                t_bm.log = MagicMock()
                t_bm.print_room_membership = MagicMock()
                t_bm.room_membership = {"1234": "funner"}
                msg = {
                    "type": "channel_left",
                    "channel": "1234"
                }
                yield from t_bm.remove_from_room(msg)
                self.assertEqual(
                    t_bm.log.mock_calls,
                    [call('I have left funner')]
                )
                self.assertEqual(t_bm.room_membership, {})

    def test_remove_in_two_rooms(self):
        with patch('charlesbot.plugins.broadcast_message.BroadcastMessage.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.broadcast_message import BroadcastMessage
            mock_init.return_value = None
            slack_client = asynctest.MagicMock()
            with patch('charlesbot.plugins.broadcast_message.filter_message_types') as mock_filter:  # NOQA
                mock_filter.return_value = True
                t_bm = BroadcastMessage(slack_client)
                t_bm.sc = slack_client
                t_bm.log = MagicMock()
                t_bm.print_room_membership = MagicMock()
                t_bm.room_membership = {"1234": "funner", "4567": "moar_fun"}
                msg = {
                    "type": "channel_left",
                    "channel": "4567"
                }
                yield from t_bm.remove_from_room(msg)
                self.assertEqual(
                    t_bm.log.mock_calls,
                    [call('I have left moar_fun')]
                )
                self.assertEqual(t_bm.room_membership, {"1234": "funner"})

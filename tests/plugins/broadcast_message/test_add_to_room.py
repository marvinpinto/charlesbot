import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from asynctest.mock import MagicMock


class TestAddToRoom(asynctest.TestCase):

    def test_add_bogus_input(self):
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
                msg = {}
                with self.assertRaises(KeyError):
                    yield from t_bm.add_to_room(msg)

    def test_add_not_in_any_rooms(self):
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
                    "type": "group_joined",
                    "channel": {
                        "name": "fun",
                        "id": "1234"
                    }
                }
                yield from t_bm.add_to_room(msg)
                self.assertEqual(
                    t_bm.log.mock_calls,
                    [call('I was invited to join fun')]
                )
                self.assertEqual(t_bm.room_membership, {"1234": "fun"})

    def test_add_in_one_room(self):
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
                t_bm.room_membership = {"4567": "funner"}
                msg = {
                    "type": "group_joined",
                    "channel": {
                        "name": "fun",
                        "id": "1234"
                    }
                }
                yield from t_bm.add_to_room(msg)
                self.assertEqual(
                    t_bm.log.mock_calls,
                    [call('I was invited to join fun')]
                )
                self.assertEqual(
                    t_bm.room_membership,
                    {"1234": "fun", "4567": "funner"}
                )

import asynctest
from asynctest.mock import call
from asynctest.mock import MagicMock
from asynctest.mock import CoroutineMock
from charlesbot.plugins.broadcast_message import BroadcastMessage


class TestParseWallMessage(asynctest.TestCase):

    def setUp(self):
        self.slack_client = MagicMock()
        self.initialize_bm_plugin()

    def tearDown(self):
        self.initialize_bm_plugin()

    def initialize_bm_plugin(self):
        self.bm = BroadcastMessage(self.slack_client)
        self.bm.seed_initial_data = MagicMock()
        self.bm.add_to_room = CoroutineMock()
        self.bm.remove_from_room = CoroutineMock()
        self.bm.get_user_info = CoroutineMock()
        self.bm.send_broadcast_message = CoroutineMock()

    def test_invalid_input_single(self):
        msg = [{}]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.get_user_info.mock_calls, [])
        self.assertEqual(self.bm.send_broadcast_message.mock_calls, [])

    def test_invalid_input_multiple(self):
        msg = [{}, {}, {}]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.get_user_info.mock_calls, [])
        self.assertEqual(self.bm.send_broadcast_message.mock_calls, [])

    def test_channel_is_empty(self):
        msg = [
            {
                "type": "message",
                "user": "marvin",
                "channel": "",
                "text": "!wall hello everyone",
            }
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.get_user_info.mock_calls, [])
        self.assertEqual(self.bm.send_broadcast_message.mock_calls, [])

    def test_channel_is_none(self):
        msg = [
            {
                "type": "message",
                "user": "marvin",
                "text": "!wall hello everyone",
            }
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.get_user_info.mock_calls, [])
        self.assertEqual(self.bm.send_broadcast_message.mock_calls, [])

    def test_msg_is_empty(self):
        msg = [
            {
                "type": "message",
                "user": "marvin",
                "channel": "C1",
                "text": "",
            }
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.get_user_info.mock_calls, [])
        self.assertEqual(self.bm.send_broadcast_message.mock_calls, [])

    def test_msg_is_none(self):
        msg = [
            {
                "type": "message",
                "user": "marvin",
                "channel": "C1",
            }
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.get_user_info.mock_calls, [])
        self.assertEqual(self.bm.send_broadcast_message.mock_calls, [])

    def test_sent_by_is_empty(self):
        msg = [
            {
                "type": "message",
                "user": "",
                "channel": "C1",
                "text": "text",
            }
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.get_user_info.mock_calls, [])
        self.assertEqual(self.bm.send_broadcast_message.mock_calls, [])

    def test_sent_by_is_none(self):
        msg = [
            {
                "type": "message",
                "channel": "C1",
                "text": "text",
            }
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.get_user_info.mock_calls, [])
        self.assertEqual(self.bm.send_broadcast_message.mock_calls, [])

    def test_parsed_failed_single(self):
        msg = [
            {
                "type": "message",
                "user": "marvin",
                "channel": "C1",
                "text": "This is not a wall message",
            }
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.get_user_info.mock_calls, [])
        self.assertEqual(self.bm.send_broadcast_message.mock_calls, [])

    def test_parsed_failed_multiple(self):
        msg = [
            {
                "type": "message",
                "user": "marvin",
                "channel": "C1",
                "text": "This is not a wall message",
            },
            {
                "type": "message",
                "user": "marvin",
                "channel": "C1",
                "text": "And neither is this!",
            },
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.get_user_info.mock_calls, [])
        self.assertEqual(self.bm.send_broadcast_message.mock_calls, [])

    def test_ok_single(self):
        msg = [
            {
                "type": "message",
                "user": "marvin",
                "channel": "C1",
                "text": "!wall This is totes a wall message",
            }
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.get_user_info.mock_calls, [call('marvin')])
        self.assertEqual(len(self.bm.send_broadcast_message.mock_calls), 1)

    def test_ok_multiple(self):
        msg = [
            {
                "type": "message",
                "user": "marvin",
                "channel": "C1",
                "text": "!wall This is totes a wall message",
            },
            {
                "type": "message",
                "user": "marvin",
                "channel": "C1",
                "text": "!wall And so is this!",
            }
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(len(self.bm.get_user_info.mock_calls), 2)
        self.assertEqual(len(self.bm.send_broadcast_message.mock_calls), 2)

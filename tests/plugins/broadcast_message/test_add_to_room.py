import asynctest
from asynctest.mock import MagicMock
from asynctest.mock import CoroutineMock
from charlesbot.plugins.broadcast_message import BroadcastMessage


class TestAddToRoom(asynctest.TestCase):

    def setUp(self):
        self.slack_client = MagicMock()
        self.initialize_bm_plugin()

    def tearDown(self):
        self.initialize_bm_plugin()

    def initialize_bm_plugin(self):
        self.bm = BroadcastMessage(self.slack_client)
        self.bm.seed_initial_data = MagicMock()
        self.bm.remove_from_room = CoroutineMock()
        self.bm.parse_wall_message = CoroutineMock()
        self.bm.room_membership = {}

    def test_invalid_input_single(self):
        msg = [{}]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, {})

    def test_invalid_input_multiple(self):
        msg = [{}, {}, {}]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, {})

    def test_join_one_group_single(self):
        msg = [
            {
                "type": "group_joined",
                "channel": {
                    "name": "fun",
                    "id": "1234"
                }
            }
        ]
        expected = {
            "1234": "fun"
        }
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, expected)

    def test_join_multiple(self):
        msg = [
            {
                "type": "group_joined",
                "channel": {
                    "name": "fun1",
                    "id": "1"
                }
            },
            {
                "type": "group_joined",
                "channel": {
                    "name": "fun2",
                    "id": "2"
                }
            },
            {
                "type": "channel_joined",
                "channel": {
                    "name": "fun3",
                    "id": "3"
                }
            }
        ]
        expected = {
            "1": "fun1",
            "2": "fun2",
            "3": "fun3"
        }
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, expected)

    def test_join_already_in_one_group_single(self):
        self.bm.room_membership = {"1": "fun1"}
        msg = [
            {
                "type": "group_joined",
                "channel": {
                    "name": "fun2",
                    "id": "2"
                }
            }
        ]
        expected = {
            "1": "fun1",
            "2": "fun2",
        }
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, expected)

    def test_join_already_in_one_group_multiple(self):
        self.bm.room_membership = {"1": "fun1"}
        msg = [
            {
                "type": "group_joined",
                "channel": {
                    "name": "fun4",
                    "id": "4"
                }
            },
            {
                "type": "group_joined",
                "channel": {
                    "name": "fun2",
                    "id": "2"
                }
            },
            {
                "type": "channel_joined",
                "channel": {
                    "name": "fun3",
                    "id": "3"
                }
            }
        ]
        expected = {
            "4": "fun4",
            "1": "fun1",
            "3": "fun3",
            "2": "fun2",
        }
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, expected)

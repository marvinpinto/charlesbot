import asynctest
from asynctest.mock import MagicMock
from asynctest.mock import CoroutineMock
from charlesbot.plugins.broadcast_message import BroadcastMessage


class TestRemoveFromRoom(asynctest.TestCase):

    def setUp(self):
        self.slack_client = MagicMock()
        self.initialize_bm_plugin()

    def tearDown(self):
        self.initialize_bm_plugin()

    def initialize_bm_plugin(self):
        self.bm = BroadcastMessage(self.slack_client)
        self.bm.seed_initial_data = MagicMock()
        self.bm.add_to_room = CoroutineMock()
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

    def test_not_in_any_rooms_single(self):
        msg = [
            {
                "type": "channel_left",
                "channel": "C024BE91L"
            }
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, {})

    def test_not_in_any_rooms_multiple(self):
        msg = [
            {
                "type": "channel_left",
                "channel": "C1"
            },
            {
                "type": "group_left",
                "channel": "G1"
            },
            {
                "type": "channel_left",
                "channel": "C2"
            },
            {
                "type": "group_left",
                "channel": "G2"
            },
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, {})

    def test_remove_from_bogus_room(self):
        self.bm.room_membership = {"1": "fun1"}
        msg = [
            {
                "type": "channel_left",
                "channel": "2"
            }
        ]
        expected = {
            "1": "fun1",
        }
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, expected)

    @asynctest.ignore_loop
    def test_remove_from_one_room(self):
        self.bm.room_membership = {"1": "fun1"}
        msg = [
            {
                "type": "channel_left",
                "channel": "1"
            }
        ]
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, {})

    @asynctest.ignore_loop
    def test_remove_from_multiple_rooms(self):
        self.bm.room_membership = {
            "1": "fun1",
            "2": "fun2",
            "3": "fun3",
            "4": "fun4",
            "5": "fun5",
        }
        msg = [
            {
                "type": "channel_left",
                "channel": "2"
            },
            {
                "type": "group_left",
                "channel": "1"
            },
            {
                "type": "group_left",
                "channel": "4"
            },
            {
                "type": "channel_left",
                "channel": "5"
            },
        ]
        expected = {
            "3": "fun3",
        }
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, expected)

import asynctest
from asynctest.mock import patch
from charlesbot.slack.slack_group_joined import SlackGroupJoined
from charlesbot.slack.slack_channel_joined import SlackChannelJoined


class TestAddToRoom(asynctest.TestCase):

    def setUp(self):
        patcher = patch('charlesbot.plugins.broadcast_message.BroadcastMessage.seed_initial_data')  # NOQA
        self.addCleanup(patcher.stop)
        self.mock_seed_initial_data = patcher.start()
        from charlesbot.plugins.broadcast_message import BroadcastMessage
        self.bm = BroadcastMessage()
        self.bm.room_membership = {}

    def test_invalid_input_single(self):
        msg = {}
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, {})

    def test_join_one_group_single(self):
        msg = SlackGroupJoined(name="fun", id="1234")
        expected = {
            "1234": "fun"
        }
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, expected)

    def test_join_multiple(self):
        msg = SlackGroupJoined(name="fun1", id="1")
        yield from self.bm.process_message(msg)
        msg = SlackGroupJoined(name="fun2", id="2")
        yield from self.bm.process_message(msg)
        msg = SlackChannelJoined(name="fun3", id="3")
        yield from self.bm.process_message(msg)
        expected = {
            "1": "fun1",
            "2": "fun2",
            "3": "fun3"
        }
        self.assertEqual(self.bm.room_membership, expected)

    def test_join_already_in_one_group_single(self):
        self.bm.room_membership = {"1": "fun1"}
        msg = SlackGroupJoined(name="fun2", id="2")
        expected = {
            "1": "fun1",
            "2": "fun2",
        }
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, expected)

    def test_join_already_in_one_group_multiple(self):
        self.bm.room_membership = {"1": "fun1"}
        msg = SlackGroupJoined(name="fun4", id="4")
        yield from self.bm.process_message(msg)
        msg = SlackGroupJoined(name="fun2", id="2")
        yield from self.bm.process_message(msg)
        msg = SlackChannelJoined(name="fun3", id="3")
        yield from self.bm.process_message(msg)
        expected = {
            "4": "fun4",
            "1": "fun1",
            "3": "fun3",
            "2": "fun2",
        }
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, expected)

import asynctest
from asynctest.mock import patch
from charlesbot.slack.slack_message import SlackMessage


class TestParseWallMessage(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot.plugins.broadcast_message.BroadcastMessage.seed_initial_data')  # NOQA
        self.addCleanup(patcher1.stop)
        self.mock_seed_initial_data = patcher1.start()

        patcher4 = patch('charlesbot.plugins.broadcast_message.BroadcastMessage.send_broadcast_message')  # NOQA
        self.addCleanup(patcher4.stop)
        self.mock_send_broadcast_message = patcher4.start()

        patcher5 = patch('charlesbot.plugins.broadcast_message.SlackUser')
        self.addCleanup(patcher5.stop)
        self.mock_slack_user = patcher5.start()

        from charlesbot.plugins.broadcast_message import BroadcastMessage
        self.bm = BroadcastMessage()

    def test_type_is_not_slack_message(self):
        msg = ""
        yield from self.bm.process_message(msg)
        self.assertEqual(self.mock_slack_user.mock_calls, [])
        self.assertEqual(self.mock_send_broadcast_message.mock_calls, [])

    def test_prefix_is_not_wall(self):
        msg = SlackMessage(type="message",
                           channel="chan1",
                           user="marvin",
                           text="Not a wall message")
        yield from self.bm.process_message(msg)
        self.assertEqual(self.mock_slack_user.mock_calls, [])
        self.assertEqual(self.mock_send_broadcast_message.mock_calls, [])

    def test_ok_single(self):
        msg = SlackMessage(type="message",
                           channel="C1",
                           user="marvin",
                           text="!wall This is totes a wall message")
        yield from self.bm.process_message(msg)
        print(self.mock_slack_user.mock_calls)
        self.assertEqual(len(self.mock_send_broadcast_message.mock_calls), 1)

import asynctest
from asynctest.mock import MagicMock


class TestSlackConnectionStreamMessages(asynctest.TestCase):

    def setUp(self):
        from charlesbot.slack.slack_connection import SlackConnection
        self.slack = SlackConnection()
        self.slack.initialized = True
        self.slack.sc = MagicMock()

    def tearDown(self):
        self.slack._drop()

    def test_stream_none(self):
        self.slack.sc.rtm_read.return_value = []
        messages = yield from self.slack.get_stream_messages()
        self.assertEqual(messages, [])

    def test_stream_error(self):
        self.slack.sc.rtm_read.side_effect = [BrokenPipeError]
        with self.assertRaises(SystemExit):
            yield from self.slack.get_stream_messages()

    def test_stream_one_message(self):
        self.slack.sc.rtm_read.return_value = ["boo"]
        messages = yield from self.slack.get_stream_messages()
        self.assertEqual(messages, [None])

    def test_stream_two_messages(self):
        self.slack.sc.rtm_read.return_value = ["boo", "urns"]
        messages = yield from self.slack.get_stream_messages()
        self.assertEqual(messages, [None, None])

    def test_stream_channel_joined(self):
        self.slack.sc.rtm_read.return_value = [{"type": "channel_joined"}]
        messages = yield from self.slack.get_stream_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual("", messages[0].is_channel)

    def test_stream_channel_left(self):
        self.slack.sc.rtm_read.return_value = [{"type": "channel_left"}]
        messages = yield from self.slack.get_stream_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual("", messages[0].channel)

    def test_stream_group_joined(self):
        self.slack.sc.rtm_read.return_value = [{"type": "group_joined"}]
        messages = yield from self.slack.get_stream_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual("", messages[0].is_group)

    def test_stream_group_left(self):
        self.slack.sc.rtm_read.return_value = [{"type": "group_left"}]
        messages = yield from self.slack.get_stream_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual("", messages[0].channel)

    def test_stream_message(self):
        self.slack.sc.rtm_read.return_value = [{"type": "message"}]
        messages = yield from self.slack.get_stream_messages()
        self.assertEqual(len(messages), 1)
        self.assertEqual("", messages[0].subtype)

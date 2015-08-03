import asynctest
import re
from asynctest.mock import MagicMock
from asynctest.mock import call
from charlesbot.plugins.help_plugin import Help


class TestHelpPlugin(asynctest.TestCase):

    def setUp(self):
        self.slack_client = MagicMock()
        self.initialize_help_plugin()

    def tearDown(self):
        self.initialize_help_plugin()

    def initialize_help_plugin(self):
        self.hp = Help(self.slack_client)
        self.hp.send_help_message = MagicMock()

    @asynctest.ignore_loop
    def test_help_message_wrapper_str(self):
        help_str = self.hp.get_help_message()
        regex = r'^```\n.*\n```$'
        p = re.compile(regex, re.MULTILINE | re.DOTALL)
        m = p.match(help_str)
        self.assertTrue(m)

    def test_parse_help_message_channel_msg_is_none(self):
        messages = [
            {
                "type": "message",
                "user": "U2147483697",
                "text": "!help",
            }
        ]
        yield from self.hp.process_message(messages)
        self.hp.send_help_message.assert_has_calls([])

    def test_one_msg_no_good(self):
        messages = [
            {
                "type": "message",
                "user": "U2147483697",
                "channel": "C2147483705",
                "text": "This is not me asking for help",
            }
        ]
        yield from self.hp.process_message(messages)
        self.hp.send_help_message.assert_has_calls([])

    def test_one_msg_one_good(self):
        messages = [
            {
                "type": "message",
                "user": "U2147483697",
                "channel": "C2147483705",
                "text": "!help",
            }
        ]
        yield from self.hp.process_message(messages)
        expected = [call('C2147483705')]
        self.hp.send_help_message.assert_has_calls(expected)

    def test_two_msgs_no_good(self):
        messages = [
            {
                "type": "message",
                "user": "U2147483697",
                "channel": "C2147483705",
                "text": "This is not me asking for help",
            },
            {
                "type": "message",
                "user": "U2147483697",
                "channel": "C2147483705",
                "text": "This is not me asking for help, either",
            }
        ]
        yield from self.hp.process_message(messages)
        self.hp.send_help_message.assert_has_calls([])

    def test_two_msgs_one_good(self):
        messages = [
            {
                "type": "message",
                "user": "U2147483697",
                "channel": "C2147483705",
                "text": "!help fine, now I need help",
            },
            {
                "type": "message",
                "user": "U2147483697",
                "channel": "C2147483705sdfd",
                "text": "This is not me asking for help, either",
            }
        ]
        yield from self.hp.process_message(messages)
        expected = [call('C2147483705')]
        self.hp.send_help_message.assert_has_calls(expected)

    def test_two_msgs_two_good(self):
        messages = [
            {
                "type": "message",
                "user": "U2147483697",
                "channel": "C2147483705",
                "text": "!help fine, now I need help",
            },
            {
                "type": "message",
                "user": "U2147483697",
                "channel": "C2147483705sdfd",
                "text": "!help halp me, plz",
            }
        ]
        yield from self.hp.process_message(messages)
        expected = [call('C2147483705'), call('C2147483705sdfd')]
        self.hp.send_help_message.assert_has_calls(expected, any_order=True)

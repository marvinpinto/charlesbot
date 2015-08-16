import asynctest
import re
from asynctest.mock import MagicMock
from asynctest.mock import call
from charlesbot.plugins.help_plugin import Help
from charlesbot.slack.slack_message import SlackMessage


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

    def test_wrong_message_type(self):
        msg = ""
        yield from self.hp.process_message(msg)
        self.hp.send_help_message.assert_has_calls([])

    def test_two_msgs_no_good(self):
        msg = SlackMessage(type="message",
                           user="U2147483697",
                           channel="C2147483705",
                           text="This is not me asking for prefix")
        yield from self.hp.process_message(msg)
        msg = SlackMessage(type="message",
                           user="U2147483697",
                           channel="C2147483705",
                           text="This is not me asking for help, either")
        yield from self.hp.process_message(msg)
        self.hp.send_help_message.assert_has_calls([])

    def test_two_msgs_one_good(self):
        msg = SlackMessage(type="message",
                           user="U2147483697",
                           channel="C1",
                           text="!help fine, now I need help")
        yield from self.hp.process_message(msg)
        msg = SlackMessage(type="message",
                           user="U2147483697",
                           channel="C2147483705",
                           text="This is not me asking for help, either")
        yield from self.hp.process_message(msg)
        expected = [call('C1')]
        self.hp.send_help_message.assert_has_calls(expected)

    def test_two_msgs_two_good(self):
        msg = SlackMessage(type="message",
                           user="U2147483697",
                           channel="C1",
                           text="!help fine, now I need help")
        yield from self.hp.process_message(msg)
        msg = SlackMessage(type="message",
                           user="U2147483697",
                           channel="C2",
                           text="!help Yep, still need help")
        yield from self.hp.process_message(msg)
        expected = [call('C1'), call('C2')]
        self.hp.send_help_message.assert_has_calls(expected, any_order=True)

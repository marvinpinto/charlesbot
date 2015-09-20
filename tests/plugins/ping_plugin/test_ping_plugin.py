import asynctest
from asynctest.mock import MagicMock
from asynctest.mock import call
from asynctest.mock import patch
from charlesbot.slack.slack_message import SlackMessage
from charlesbot.slack.slack_pong import SlackPong


class TestPingPlugin(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot.plugins.ping_plugin.Ping.schedule_ping_frequency')  # NOQA
        self.addCleanup(patcher1.stop)
        self.mock_schedule_ping_frequency = patcher1.start()

        patcher2 = patch('charlesbot.plugins.ping_plugin.Ping.get_package_version_number')  # NOQA
        self.addCleanup(patcher2.stop)
        self.mock_get_package_version_number = patcher2.start()

        from charlesbot.plugins.ping_plugin import Ping
        self.ping = Ping()
        self.ping.send_version_message = MagicMock()

    @asynctest.ignore_loop
    def test_get_help_string(self):
        """
        Don't care about the contents of the help string, just as long as there
        is something in there.
        """
        help_str = self.ping.get_help_message()
        self.assertTrue(help_str)

    def test_process_incorrect_msg_type(self):
        yield from self.ping.process_message("invalid")
        self.assertEqual(self.ping.send_version_message.mock_calls, [])

    def test_process_irrelevant_slack_message(self):
        msg = SlackMessage(type="message",
                           user="U2147483697",
                           channel="C2147483705",
                           text="This is not the prefix you are looking for")
        yield from self.ping.process_message(msg)
        self.assertEqual(self.ping.send_version_message.mock_calls, [])

    def test_process_slack_message(self):
        msg = SlackMessage(type="message",
                           user="U2147483697",
                           channel="C2147483705",
                           text="!version")
        yield from self.ping.process_message(msg)
        expected = [call('C2147483705')]
        self.ping.send_version_message.assert_has_calls(expected)

    def test_process_pong_message(self):
        msg = SlackPong(type="pong",
                        reply_to="bob",
                        time="12:00am")
        yield from self.ping.process_message(msg)
        self.assertEqual(self.ping.send_version_message.mock_calls, [])

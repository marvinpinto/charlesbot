import asynctest
from asynctest.mock import MagicMock
from asynctest.mock import call
from asynctest.mock import patch


class TestProcessMessage(asynctest.TestCase):

    def setUp(self):
        self.slack_client = MagicMock()
        patcher = patch('charlesbot.plugins.pagerduty.pagerduty.Pagerduty.load_config')  # NOQA
        self.addCleanup(patcher.stop)
        self.mock_load_config = patcher.start()
        from charlesbot.plugins.pagerduty.pagerduty import Pagerduty
        self.pd = Pagerduty(self.slack_client)
        self.pd.handle_single_prefixed_message = MagicMock()

    def test_one_msg_no_good(self):
        messages = [
            {
                "type": "message",
                "user": "user1",
                "channel": "C1",
                "text": "Don't care who's on call",
            }
        ]
        yield from self.pd.process_message(messages)
        self.pd.handle_single_prefixed_message.assert_has_calls([])

    def test_one_msg_one_good(self):
        messages = [
            {
                "type": "message",
                "user": "user1",
                "channel": "C1",
                "text": "!oncall",
            }
        ]
        yield from self.pd.process_message(messages)
        expected = [call("C1")]
        self.pd.handle_single_prefixed_message.assert_has_calls(expected)

    def test_two_msgs_no_good(self):
        messages = [
            {
                "type": "message",
                "user": "user1",
                "channel": "C1",
                "text": "Don't care who's on call",
            },
            {
                "type": "message",
                "user": "user1",
                "channel": "C1",
                "text": "Still don't care who's on call",
            }
        ]
        yield from self.pd.process_message(messages)
        self.pd.handle_single_prefixed_message.assert_has_calls([])

    def test_two_msgs_one_good(self):
        messages = [
            {
                "type": "message",
                "user": "user1",
                "channel": "C1",
                "text": "Don't care who's on call",
            },
            {
                "type": "message",
                "user": "user2",
                "channel": "C2",
                "text": "!oncall",
            }
        ]
        yield from self.pd.process_message(messages)
        expected = [call("C2")]
        self.pd.handle_single_prefixed_message.assert_has_calls(expected)

    def test_two_msgs_two_good(self):
        messages = [
            {
                "type": "message",
                "user": "user1",
                "channel": "C1",
                "text": "!oncall",
            },
            {
                "type": "message",
                "user": "user2",
                "channel": "C2",
                "text": "!oncall",
            }
        ]
        yield from self.pd.process_message(messages)
        expected = [call("C1"), call("C2")]
        self.pd.handle_single_prefixed_message.assert_has_calls(expected,
                                                                any_order=True)

import asynctest
import asyncio
from asynctest.mock import MagicMock
from charlesbot.base_plugin import BasePlugin


class TestBasePluginParseMessage(asynctest.TestCase):

    class DummyPlugin(BasePlugin):
        def __init__(myself, slack_client):
            super().__init__(slack_client, "Dummy")
            myself.call_counter = 0

        @asyncio.coroutine
        def process_message(myself, message):
            pass

        @asyncio.coroutine
        def handle_single_prefixed_message(myself, channel_id):
            myself.call_counter += 1

    def setUp(self):
        self.slack_client = MagicMock()
        self.initialize_dummy_plugin()

    def tearDown(self):
        self.initialize_dummy_plugin()

    def initialize_dummy_plugin(self):
        self.bp = TestBasePluginParseMessage.DummyPlugin(self.slack_client)
        self.bp.set_running(False)

    def test_parse_message_channel_is_none(self):
        messages = {
            "type": "message",
            "user": "U2147483697",
            "text": "!help",
        }
        yield from self.bp.parse_single_prefixed_message(messages, "!help")
        self.assertEqual(self.bp.call_counter, 0)

    def test_parse_prefix_message_channel_is_empty(self):
        messages = {
            "type": "message",
            "user": "U2147483697",
            "text": "!prefix",
            "channel": "",
        }
        yield from self.bp.parse_single_prefixed_message(messages, "!prefix")
        self.assertEqual(self.bp.call_counter, 0)

    def test_parse_prefix_message_msg_is_none(self):
        messages = {
            "type": "message",
            "user": "U2147483697",
            "channel": "C1",
        }
        yield from self.bp.parse_single_prefixed_message(messages, "!prefix")
        self.assertEqual(self.bp.call_counter, 0)

    def test_parse_prefix_message_msg_is_empty(self):
        messages = {
            "type": "message",
            "user": "U2147483697",
            "text": "",
            "channel": "C1",
        }
        yield from self.bp.parse_single_prefixed_message(messages, "!prefix")
        self.assertEqual(self.bp.call_counter, 0)

    def test_parse_prefix_message_user_is_none(self):
        messages = {
            "type": "message",
            "channel": "C1",
            "text": "!prefix hello!",
        }
        yield from self.bp.parse_single_prefixed_message(messages, "!prefix")
        self.assertEqual(self.bp.call_counter, 0)

    def test_parse_prefix_message_user_is_empty(self):
        messages = {
            "type": "message",
            "user": "",
            "text": "!prefix hello!",
            "channel": "C1",
        }
        yield from self.bp.parse_single_prefixed_message(messages, "!prefix")
        self.assertEqual(self.bp.call_counter, 0)

    def test_one_msg_no_good(self):
        messages = {
            "type": "message",
            "user": "U2147483697",
            "channel": "C2147483705",
            "text": "This is not me asking for help",
        }
        yield from self.bp.parse_single_prefixed_message(messages, "!help")
        self.assertEqual(self.bp.call_counter, 0)

    def test_one_msg_one_good(self):
        messages = {
            "type": "message",
            "user": "U2147483697",
            "channel": "C2147483705",
            "text": "!prefix",
        }
        yield from self.bp.parse_single_prefixed_message(messages, "!prefix")
        self.assertEqual(self.bp.call_counter, 1)

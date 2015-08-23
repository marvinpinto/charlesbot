import asynctest
import asyncio
from asynctest.mock import MagicMock
from charlesbot.base_plugin import BasePlugin
from charlesbot.slack.slack_message import SlackMessage


class TestBasePlugin(asynctest.TestCase):

    class DummyPlugin(BasePlugin):
        def __init__(myself):
            super().__init__("Dummy")
            myself.call_counter = 0

        @asyncio.coroutine
        def process_message(myself, message):
            myself.call_counter += 1

    def setUp(self):
        self.dc = TestBasePlugin.DummyPlugin()
        self.dc.set_running(False)

    @asynctest.ignore_loop
    def test_get_plugin_name(self):
        self.assertEqual(self.dc.get_plugin_name(), "Dummy")
        self.dc._plugin_name = "plug2"
        self.assertEqual(self.dc.get_plugin_name(), "plug2")
        self.dc._plugin_name = ""
        self.assertEqual(self.dc.get_plugin_name(), "")
        self.dc._plugin_name = None
        self.assertEqual(self.dc.get_plugin_name(), None)

    @asynctest.ignore_loop
    def test_plugin_running(self):
        self.assertEqual(self.dc.is_running(), False)
        self.dc.set_running(True)
        self.assertEqual(self.dc.is_running(), True)

    def test_queue_message(self):
        yield from self.dc.queue_message("msg one")
        self.assertEqual(self.dc._q.qsize(), 1)
        q_val = yield from self.dc._q.get()
        self.assertEqual(q_val, "msg one")
        yield from self.dc.queue_message("msg two")
        yield from self.dc.queue_message("msg three")
        self.assertEqual(self.dc._q.qsize(), 2)
        q_val = yield from self.dc._q.get()
        self.assertEqual(q_val, "msg two")
        q_val = yield from self.dc._q.get()
        self.assertEqual(q_val, "msg three")
        self.assertTrue(self.dc._q.empty())
        self.assertEqual(self.dc._q.qsize(), 0)

    def test_queue_consume(self):
        self.assertEqual(self.dc.call_counter, 0)
        self.dc.is_running = MagicMock()
        self.dc.is_running.side_effect = [True, True, False]
        yield from self.dc.queue_message("one")
        yield from self.dc.queue_message("two")
        yield from self.dc.queue_message("three")
        yield from self.dc.consume()
        self.assertEqual(self.dc._q.qsize(), 1)
        self.assertEqual(self.dc.call_counter, 2)

    def test_bot_message_wrong_object_type(self):
        self.assertEqual(self.dc.call_counter, 0)
        self.dc.is_running = MagicMock()
        self.dc.is_running.side_effect = [True, False]
        yield from self.dc.queue_message("one")
        yield from self.dc.consume()
        self.assertEqual(self.dc._q.qsize(), 0)
        self.assertEqual(self.dc.call_counter, 1)

    def test_bot_message_wrong_subtype(self):
        self.assertEqual(self.dc.call_counter, 0)
        self.dc.is_running = MagicMock()
        self.dc.is_running.side_effect = [True, False]
        msg = SlackMessage(type="message", text="hello")
        yield from self.dc.queue_message(msg)
        yield from self.dc.consume()
        self.assertEqual(self.dc._q.qsize(), 0)
        self.assertEqual(self.dc.call_counter, 1)

    def test_bot_message(self):
        self.assertEqual(self.dc.call_counter, 0)
        self.dc.is_running = MagicMock()
        self.dc.is_running.side_effect = [True, False]
        msg = SlackMessage(type="message",
                           text="hello",
                           subtype="bot_message")
        yield from self.dc.queue_message(msg)
        yield from self.dc.consume()
        self.assertEqual(self.dc._q.qsize(), 0)
        self.assertEqual(self.dc.call_counter, 0)

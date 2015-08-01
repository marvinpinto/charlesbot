from charlesbot.util.parse import does_msg_contain_prefix
from charlesbot.util.parse import filter_message_types
import logging
import asyncio


class Help(object):

    def __init__(self, slack_client):
        self.is_running = True
        self._plugin_name = "Help!"
        self.log = logging.getLogger(__name__)
        self.sc = slack_client
        self.log.info("Initializing the Help! plugin")
        loop = asyncio.get_event_loop()
        self.q = asyncio.Queue()
        loop.create_task(self.consume())

    def get_plugin_name(self):
        return self._plugin_name

    def get_help_message(self):
        msg = [
            "!help - This help message",
            "!wall <msg> - Broadcast a message to all channels I'm a part of",
        ]
        help_msg = "\n".join(msg)
        return "```\n%s\n```" % help_msg

    @asyncio.coroutine
    def process_message(self, messages):
        for msg in messages:
            yield from self.parse_help_message(msg)

    @asyncio.coroutine
    def consume(self):
        while self.is_running:
            value = yield from self.q.get()
            loop = asyncio.get_event_loop()
            loop.create_task(self.process_message(value))

    @asyncio.coroutine
    def parse_help_message(self, msg):
        types = ['message']
        fields = ['channel', 'user', 'text']
        if not filter_message_types(msg, types, fields):
            return
        channel_id = msg['channel']
        msg_text = msg['text']
        parsed = does_msg_contain_prefix("!help", msg_text)
        if parsed:
            yield from self.send_help_message(channel_id)

    @asyncio.coroutine
    def send_help_message(self, channel_id):
        self.sc.rtm_send_message(channel_id, self.get_help_message())

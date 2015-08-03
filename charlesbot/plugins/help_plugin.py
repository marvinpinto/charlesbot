from charlesbot.util.parse import does_msg_contain_prefix
from charlesbot.util.parse import parse_channel_message
from charlesbot.base_plugin import BasePlugin
import asyncio


class Help(BasePlugin):

    def __init__(self, slack_client):
        super().__init__(slack_client, "Help!")

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
    def parse_help_message(self, msg):
        channel, msg = parse_channel_message(msg)
        if channel is None or msg is None:
            return
        parsed = does_msg_contain_prefix("!help", msg)
        if parsed:
            yield from self.send_help_message(channel)

    @asyncio.coroutine
    def send_help_message(self, channel_id):
        self.sc.rtm_send_message(channel_id, self.get_help_message())

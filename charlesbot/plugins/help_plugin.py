from charlesbot.base_plugin import BasePlugin
import asyncio


class Help(BasePlugin):

    def __init__(self, slack_client):
        super().__init__(slack_client, "Help!")

    def get_help_message(self):
        msg = [
            "!help - This help message",
            "!wall <msg> - Broadcast a message to all channels I'm a part of",
            "!oncall - Find out who's on-call right now",
        ]
        help_msg = "\n".join(msg)
        return "```\n%s\n```" % help_msg

    @asyncio.coroutine
    def process_message(self, messages):
        for msg in messages:
            yield from self.parse_single_prefixed_message(msg, "!help")

    @asyncio.coroutine
    def handle_single_prefixed_message(self, channel_id):
        self.sc.rtm_send_message(channel_id, self.get_help_message())

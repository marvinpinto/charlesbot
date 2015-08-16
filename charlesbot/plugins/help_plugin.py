from charlesbot.base_plugin import BasePlugin
from charlesbot.util.parse import does_msg_contain_prefix
from charlesbot.slack.slack_message import SlackMessage
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
    def process_message(self, message):
        if not type(message) is SlackMessage:
            return
        if does_msg_contain_prefix("!help", message.text):
            yield from self.send_help_message(message.channel)

    @asyncio.coroutine
    def send_help_message(self, channel_id):
        self.sc.rtm_send_message(channel_id, self.get_help_message())

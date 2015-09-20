from charlesbot.base_plugin import BasePlugin
from charlesbot.util.parse import does_msg_contain_prefix
from charlesbot.slack.slack_message import SlackMessage
import asyncio


class Help(BasePlugin):

    def __init__(self):
        super().__init__("Help!")
        self.initialize_help_message_list()

    def initialize_help_message_list(self):
        self.help_msg_list = []
        self.help_msg_list.append("!help - This help message")
        self.help_msg_list.sort()

    def add_help_message(self, message):
        if message:
            self.help_msg_list.append(str(message))
            self.help_msg_list.sort()

    def get_help_message(self):
        help_msg = "\n".join(self.help_msg_list)
        return "```\n%s\n```" % help_msg

    @asyncio.coroutine
    def process_message(self, message):
        if not type(message) is SlackMessage:
            return
        if does_msg_contain_prefix("!help", message.text):
            yield from self.send_help_message(message.channel)

    @asyncio.coroutine
    def send_help_message(self, channel_id):  # pragma: no cover
        yield from self.slack.send_channel_message(channel_id,
                                                   self.get_help_message())

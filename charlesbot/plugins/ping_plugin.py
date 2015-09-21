from charlesbot.base_plugin import BasePlugin
from charlesbot.util.parse import does_msg_contain_prefix
from charlesbot.slack.slack_message import SlackMessage
from charlesbot.slack.slack_pong import SlackPong
import asyncio
from aiocron import crontab
import pkg_resources


class Ping(BasePlugin):

    def __init__(self):
        super().__init__("Ping Pong")
        self.schedule_ping_frequency()
        self.get_package_version_number()

    def get_package_version_number(self):  # pragma: no cover
        self.version = pkg_resources.require("charlesbot")[0].version

    def schedule_ping_frequency(self):  # pragma: no cover
        "Send a ping message to slack every 20 seconds"
        ping = crontab('* * * * * */20', func=self.send_ping, start=False)
        ping.start()

    def get_help_message(self):
        return "!version - List the running CharlesBOT version"

    @asyncio.coroutine
    def process_message(self, message):
        if not type(message) in [SlackMessage, SlackPong]:
            return

        if type(message) is SlackMessage:
            if does_msg_contain_prefix("!version", message.text):
                yield from self.send_version_message(message.channel)

        if type(message) is SlackPong:
            self.log.debug(str(message))

    @asyncio.coroutine
    def send_version_message(self, channel_id):  # pragma: no cover
        version_str = "CharlesBOT version %s" % self.version
        yield from self.slack.send_channel_message(channel_id,
                                                   version_str)

    @asyncio.coroutine
    def send_ping(self):  # pragma: no cover
        yield from self.slack.send_ping_message()

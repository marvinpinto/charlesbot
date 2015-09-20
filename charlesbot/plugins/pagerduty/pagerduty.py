import asyncio
from datetime import datetime
from charlesbot.base_plugin import BasePlugin
from charlesbot.util.parse import does_msg_contain_prefix
from charlesbot.slack.slack_message import SlackMessage
from charlesbot.config import configuration

from charlesbot.plugins.pagerduty.pagerduty_helpers import (
    get_oncall_users,
    get_pagerduty_schedules,
    send_oncall_response
)


class Pagerduty(BasePlugin):

    def __init__(self):
        super().__init__("Pagerduty")
        self.load_config()

    def load_config(self):  # pragma: no cover
        config_dict = configuration.get()
        self.token = config_dict['pagerduty']['token']
        self.subdomain = config_dict['pagerduty']['subdomain']

    def get_help_message(self):  # pragma: no cover
        return "!oncall - Find out who's on-call right now"

    @asyncio.coroutine
    def process_message(self, message):
        if not type(message) is SlackMessage:
            return
        if does_msg_contain_prefix("!oncall", message.text):
            yield from self.send_who_is_on_call_message(message.channel)

    @asyncio.coroutine
    def send_who_is_on_call_message(self, channel_id):
        schedules = yield from get_pagerduty_schedules(self.token,
                                                       self.subdomain)
        time_period = datetime.now().isoformat()
        yield from get_oncall_users(self.token,
                                    self.subdomain,
                                    schedules,
                                    time_period,
                                    time_period)
        yield from send_oncall_response(self.slack, schedules, channel_id)

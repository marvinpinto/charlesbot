import asyncio
from datetime import datetime
from charlesbot.base_plugin import BasePlugin
from charlesbot.util.parse import does_msg_contain_prefix
from charlesbot.slack.slack_message import SlackMessage

from charlesbot.util.config import (
    get_config_file_name,
    read_config
)

from charlesbot.plugins.pagerduty.pagerduty_helpers import (
    get_oncall_users,
    get_pagerduty_schedules,
    send_oncall_response
)


class Pagerduty(BasePlugin):

    def __init__(self, slack_client):
        super().__init__(slack_client, "Pagerduty")
        self.load_config()

    def load_config(self):
        config = read_config(get_config_file_name())
        self.token = config.get('pagerduty', 'token')
        self.subdomain = config.get('pagerduty', 'subdomain')

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
        yield from send_oncall_response(self.sc, schedules, channel_id)

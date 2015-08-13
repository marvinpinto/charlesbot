import asyncio
from datetime import datetime
from charlesbot.base_plugin import BasePlugin

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
    def process_message(self, messages):
        for msg in messages:
            yield from self.parse_single_prefixed_message(msg, "!oncall")

    @asyncio.coroutine
    def handle_single_prefixed_message(self, channel_id):
        schedules = yield from get_pagerduty_schedules(self.token,
                                                       self.subdomain)
        time_period = datetime.now().isoformat()
        yield from get_oncall_users(self.token,
                                    self.subdomain,
                                    schedules,
                                    time_period,
                                    time_period)
        yield from send_oncall_response(self.sc, schedules, channel_id)

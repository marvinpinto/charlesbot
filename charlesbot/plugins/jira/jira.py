import asyncio
from charlesbot.base_plugin import BasePlugin
from charlesbot.slack.slack_message import SlackMessage

from charlesbot.util.config import (
    get_config_file_name,
    read_config
)

from charlesbot.plugins.jira.jira_helpers import (
    get_jira_issue_info,
    send_jira_issue_response,
    extract_jira_ticket_numbers
)


class Jira(BasePlugin):

    def __init__(self, slack_client):
        super().__init__(slack_client, "Jira")
        self.load_config()

    def load_config(self):
        config = read_config(get_config_file_name())
        self.base_url = config.get('jira', 'base_url')

    @asyncio.coroutine
    def process_message(self, message):
        if not type(message) is SlackMessage:
            return
        tickets = extract_jira_ticket_numbers(message.text)
        for ticket in tickets:
            yield from self.send_jira_issue_information(message.channel,
                                                        ticket)

    @asyncio.coroutine
    def send_jira_issue_information(self, channel, jira_ticket):
        jira_issue = yield from get_jira_issue_info(self.base_url, jira_ticket)
        if jira_issue:
            yield from send_jira_issue_response(self.sc,
                                                channel,
                                                self.base_url,
                                                jira_issue)

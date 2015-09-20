import asyncio
from charlesbot.base_plugin import BasePlugin
from charlesbot.slack.slack_message import SlackMessage
from charlesbot.config import configuration

from charlesbot.plugins.jira.jira_helpers import (
    get_jira_issue_info,
    send_jira_issue_response,
    extract_jira_ticket_numbers
)


class Jira(BasePlugin):

    def __init__(self):
        super().__init__("Jira")
        self.load_config()

    def load_config(self):  # pragma: no cover
        config_dict = configuration.get()
        self.base_url = config_dict['jira']['base_url']

    def get_help_message(self):  # pragma: no cover
        return ""

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
            yield from send_jira_issue_response(self.slack,
                                                channel,
                                                self.base_url,
                                                jira_issue)

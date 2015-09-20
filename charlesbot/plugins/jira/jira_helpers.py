import asyncio
import re
from charlesbot.util.http import http_get_request
from charlesbot.slack.slack_attachment import SlackAttachment
import logging
import traceback
import json
from charlesbot.plugins.jira.jira_issue import JiraIssue
log = logging.getLogger(__name__)


@asyncio.coroutine
def get_jira_issue_info(base_url, ticket_number):
    issue_url = "%s/rest/api/latest/issue/%s" % (base_url, ticket_number)
    response = yield from http_get_request(issue_url)
    if not response:
        return None
    try:
        json_response = json.loads(response)
        jira_issue = JiraIssue()
        jira_issue.load(json_response)
    except (ValueError, KeyError, TypeError):
        log.error("Error parsing json response from jira")
        log.error(traceback.format_exc())
        return None
    return jira_issue


@asyncio.coroutine
def send_jira_issue_response(slack_conn, channel, jira_base_url, jira_issue):
    title_text = "%s: %s" % (jira_issue.key, jira_issue.summary)
    title_url = "%s/browse/%s" % (jira_base_url, jira_issue.key)
    attachment = SlackAttachment(color=jira_issue.status,
                                 fallback=title_text,
                                 text=jira_issue.description,
                                 mrkdwn_in=['text'],
                                 thumb_url=jira_issue.assignee_gravatar,
                                 title=title_text,
                                 title_link=title_url)

    yield from slack_conn.api_call(
        'chat.postMessage',
        channel=channel,
        attachments=attachment,
        as_user=False,
        username="JIRA",
        icon_url="https://slack.global.ssl.fastly.net/12d4/img/services/jira_48.png"  # NOQA
    )


def extract_jira_ticket_numbers(msg):
    regex_str = "\\b([A-Z]+-\d+)\\b"
    p = re.compile(regex_str, re.MULTILINE)
    m = p.findall(msg)
    return m

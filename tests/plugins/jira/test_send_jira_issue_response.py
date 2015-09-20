import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from charlesbot.slack.slack_attachment import SlackAttachment
from charlesbot.plugins.jira.jira_issue import JiraIssue


class TestSendJiraIssueResponse(asynctest.TestCase):

    def setUp(self):
        patcher2 = patch('charlesbot.slack.slack_connection.SlackConnection.api_call')  # NOQA
        self.addCleanup(patcher2.stop)
        self.mock_api_call = patcher2.start()

        from charlesbot.plugins.jira.jira_helpers import send_jira_issue_response  # NOQA
        self.send_response = send_jira_issue_response

        from charlesbot.slack.slack_connection import SlackConnection
        self.slack_connection = SlackConnection()

    def tearDown(self):
        self.slack_connection._drop()

    def test_send_issue(self):
        issue = JiraIssue(key="JIRA-9",
                          summary="this is the problem",
                          description="detailed description here")
        expected_attachment = SlackAttachment(
            color="#A4ADAD",
            fallback="JIRA-9: this is the problem",
            text="detailed description here",
            mrkdwn_in=['text'],
            thumb_url="https://slack.global.ssl.fastly.net/12d4/img/services/jira_48.png",  # NOQA
            title="JIRA-9: this is the problem",
            title_link="https://jira.atlassian.com/browse/JIRA-9"
        )
        yield from self.send_response(self.slack_connection,
                                      "#work",
                                      "https://jira.atlassian.com",
                                      issue)
        expected_call = call(
            'chat.postMessage',
            channel="#work",
            attachments=expected_attachment,
            as_user=False,
            username="JIRA",
            icon_url="https://slack.global.ssl.fastly.net/12d4/img/services/jira_48.png"  # NOQA
        )
        self.assertEqual(self.mock_api_call.mock_calls, [expected_call])

import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from asynctest.mock import MagicMock
from charlesbot.slack.slack_attachment import SlackAttachment
from charlesbot.plugins.jira.jira_issue import JiraIssue


class TestSendJiraIssueResponse(asynctest.TestCase):

    def setUp(self):
        patcher = patch('charlesbot.plugins.jira.jira_helpers.slack_rtm_api_call')  # NOQA
        self.addCleanup(patcher.stop)
        self.mock_slack_rtm = patcher.start()
        self.mock_slack_rtm.reset_mock()
        from charlesbot.plugins.jira.jira_helpers import send_jira_issue_response  # NOQA
        self.send_response = send_jira_issue_response

    def test_send_issue(self):
        mock_slackclient = MagicMock()
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
        yield from self.send_response(mock_slackclient,
                                      "#work",
                                      "https://jira.atlassian.com",
                                      issue)
        expected_call = call(
            mock_slackclient,
            'chat.postMessage',
            channel="#work",
            attachments=expected_attachment,
            as_user=False,
            username="JIRA",
            icon_url="https://slack.global.ssl.fastly.net/12d4/img/services/jira_48.png"  # NOQA
        )
        self.assertEqual(self.mock_slack_rtm.mock_calls, [expected_call])

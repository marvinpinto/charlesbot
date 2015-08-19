import asynctest
import json
from asynctest.mock import patch
from asynctest.mock import call
from charlesbot.plugins.jira.jira_issue import JiraIssue


class TestGetJiraIssueInfo(asynctest.TestCase):

    def setUp(self):
        patcher = patch('charlesbot.plugins.jira.jira_helpers.http_get_request')  # NOQA
        self.addCleanup(patcher.stop)
        self.mock_http = patcher.start()
        self.mock_http.side_effect = []
        from charlesbot.plugins.jira.jira_helpers import get_jira_issue_info
        self.get_issue = get_jira_issue_info
        self.mock_http.reset_mock()
        self.base_url = "http://jira.atlassian.com"
        self.ticket_number = "JIRA-9"
        self.expected_http_calls = [
            call('http://jira.atlassian.com/rest/api/latest/issue/JIRA-9'),
        ]

    def test_empty_http_response(self):
        self.mock_http.side_effect = [""]
        issue = yield from self.get_issue(self.base_url, self.ticket_number)
        self.assertEqual(self.mock_http.mock_calls, self.expected_http_calls)
        self.assertEqual(issue, None)

    def test_invalid_json(self):
        self.mock_http.side_effect = ["{"]
        issue = yield from self.get_issue(self.base_url, self.ticket_number)
        self.assertEqual(self.mock_http.mock_calls, self.expected_http_calls)
        self.assertEqual(issue, None)

    def test_invalid_response(self):
        response = {
            "id": "234",
            "key": "key2",
            "fields": {
                "status": {
                    "statusCategory": {
                        "id": 3,
                    }
                }
            }
        }
        expected_issue = JiraIssue(id="234",
                                   key="key2")
        expected_issue.status = "#6AC36A"
        self.mock_http.side_effect = [json.dumps(response)]
        issue = yield from self.get_issue(self.base_url, self.ticket_number)
        self.assertEqual(self.mock_http.mock_calls, self.expected_http_calls)
        self.assertEqual(issue, expected_issue)

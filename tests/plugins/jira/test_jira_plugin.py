import asynctest
from asynctest.mock import patch
from asynctest.mock import call
from charlesbot.slack.slack_message import SlackMessage


class TestJiraPlugin(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot.plugins.jira.jira.Jira.load_config')
        self.addCleanup(patcher1.stop)
        self.mock_load_config = patcher1.start()

        patcher2 = patch('charlesbot.plugins.jira.jira.get_jira_issue_info')
        self.addCleanup(patcher2.stop)
        self.mock_get_jira_issue_info = patcher2.start()

        patcher3 = patch('charlesbot.plugins.jira.jira.send_jira_issue_response')  # NOQA
        self.addCleanup(patcher3.stop)
        self.mock_send_jira_issue_response = patcher3.start()

        from charlesbot.plugins.jira.jira import Jira
        self.jira = Jira()
        self.jira.base_url = "https://jira.atlassian.com"
        self.sm = SlackMessage()
        self.sm.channel = "#work"

    def test_one_msg_wrong_object_type(self):
        msg = ""
        yield from self.jira.process_message(msg)
        self.assertEqual(self.mock_get_jira_issue_info.mock_calls, [])
        self.assertEqual(self.mock_send_jira_issue_response.mock_calls, [])

    def test_single_ticket(self):
        self.sm.text = "JIRA-001"
        yield from self.jira.process_message(self.sm)
        expected_calls = [
            call("https://jira.atlassian.com", "JIRA-001"),
        ]
        self.assertEqual(self.mock_get_jira_issue_info.mock_calls,
                         expected_calls)

    def test_multiple_tickets(self):
        self.sm.text = "JIRA-001,JIRA-002, JIRA-003.JIRA-04 JIRA-05"
        yield from self.jira.process_message(self.sm)
        expected_calls = [
            call("https://jira.atlassian.com", "JIRA-001"),
            call("https://jira.atlassian.com", "JIRA-002"),
            call("https://jira.atlassian.com", "JIRA-003"),
            call("https://jira.atlassian.com", "JIRA-04"),
            call("https://jira.atlassian.com", "JIRA-05"),
        ]
        self.assertEqual(self.mock_get_jira_issue_info.mock_calls,
                         expected_calls)

    def test_single_ticket_sentence(self):
        self.sm.text = "Hey Bob, have a look at JENKINS-55342. It's got deets"
        yield from self.jira.process_message(self.sm)
        expected_calls = [
            call("https://jira.atlassian.com", "JENKINS-55342"),
        ]
        self.assertEqual(self.mock_get_jira_issue_info.mock_calls,
                         expected_calls)

    def test_multiple_tickets_sentence(self):
        self.sm.text = "Tickets ATL-1, ATL-2,,ATL-3\nOh, Also ATL-04 and ATL05"
        yield from self.jira.process_message(self.sm)
        expected_calls = [
            call("https://jira.atlassian.com", "ATL-1"),
            call("https://jira.atlassian.com", "ATL-2"),
            call("https://jira.atlassian.com", "ATL-3"),
            call("https://jira.atlassian.com", "ATL-04"),
        ]
        self.assertEqual(self.mock_get_jira_issue_info.mock_calls,
                         expected_calls)

    def test_lowercase_ticket(self):
        self.sm.text = "Tickets atl-1, atl-2"
        yield from self.jira.process_message(self.sm)
        expected_calls = []
        self.assertEqual(self.mock_get_jira_issue_info.mock_calls,
                         expected_calls)

    def test_invalid_ticket(self):
        self.sm.text = "Tickets atlL-1, atlJENKING-2"
        yield from self.jira.process_message(self.sm)
        expected_calls = []
        self.assertEqual(self.mock_get_jira_issue_info.mock_calls,
                         expected_calls)

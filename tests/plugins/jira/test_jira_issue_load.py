import unittest
from charlesbot.plugins.jira.jira_issue import JiraIssue


class TestJiraIssueLoad(unittest.TestCase):

    def test_load_empty_dict(self):
        ji_1 = JiraIssue(id="123", key="key")
        ji_1.load({})
        self.assertEqual(ji_1.id, "123")
        self.assertEqual(ji_1.key, "key")

    def test_load_non_present_keys(self):
        ji_1 = JiraIssue(id="123", key="key")
        ji_1.load({"boo": "urns"})
        self.assertEqual(ji_1.id, "123")
        self.assertEqual(ji_1.key, "key")

    def test_load_id_key_present(self):
        ji_1 = JiraIssue(id="123", key="key")
        ji_1.load({"id": "234", "key": "key2"})
        self.assertEqual(ji_1.id, "234")
        self.assertEqual(ji_1.key, "key2")

    def test_load_assignee_displayname(self):
        ji_1 = JiraIssue(id="123", key="key")
        ji_1.load(
            {
                "id": "234",
                "key": "key2",
                "fields": {
                    "assignee": {
                        "displayName": "marvin",
                    }
                }
            }
        )
        self.assertEqual(ji_1.id, "234")
        self.assertEqual(ji_1.key, "key2")
        self.assertEqual(ji_1.assignee_name, "marvin")

    def test_load_assignee_avatarurl(self):
        ji_1 = JiraIssue(id="123", key="key")
        ji_1.load(
            {
                "id": "234",
                "key": "key2",
                "fields": {
                    "assignee": {
                        "displayName": "marvin",
                        "avatarUrls": {
                            "48x48": "google.com",
                        }
                    }
                }
            }
        )
        self.assertEqual(ji_1.id, "234")
        self.assertEqual(ji_1.key, "key2")
        self.assertEqual(ji_1.assignee_name, "marvin")
        self.assertEqual(ji_1.assignee_gravatar, "google.com")

    def test_load_description(self):
        ji_1 = JiraIssue(id="123", key="key")
        ji_1.load(
            {
                "id": "234",
                "key": "key2",
                "fields": {
                    "description": "my description",
                }
            }
        )
        self.assertEqual(ji_1.id, "234")
        self.assertEqual(ji_1.key, "key2")
        self.assertEqual(ji_1.description, "my description")

    def test_load_summary(self):
        ji_1 = JiraIssue(id="123", key="key")
        ji_1.load(
            {
                "id": "234",
                "key": "key2",
                "fields": {
                    "description": "my description",
                    "summary": "my summary",
                }
            }
        )
        self.assertEqual(ji_1.id, "234")
        self.assertEqual(ji_1.key, "key2")
        self.assertEqual(ji_1.description, "my description")
        self.assertEqual(ji_1.summary, "my summary")

    def test_load_status_invalid(self):
        ji_1 = JiraIssue(id="123", key="key")
        ji_1.load(
            {
                "id": "234",
                "key": "key2",
                "fields": {
                    "status": {
                        "statusCategory": {
                            "id": 5,
                        }
                    }
                }
            }
        )
        self.assertEqual(ji_1.id, "234")
        self.assertEqual(ji_1.key, "key2")
        self.assertEqual(ji_1.description, "")
        self.assertEqual(ji_1.summary, "")
        self.assertEqual(ji_1.status, "#A4ADAD")

    def test_load_status_valid(self):
        ji_1 = JiraIssue(id="123", key="key")
        ji_1.load(
            {
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
        )
        self.assertEqual(ji_1.id, "234")
        self.assertEqual(ji_1.key, "key2")
        self.assertEqual(ji_1.description, "")
        self.assertEqual(ji_1.summary, "")
        self.assertEqual(ji_1.status, "#6AC36A")

    def test_load_fields_null(self):
        ji_1 = JiraIssue(id="123", key="key")
        ji_1.load(
            {
                "id": "234",
                "key": "key2",
                "fields": None,
            }
        )
        self.assertEqual(ji_1.id, "234")
        self.assertEqual(ji_1.key, "key2")
        self.assertEqual(ji_1.assignee_name, "")

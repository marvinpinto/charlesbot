import unittest
from charlesbot.plugins.jira.jira_issue import JiraIssue


class TestJiraIssue(unittest.TestCase):

    def setUp(self):
        self.ji = JiraIssue()
        self.default_gravatar = "https://slack.global.ssl.fastly.net/12d4/img/services/jira_48.png"  # NOQA

    def test_status_color_invalid_id(self):
        color = self.ji.get_status_color(5)
        self.assertEqual(color, "#A4ADAD")

    def test_status_color_valid_id_one(self):
        color = self.ji.get_status_color(2)
        self.assertEqual(color, "#19689C")

    def test_status_color_valid_id_two(self):
        color = self.ji.get_status_color(1)
        self.assertEqual(color, "#A4ADAD")

    def test_gravatar_none(self):
        gravatar = self.ji.parse_jira_base_gravatar_url(None)
        self.assertEqual(gravatar, self.default_gravatar)

    def test_gravatar_empty(self):
        gravatar = self.ji.parse_jira_base_gravatar_url("")
        self.assertEqual(gravatar, self.default_gravatar)

    def test_gravatar_valid_one(self):
        gravatar = self.ji.parse_jira_base_gravatar_url("boocom")
        self.assertEqual(gravatar, "boocom")

    def test_gravatar_valid_two(self):
        g = "https://secure.gravatar.com/avatar/6e80e9c01e8e48e374648e8dadcffa15?d=mm&s=48"  # NOQA
        r = "https://secure.gravatar.com/avatar/6e80e9c01e8e48e374648e8dadcffa15"  # NOQA
        gravatar = self.ji.parse_jira_base_gravatar_url(g)
        self.assertEqual(gravatar, r)

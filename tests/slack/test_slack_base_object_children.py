import unittest
from charlesbot.slack.slack_channel_joined import SlackChannelJoined
from charlesbot.slack.slack_channel_left import SlackChannelLeft
from charlesbot.slack.slack_group_joined import SlackGroupJoined
from charlesbot.slack.slack_group_left import SlackGroupLeft
from charlesbot.slack.slack_message import SlackMessage


class TestSlackBaseObjectChildren(unittest.TestCase):

    def test_slack_channel_joined_compatibility(self):
        sc = SlackChannelJoined()
        object_dict = {"type": "channel_joined"}
        self.assertTrue(sc.is_compatible(object_dict))

    def test_slack_channel_left_compatibility(self):
        sc = SlackChannelLeft()
        object_dict = {"type": "channel_left"}
        self.assertTrue(sc.is_compatible(object_dict))

    def test_slack_group_joined_compatibility(self):
        sc = SlackGroupJoined()
        object_dict = {"type": "group_joined"}
        self.assertTrue(sc.is_compatible(object_dict))

    def test_slack_group_left_compatibility(self):
        sc = SlackGroupLeft()
        object_dict = {"type": "group_left"}
        self.assertTrue(sc.is_compatible(object_dict))

    def test_slack_message_compatibility(self):
        sc = SlackMessage()
        object_dict = {"type": "message"}
        self.assertTrue(sc.is_compatible(object_dict))

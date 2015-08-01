import asynctest
import json
from unittest.mock import MagicMock
from charlesbot.util.slack import slack_rtm_api_call
from slackclient import SlackClient
from tests import load_fixture


class TestSlackRtmApiCall(asynctest.TestCase):

    def setUp(self):
        self.channel_list_one = load_fixture('channel_list_one.json')
        self.channel_list_two = load_fixture('channel_list_two.json')
        self.channel_list_three = load_fixture('channel_list_three.json')
        self.channel_list_four = load_fixture('channel_list_four.json')

    def test_slack_rtm_api_call_ok(self):
        channel_list = self.channel_list_one.encode('utf8')
        fake_client = SlackClient("faketoken")
        fake_client.api_call = MagicMock(return_value=channel_list)
        val = yield from slack_rtm_api_call(fake_client, "fake_endpoint")
        self.assertEqual(
            json.loads(val),
            json.loads(channel_list.decode('utf-8'))
        )

    def test_slack_rtm_api_call_not_ok(self):
        channel_list = self.channel_list_two.encode('utf8')
        fake_client = SlackClient("faketoken")
        fake_client.api_call = MagicMock(return_value=channel_list)
        val = yield from slack_rtm_api_call(fake_client, "fake_endpoint")
        self.assertEqual(json.loads(val), '[]')

    def test_slack_rtm_api_call_not_encoded_utf8(self):
        channel_list = self.channel_list_three
        fake_client = SlackClient("faketoken")
        fake_client.api_call = MagicMock(return_value=channel_list)
        with self.assertRaises(AttributeError):
            yield from slack_rtm_api_call(fake_client, "fake_endpoint")

    def test_slack_rtm_api_call_malformed_json(self):
        channel_list = self.channel_list_four.encode('utf8')
        fake_client = SlackClient("faketoken")
        fake_client.api_call = MagicMock(return_value=channel_list)
        with self.assertRaises(ValueError):
            yield from slack_rtm_api_call(fake_client, "fake_endpoint")

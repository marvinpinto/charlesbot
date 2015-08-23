import asynctest
from asynctest.mock import MagicMock
from tests import load_fixture
import json


class TestSlackConnectionApiCall(asynctest.TestCase):

    def setUp(self):
        self.channel_list_one = load_fixture('channel_list_one.json')
        self.channel_list_two = load_fixture('channel_list_two.json')
        self.channel_list_three = load_fixture('channel_list_three.json')
        self.channel_list_four = load_fixture('channel_list_four.json')

        from charlesbot.slack.slack_connection import SlackConnection
        self.slack = SlackConnection()
        self.slack.initialized = True
        self.slack.sc = MagicMock()

    def tearDown(self):
        self.slack._drop()

    def test_slack_rtm_api_call_ok(self):
        channel_list = self.channel_list_one.encode('utf8')
        self.slack.sc.api_call.return_value = channel_list
        val = yield from self.slack.api_call("fake_endpoint")
        self.assertEqual(
            json.loads(val),
            json.loads(channel_list.decode('utf-8'))
        )

    def test_slack_rtm_api_call_not_ok(self):
        channel_list = self.channel_list_two.encode('utf8')
        self.slack.sc.api_call.return_value = channel_list
        val = yield from self.slack.api_call("fake_endpoint")
        self.assertEqual(json.loads(val), '{}')

    def test_slack_rtm_api_call_not_encoded_utf8(self):
        channel_list = self.channel_list_three
        self.slack.sc.api_call.return_value = channel_list
        with self.assertRaises(AttributeError):
            yield from self.slack.api_call("fake_endpoint")

    def test_slack_rtm_api_call_malformed_json(self):
        channel_list = self.channel_list_four.encode('utf8')
        self.slack.sc.api_call.return_value = channel_list
        with self.assertRaises(ValueError):
            yield from self.slack.api_call("fake_endpoint")

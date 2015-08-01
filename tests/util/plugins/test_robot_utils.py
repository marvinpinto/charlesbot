import unittest
from unittest.mock import patch
from slackclient import SlackClient
from charlesbot.util.plugins import initialize_plugins


class TestRobotUtils(unittest.TestCase):

    def mock_get_plugin_class(input_string, slack_client):
        return input_string

    @patch(
        'charlesbot.util.plugins.get_plugin_class',
        side_effect=mock_get_plugin_class
    )
    def test_initialize_plugins_single(self, mock1):
        input_list = "oneplugin"
        expected_output = ["oneplugin"]
        fake_client = SlackClient("faketoken")
        self.assertCountEqual(
            initialize_plugins(fake_client, input_list),
            expected_output
        )

    @patch(
        'charlesbot.util.plugins.get_plugin_class',
        side_effect=mock_get_plugin_class
    )
    def test_initialize_plugins_multiple(self, mock1):
        input_list = "one,two"
        expected_output = ['one', 'two']
        fake_client = SlackClient("faketoken")
        self.assertCountEqual(
            initialize_plugins(fake_client, input_list),
            expected_output
        )

    @patch(
        'charlesbot.util.plugins.get_plugin_class',
        side_effect=mock_get_plugin_class
    )
    def test_initialize_plugins_empty(self, mock1):
        input_list = ""
        expected_output = []
        fake_client = SlackClient("faketoken")
        self.assertEqual(
            initialize_plugins(fake_client, input_list),
            expected_output
        )

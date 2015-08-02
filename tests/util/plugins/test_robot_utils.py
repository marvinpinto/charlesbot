import unittest
from unittest.mock import patch
from slackclient import SlackClient


class TestRobotUtils(unittest.TestCase):

    def mock_get_plugin_class(self, input_string, slack_client):
        return input_string

    def test_initialize_plugins_single(self):
        with patch('charlesbot.util.plugins.get_plugin_class') as mock1:
            from charlesbot.util.plugins import initialize_plugins
            mock1.side_effect = self.mock_get_plugin_class
            input_list = "oneplugin"
            expected_output = ["oneplugin"]
            fake_client = SlackClient("faketoken")
            self.assertCountEqual(
                initialize_plugins(fake_client, input_list),
                expected_output
            )

    def test_initialize_plugins_multiple(self):
        with patch('charlesbot.util.plugins.get_plugin_class') as mock1:
            from charlesbot.util.plugins import initialize_plugins
            mock1.side_effect = self.mock_get_plugin_class
            input_list = "one,two"
            expected_output = ['one', 'two']
            fake_client = SlackClient("faketoken")
            self.assertCountEqual(
                initialize_plugins(fake_client, input_list),
                expected_output
            )

    def test_initialize_plugins_empty(self):
        with patch('charlesbot.util.plugins.get_plugin_class') as mock1:
            from charlesbot.util.plugins import initialize_plugins
            mock1.side_effect = self.mock_get_plugin_class
            input_list = ""
            expected_output = []
            fake_client = SlackClient("faketoken")
            self.assertEqual(
                initialize_plugins(fake_client, input_list),
                expected_output
            )

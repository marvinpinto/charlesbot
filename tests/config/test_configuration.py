import unittest
import io
import yaml
import os
from unittest.mock import mock_open
from unittest.mock import patch
from unittest.mock import call


class TestConfiguration(unittest.TestCase):

    def test_read_config_dict_valid(self):
        m = mock_open()
        yaml_file = """
        main:
          slackbot_token: 'token123'
          enabled_plugins:
            - none
        """
        with patch('charlesbot.config.configuration.open',
                   m,
                   create=True):
            m.return_value = io.StringIO(yaml_file)
            from charlesbot.config import configuration
            result = configuration.read_config_dict("fake filename")
            m.assert_has_calls([call("fake filename", "r")])
            self.assertTrue(result['main']['slackbot_token'], 'token123')
            self.assertTrue(result['main']['enabled_plugins'], ['none'])

    def test_read_config_dict_invalid(self):
        m = mock_open()
        yaml_file = "{:"
        with patch('charlesbot.config.configuration.open',
                   m,
                   create=True):
            m.return_value = io.StringIO(yaml_file)
            from charlesbot.config import configuration
            with self.assertRaises(yaml.parser.ParserError):
                configuration.read_config_dict("fake filename")
            m.assert_has_calls([call("fake filename", "r")])

    @patch.dict('os.environ', {'CHARLESBOT_SETTINGS_FILE': 'filename'})
    def test_config_file_name(self):
        from charlesbot.config import configuration
        self.assertEqual(configuration.get_config_file_name(), 'filename')

    @patch.dict('os.environ', {'CHARLESBOT_SETTINGS_FILE': ''})
    def test_config_file_name_empty(self):
        from charlesbot.config import configuration
        self.assertEqual(configuration.get_config_file_name(),
                         './development.yaml')

    @patch.dict('os.environ', {'CHARLESBOT_SETTINGS_FILE': 'filename'})
    def test_config_file_name_not_present(self):
        from charlesbot.config import configuration
        del os.environ['CHARLESBOT_SETTINGS_FILE']
        self.assertEqual(configuration.get_config_file_name(),
                         './development.yaml')

    def test_get(self):
        with patch('charlesbot.config.configuration.read_config_dict') as mock_read_dict:  # NOQA
            from charlesbot.config import configuration
            mock_read_dict.return_value = {"test": "one"}
            result = configuration.get()
            self.assertEqual(result, {"test": "one"})

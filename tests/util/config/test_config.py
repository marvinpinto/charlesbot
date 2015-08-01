import unittest
import os
from unittest.mock import patch
from charlesbot.util.config import get_config_file_name


class TestConfig(unittest.TestCase):

    @patch.dict('os.environ', {'CHARLESBOT_SETTINGS_FILE': 'filename'})
    def test_config_file_name(self):
        self.assertEqual(get_config_file_name(), 'filename')

    @patch.dict('os.environ', {'CHARLESBOT_SETTINGS_FILE': ''})
    def test_config_file_name_empty(self):
        self.assertEqual(get_config_file_name(), './development.ini')

    @patch.dict('os.environ', {'CHARLESBOT_SETTINGS_FILE': 'filename'})
    def test_config_file_name_not_present(self):
        del os.environ['CHARLESBOT_SETTINGS_FILE']
        self.assertEqual(get_config_file_name(), './development.ini')

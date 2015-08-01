import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import re


class TestGetHelpMessage(unittest.TestCase):

    def test_help_message_wrapper_str(self):
        with patch('charlesbot.plugins.help_plugin.Help.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.help_plugin import Help
            mock_init.return_value = None
            slack_client = MagicMock()
            t_hlp = Help(slack_client)
            t_hlp.sc = slack_client
            help_str = t_hlp.get_help_message()
            regex = r'^```\n.*\n```$'
            p = re.compile(regex, re.MULTILINE | re.DOTALL)
            m = p.match(help_str)
            self.assertTrue(m)

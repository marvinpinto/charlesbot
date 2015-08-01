import asynctest
from asynctest.mock import patch
from asynctest.mock import MagicMock


class TestMisc(asynctest.TestCase):

    @asynctest.ignore_loop
    def test_get_plugin_name(self):
        with patch('charlesbot.plugins.help_plugin.Help.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.help_plugin import Help
            mock_init.return_value = None
            slack_client = MagicMock()
            t_bm = Help(slack_client)
            t_bm.sc = slack_client
            t_bm._plugin_name = "fancy plugin"
            self.assertEqual(t_bm.get_plugin_name(), "fancy plugin")

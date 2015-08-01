import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from asynctest.mock import MagicMock


class TestMisc(asynctest.TestCase):

    @asynctest.ignore_loop
    def test_get_plugin_name(self):
        with patch('charlesbot.plugins.broadcast_message.BroadcastMessage.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.broadcast_message import BroadcastMessage
            mock_init.return_value = None
            slack_client = MagicMock()
            t_bm = BroadcastMessage(slack_client)
            t_bm.sc = slack_client
            t_bm._plugin_name = "fancy plugin"
            self.assertEqual(t_bm.get_plugin_name(), "fancy plugin")

    def test_seed_robot_info(self):
        with patch('charlesbot.plugins.broadcast_message.BroadcastMessage.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.broadcast_message import BroadcastMessage
            mock_init.return_value = None
            slack_client = MagicMock()
            with patch('charlesbot.plugins.broadcast_message.slack_rtm_api_call') as mock_slack:  # NOQA
                with patch('charlesbot.plugins.broadcast_message.get_robot_info') as mock_robot:  # NOQA
                    mock_robot.return_value = {"U1234": "robotname"}
                    t_bm = BroadcastMessage(slack_client)
                    t_bm.sc = slack_client
                    t_bm.log = MagicMock()
                    yield from t_bm.seed_robot_info()
                    self.assertEqual(
                        t_bm.log.mock_calls,
                        [call('Robot username: robotname')]
                    )

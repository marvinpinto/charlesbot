import asynctest
from unittest.mock import call
from unittest.mock import patch
from unittest.mock import MagicMock
from charlesbot.robot import Robot


class TestRobot(asynctest.TestCase):

    @asynctest.ignore_loop
    @patch.object(Robot, 'connect')
    @patch.object(Robot, '__init__')
    def test_slack_connect_exit(self, mock_init, mock_connect):
        mock_connect.return_value = False
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        with self.assertRaises(SystemExit):
            test_robot.start()

    @asynctest.ignore_loop
    @patch.object(Robot, '__init__')
    def test_exit_cleanly_stop_was_called(self, mock_init):
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        test_robot.plugin_list = []
        test_robot.exit_cleanly()
        self.assertEqual(test_robot.is_running, False)

    @patch.object(Robot, '__init__')
    def test_queue_message_empty_msg_1(self, mock_init):
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        plugin = MagicMock()
        msg = ""
        yield from test_robot.queue_message(msg, plugin)
        self.assertEqual(plugin.method_calls, [])

    @patch.object(Robot, '__init__')
    def test_queue_message_empty_msg_2(self, mock_init):
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        plugin = MagicMock()
        msg = []
        yield from test_robot.queue_message(msg, plugin)
        self.assertEqual(plugin.method_calls, [])

    @patch.object(Robot, '__init__')
    def test_queue_message_actual_msg_1(self, mock_init):
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        plugin = MagicMock()
        msg = "HelloPlugin"
        yield from test_robot.queue_message(msg, plugin)
        expected = [call.q.put('HelloPlugin')]
        self.assertEqual(plugin.method_calls, expected)

    @patch.object(Robot, '__init__')
    def test_queue_message_actual_msg_2(self, mock_init):
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        plugin = MagicMock()
        msg = ["HelloPlugin"]
        yield from test_robot.queue_message(msg, plugin)
        expected = [call.q.put(['HelloPlugin'])]
        self.assertEqual(plugin.method_calls, expected)

    @patch.object(Robot, '__init__')
    def test_route_message_to_plugin_empty_list(self, mock_init):
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        test_robot.sc = MagicMock()
        test_robot.queue_message = MagicMock()
        test_robot.plugin_list = []
        yield from test_robot.route_message_to_plugin()
        self.assertEqual(test_robot.sc.rtm_read.call_count, 1)
        self.assertEqual(test_robot.queue_message.call_count, 0)
        self.assertEqual(test_robot.log.error.call_count, 0)
        self.assertEqual(test_robot.log.debug.call_count, 0)

    @patch.object(Robot, '__init__')
    def test_route_message_to_plugin_list_one(self, mock_init):
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        test_robot.sc = MagicMock()
        test_robot.queue_message = MagicMock()
        test_robot.plugin_list = ["plug1"]
        yield from test_robot.route_message_to_plugin()
        self.assertEqual(test_robot.sc.rtm_read.call_count, 1)
        self.assertEqual(test_robot.queue_message.call_count, 1)
        self.assertEqual(test_robot.log.error.call_count, 0)
        self.assertEqual(test_robot.log.debug.call_count, 0)

    @patch.object(Robot, '__init__')
    def test_route_message_to_plugin_list_multiple(self, mock_init):
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        test_robot.sc = MagicMock()
        test_robot.queue_message = MagicMock()
        test_robot.plugin_list = ["plug1", "plug2"]
        yield from test_robot.route_message_to_plugin()
        self.assertEqual(test_robot.sc.rtm_read.call_count, 1)
        self.assertEqual(test_robot.queue_message.call_count, 2)
        self.assertEqual(test_robot.log.error.call_count, 0)
        self.assertEqual(test_robot.log.debug.call_count, 0)

    @patch.object(Robot, '__init__')
    def test_route_message_to_plugin_list_one_exception(self, mock_init):
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        test_robot.sc = MagicMock()
        test_robot.queue_message = MagicMock()
        test_robot.plugin_list = ["plug1"]
        test_robot.sc.rtm_read.side_effect = [BrokenPipeError]
        yield from test_robot.route_message_to_plugin()
        self.assertEqual(test_robot.sc.rtm_read.call_count, 1)
        self.assertEqual(test_robot.queue_message.call_count, 0)
        self.assertEqual(test_robot.log.error.call_count, 1)
        self.assertEqual(test_robot.log.debug.call_count, 1)

    @patch.object(Robot, '__init__')
    def test_route_message_to_plugin_list_mult_exception_1(self, mock_init):
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        test_robot.sc = MagicMock()
        test_robot.queue_message = MagicMock()
        test_robot.plugin_list = ["plug1", "plug2"]
        test_robot.sc.rtm_read.side_effect = [BrokenPipeError]
        yield from test_robot.route_message_to_plugin()
        self.assertEqual(test_robot.sc.rtm_read.call_count, 1)
        self.assertEqual(test_robot.queue_message.call_count, 0)
        self.assertEqual(test_robot.log.error.call_count, 1)
        self.assertEqual(test_robot.log.debug.call_count, 1)

    @patch.object(Robot, '__init__')
    def test_route_message_to_plugin_list_mult_exception_2(self, mock_init):
        mock_init.return_value = None
        test_robot = Robot()
        test_robot.log = MagicMock()
        test_robot.sc = MagicMock()
        test_robot.queue_message = MagicMock()
        test_robot.plugin_list = ["plug1", "plug2", "plug3"]
        test_robot.sc.rtm_read.side_effect = [BrokenPipeError]
        yield from test_robot.route_message_to_plugin()
        self.assertEqual(test_robot.sc.rtm_read.call_count, 1)
        self.assertEqual(test_robot.queue_message.call_count, 0)
        self.assertEqual(test_robot.log.error.call_count, 1)
        self.assertEqual(test_robot.log.debug.call_count, 1)

import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from asynctest.mock import MagicMock


class TestRobot(asynctest.TestCase):

    @asynctest.ignore_loop
    def test_slack_connect_exit(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            with patch('charlesbot.robot.Robot.connect') as mock_connect:
                from charlesbot.robot import Robot
                mock_connect.return_value = False
                mock_init.return_value = None
                test_robot = Robot()
                test_robot.log = MagicMock()
                with self.assertRaises(SystemExit):
                    test_robot.start()

    @asynctest.ignore_loop
    def test_exit_cleanly_stop_was_called(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            from charlesbot.robot import Robot
            mock_init.return_value = None
            test_robot = Robot()
            test_robot.log = MagicMock()
            test_robot.plugin_list = []
            test_robot.exit_cleanly()
            self.assertEqual(test_robot.is_running, False)

    def test_queue_message_empty_msg_1(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            from charlesbot.robot import Robot
            mock_init.return_value = None
            test_robot = Robot()
            test_robot.log = MagicMock()
            plugin = MagicMock()
            msg = ""
            yield from test_robot.queue_message(msg, plugin)
            self.assertEqual(plugin.method_calls, [])

    def test_queue_message_empty_msg_2(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            from charlesbot.robot import Robot
            mock_init.return_value = None
            test_robot = Robot()
            test_robot.log = MagicMock()
            plugin = MagicMock()
            msg = []
            yield from test_robot.queue_message(msg, plugin)
            self.assertEqual(plugin.method_calls, [])

    def test_queue_message_actual_msg_1(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            from charlesbot.robot import Robot
            mock_init.return_value = None
            test_robot = Robot()
            test_robot.log = MagicMock()
            plugin = MagicMock()
            msg = "HelloPlugin"
            yield from test_robot.queue_message(msg, plugin)
            expected = [call.queue_message('HelloPlugin')]
            self.assertEqual(plugin.method_calls, expected)

    def test_queue_message_actual_msg_2(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            from charlesbot.robot import Robot
            mock_init.return_value = None
            test_robot = Robot()
            test_robot.log = MagicMock()
            plugin = MagicMock()
            msg = ["HelloPlugin"]
            yield from test_robot.queue_message(msg, plugin)
            expected = [call.queue_message(['HelloPlugin'])]
            self.assertEqual(plugin.method_calls, expected)

    def test_route_message_to_plugin_empty_list(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            from charlesbot.robot import Robot
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

    def test_route_message_to_plugin_list_one(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            from charlesbot.robot import Robot
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

    def test_route_message_to_plugin_list_multiple(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            from charlesbot.robot import Robot
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

    def test_route_message_to_plugin_list_one_exception(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            from charlesbot.robot import Robot
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

    def test_route_message_to_plugin_list_mult_exception_1(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            from charlesbot.robot import Robot
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

    def test_route_message_to_plugin_list_mult_exception_2(self):
        with patch('charlesbot.robot.Robot.__init__') as mock_init:
            from charlesbot.robot import Robot
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

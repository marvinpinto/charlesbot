import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from asynctest.mock import MagicMock


class TestRobot(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot.robot.Robot.initialize_robot')
        self.addCleanup(patcher1.stop)
        self.mock_initialize_robot = patcher1.start()

        from charlesbot.robot import Robot
        self.robot = Robot()

    @asynctest.ignore_loop
    def test_exit_cleanly_no_plugins(self):
        self.robot.plugin_list = []
        self.robot.exit_cleanly()
        self.assertEqual(self.robot.is_running(), False)

    @asynctest.ignore_loop
    def test_exit_cleanly_multiple_plugins(self):
        plugin1 = MagicMock()
        plugin2 = MagicMock()
        self.robot.plugin_list = [plugin1, plugin2]
        self.robot.exit_cleanly()
        self.assertEqual(self.robot.is_running(), False)
        self.assertFalse(plugin1.is_running)
        self.assertFalse(plugin2.is_running)

    def test_queue_message_empty_msg_1(self):
        plugin1 = MagicMock()
        msg = ""
        yield from self.robot.queue_message(msg, plugin1)
        self.assertEqual(plugin1.method_calls, [])

    def test_queue_message_empty_msg_2(self):
        plugin1 = MagicMock()
        msg = []
        yield from self.robot.queue_message(msg, plugin1)
        self.assertEqual(plugin1.method_calls, [])

    def test_queue_message_actual_msg_1(self):
        plugin1 = MagicMock()
        msg = "HelloPlugin"
        yield from self.robot.queue_message(msg, plugin1)
        expected = call.queue_message('HelloPlugin')
        self.assertEqual(plugin1.method_calls, [expected])

    def test_queue_message_actual_msg_2(self):
        plugin1 = MagicMock()
        msg = ["HelloPlugin"]
        yield from self.robot.queue_message(msg, plugin1)
        expected = call.queue_message(['HelloPlugin'])
        self.assertEqual(plugin1.method_calls, [expected])

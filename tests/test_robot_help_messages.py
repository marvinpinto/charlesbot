import asynctest
from asynctest.mock import patch
from asynctest.mock import MagicMock


class TestRobotHelpMessages(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot.robot.Robot.initialize_robot')
        self.addCleanup(patcher1.stop)
        self.mock_initialize_robot = patcher1.start()

        from charlesbot.robot import Robot
        self.robot = Robot()

    @asynctest.ignore_loop
    def test_empty_plugin_list(self):
        self.robot.plugin_list = []
        self.robot.initialize_static_plugins()
        self.assertEqual(len(self.robot.plugin_list), 2)

    @asynctest.ignore_loop
    def test_plugin_list_one_entry(self):
        plugin1 = MagicMock()
        self.robot.plugin_list = [plugin1]
        self.robot.initialize_static_plugins()
        self.assertEqual(len(self.robot.plugin_list), 3)

    @asynctest.ignore_loop
    def test_plugin_list_two_entries(self):
        plugin1 = MagicMock()
        plugin2 = MagicMock()
        self.robot.plugin_list = [plugin1, plugin2]
        self.robot.initialize_static_plugins()
        self.assertEqual(len(self.robot.plugin_list), 4)

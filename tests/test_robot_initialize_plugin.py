import unittest
from unittest.mock import patch


class TestRobotInitializePlugin(unittest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot.robot.Robot.initialize_robot')
        self.addCleanup(patcher1.stop)
        self.mock_initialize_robot = patcher1.start()

        from charlesbot.robot import Robot
        self.robot = Robot()

    def test_empty_enabled_plugins_list(self):
        self.robot.enabled_plugins = []
        enabled_list = self.robot.initialize_plugins()
        self.assertEqual(enabled_list, [])

    def test_dummy_class_loader(self):
        self.robot.enabled_plugins = ['charlesbot.robot.Robot']
        enabled_list = self.robot.initialize_plugins()
        self.assertEqual(len(enabled_list), 1)

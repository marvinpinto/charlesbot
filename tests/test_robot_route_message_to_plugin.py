import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from asynctest.mock import MagicMock
from asynctest.mock import CoroutineMock


class TestRobotRouteMessageToPlugin(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot.robot.Robot.initialize_robot')
        self.addCleanup(patcher1.stop)
        self.mock_initialize_robot = patcher1.start()

        patcher2 = patch('charlesbot.robot.Robot.is_running')
        self.addCleanup(patcher2.stop)
        self.mock_is_running = patcher2.start()

        self.mock_slack = MagicMock()
        self.mock_slack.get_stream_messages = CoroutineMock()

        patcher3 = patch('charlesbot.robot.Robot.queue_message')
        self.addCleanup(patcher3.stop)
        self.mock_queue_message = patcher3.start()

        from charlesbot.robot import Robot
        self.robot = Robot()
        self.robot.slack = self.mock_slack
        self.mock_is_running.side_effect = [True, False]  # single iteration

    def test_no_msgs_returned_from_stream(self):
        self.mock_slack.get_stream_messages.return_value = []
        yield from self.robot.produce()
        self.assertEqual(self.mock_queue_message.mock_calls, [])

    def test_multiple_produce_iterations(self):
        self.mock_is_running.side_effect = [True, True, False]
        self.mock_slack.get_stream_messages.return_value = []
        yield from self.robot.produce()
        self.assertEqual(self.mock_queue_message.mock_calls, [])

    def test_single_msg_empty_plugin_list(self):
        self.mock_slack.get_stream_messages.return_value = ['msg1']
        self.robot.plugin_list = []
        yield from self.robot.produce()
        self.assertEqual(self.mock_queue_message.mock_calls, [])

    def test_single_msg_one_plugin(self):
        self.mock_slack.get_stream_messages.return_value = ['msg1']
        self.robot.plugin_list = ['plug1']
        yield from self.robot.produce()
        expected_call_1 = call('msg1', 'plug1')
        self.assertTrue(len(self.mock_queue_message.mock_calls), 1)
        self.assertTrue(expected_call_1 in self.mock_queue_message.mock_calls)

    def test_single_msg_multiple_plugins(self):
        self.mock_slack.get_stream_messages.return_value = ['msg1']
        self.robot.plugin_list = ['plug1', 'plug2']
        yield from self.robot.produce()
        expected_call_1 = call('msg1', 'plug1')
        expected_call_2 = call('msg1', 'plug2')
        self.assertTrue(len(self.mock_queue_message.mock_calls), 2)
        self.assertTrue(expected_call_1 in self.mock_queue_message.mock_calls)
        self.assertTrue(expected_call_2 in self.mock_queue_message.mock_calls)

    def test_multiple_msgs_empty_plugin_list(self):
        self.mock_slack.get_stream_messages.return_value = ['msg1', 'msg2']
        self.robot.plugin_list = []
        yield from self.robot.produce()
        self.assertEqual(self.mock_queue_message.mock_calls, [])

    def test_multiple_msgs_one_plugin(self):
        self.mock_slack.get_stream_messages.return_value = ['msg1', 'msg2']
        self.robot.plugin_list = ['plug1']
        yield from self.robot.produce()
        expected_call_1 = call('msg1', 'plug1')
        expected_call_2 = call('msg2', 'plug1')
        self.assertTrue(len(self.mock_queue_message.mock_calls), 2)
        self.assertTrue(expected_call_1 in self.mock_queue_message.mock_calls)
        self.assertTrue(expected_call_2 in self.mock_queue_message.mock_calls)

    def test_multiple_msgs_multiple_plugins(self):
        self.mock_slack.get_stream_messages.return_value = ['msg1', 'msg2']
        self.robot.plugin_list = ['plug1', 'plug2']
        yield from self.robot.produce()
        expected_call_1 = call('msg1', 'plug1')
        expected_call_2 = call('msg2', 'plug1')
        expected_call_3 = call('msg1', 'plug2')
        expected_call_4 = call('msg2', 'plug2')
        self.assertTrue(len(self.mock_queue_message.mock_calls), 4)
        self.assertTrue(expected_call_1 in self.mock_queue_message.mock_calls)
        self.assertTrue(expected_call_2 in self.mock_queue_message.mock_calls)
        self.assertTrue(expected_call_3 in self.mock_queue_message.mock_calls)
        self.assertTrue(expected_call_4 in self.mock_queue_message.mock_calls)

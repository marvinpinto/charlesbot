import asynctest
from asynctest.mock import CoroutineMock
from asynctest.mock import patch
from asynctest.mock import call
from charlesbot.slack.slack_message import SlackMessage


class TestPagerdutyPlugin(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot.plugins.pagerduty.pagerduty.get_pagerduty_schedules')  # NOQA
        self.addCleanup(patcher1.stop)
        self.mock_get_pagerduty_schedules = patcher1.start()

        patcher2 = patch('charlesbot.plugins.pagerduty.pagerduty.get_oncall_users')  # NOQA
        self.addCleanup(patcher2.stop)
        self.mock_get_oncall_users = patcher2.start()

        patcher3 = patch('charlesbot.plugins.pagerduty.pagerduty.send_oncall_response')  # NOQA
        self.addCleanup(patcher3.stop)
        self.mock_send_oncall_response = patcher3.start()

        patcher4 = patch('charlesbot.plugins.pagerduty.pagerduty.Pagerduty.load_config')  # NOQA
        self.addCleanup(patcher4.stop)
        self.mock_load_config = patcher4.start()

        from charlesbot.plugins.pagerduty.pagerduty import Pagerduty
        self.pd = Pagerduty()
        self.pd.token = "sekrittoken"
        self.pd.subdomain = "acmedomain"
        self.mock_schedule = CoroutineMock()

    def test_one_msg_wrong_object_type(self):
        msg = ""
        yield from self.pd.process_message(msg)
        self.assertEqual(self.mock_get_pagerduty_schedules.mock_calls, [])
        self.assertEqual(self.mock_get_oncall_users.mock_calls, [])
        self.assertEqual(self.mock_send_oncall_response.mock_calls, [])

    def test_one_msg_no_good(self):
        msg = SlackMessage(type="message",
                           user="PDUSER1",
                           channel="C1",
                           text="Don't want it")
        yield from self.pd.process_message(msg)
        self.assertEqual(self.mock_get_pagerduty_schedules.mock_calls, [])
        self.assertEqual(self.mock_get_oncall_users.mock_calls, [])
        self.assertEqual(self.mock_send_oncall_response.mock_calls, [])

    def test_one_msg_one_good(self):
        msg = SlackMessage(type="message",
                           user="PDUSER1",
                           channel="C1",
                           text="!oncall")
        yield from self.pd.process_message(msg)
        self.mock_get_pagerduty_schedules.return_value = [self.mock_schedule]
        expected = call("sekrittoken", "acmedomain")
        self.assertEqual(self.mock_get_pagerduty_schedules.mock_calls,
                         [expected])
        self.assertEqual(len(self.mock_get_oncall_users.mock_calls), 1)
        self.assertEqual(len(self.mock_send_oncall_response.mock_calls), 1)

    def test_two_msgs_no_good(self):
        msg = SlackMessage(type="message",
                           user="PDUSER1",
                           channel="C1",
                           text="Don't need no oncall schedule")
        yield from self.pd.process_message(msg)
        msg = SlackMessage(type="message",
                           user="PDUSER1",
                           channel="C1",
                           text="Nope, don't want it")
        yield from self.pd.process_message(msg)
        self.assertEqual(len(self.mock_get_pagerduty_schedules.mock_calls), 0)
        self.assertEqual(len(self.mock_get_oncall_users.mock_calls), 0)
        self.assertEqual(len(self.mock_send_oncall_response.mock_calls), 0)

    def test_two_msgs_one_good(self):
        msg = SlackMessage(type="message",
                           user="PDUSER1",
                           channel="C1",
                           text="!oncall")
        yield from self.pd.process_message(msg)
        msg = SlackMessage(type="message",
                           user="PDUSER1",
                           channel="C1",
                           text="Nope, don't want it")
        yield from self.pd.process_message(msg)
        self.mock_get_pagerduty_schedules.return_value = [self.mock_schedule]
        expected = call("sekrittoken", "acmedomain")
        self.assertEqual(self.mock_get_pagerduty_schedules.mock_calls,
                         [expected])
        self.assertEqual(len(self.mock_get_oncall_users.mock_calls), 1)
        self.assertEqual(len(self.mock_send_oncall_response.mock_calls), 1)

    def test_two_msgs_two_good(self):
        msg = SlackMessage(type="message",
                           user="PDUSER1",
                           channel="C1",
                           text="!oncall")
        yield from self.pd.process_message(msg)
        msg = SlackMessage(type="message",
                           user="PDUSER1",
                           channel="C1",
                           text="!oncall")
        yield from self.pd.process_message(msg)
        self.assertEqual(len(self.mock_get_pagerduty_schedules.mock_calls), 2)
        self.assertEqual(len(self.mock_get_oncall_users.mock_calls), 2)
        self.assertEqual(len(self.mock_send_oncall_response.mock_calls), 2)

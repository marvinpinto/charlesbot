import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from charlesbot.plugins.pagerduty.pagerduty_schedule import PagerdutySchedule
from charlesbot.plugins.pagerduty.pagerduty_user import PagerdutyUser
from charlesbot.slack.slack_attachment import SlackAttachment


class TestSendOncallResponse(asynctest.TestCase):

    def setUp(self):
        patcher2 = patch('charlesbot.slack.slack_connection.SlackConnection.api_call')  # NOQA
        self.addCleanup(patcher2.stop)
        self.mock_api_call = patcher2.start()

        from charlesbot.slack.slack_connection import SlackConnection
        self.slack_connection = SlackConnection()

        from charlesbot.plugins.pagerduty.pagerduty_helpers import send_oncall_response  # NOQA
        self.send_response = send_oncall_response

        self.token = "tokensekrit"
        self.subdomain = "subdomain"

    def tearDown(self):
        self.slack_connection._drop()

    def test_one_schedule_no_oncall_people(self):
        pd_sched1 = PagerdutySchedule(name="Schedule1",
                                      oncall_users=[])
        attachment = SlackAttachment(
            color="#36a64f",
            fallback="*Schedule1* - could not determine who's on call :disappointed:",  # NOQA
            text="*Schedule1* - could not determine who's on call :disappointed:",  # NOQA
            mrkdwn_in=["text"]
        )
        expected = call('chat.postMessage',
                        channel="chan1",
                        attachments=attachment,
                        as_user=False,
                        username="Currently On-Call",
                        icon_url="https://slack.global.ssl.fastly.net/11699/img/services/pagerduty_48.png")  # NOQA
        yield from self.send_response(self.slack_connection,
                                      [pd_sched1],
                                      "chan1")
        self.assertEqual(self.mock_api_call.mock_calls, [expected])

    def test_one_schedule_one_oncall_person(self):
        pd_user1 = PagerdutyUser(user_id="PDUSER1",
                                 full_name="User 1")
        pd_sched1 = PagerdutySchedule(name="Schedule1",
                                      oncall_users=[pd_user1])
        attachment = SlackAttachment(
            color="#36a64f",
            fallback="*Schedule1* - User 1",
            text="*Schedule1* - User 1",
            mrkdwn_in=["text"]
        )
        expected = call('chat.postMessage',
                        channel="chan1",
                        attachments=attachment,
                        as_user=False,
                        username="Currently On-Call",
                        icon_url="https://slack.global.ssl.fastly.net/11699/img/services/pagerduty_48.png")  # NOQA
        yield from self.send_response(self.slack_connection,
                                      [pd_sched1],
                                      "chan1")
        self.assertEqual(self.mock_api_call.mock_calls, [expected])

    def test_one_schedule_two_oncall_people(self):
        pd_user1 = PagerdutyUser(user_id="PDUSER1",
                                 full_name="User 1")
        pd_user2 = PagerdutyUser(user_id="PDUSER2",
                                 full_name="User 2")
        pd_sched1 = PagerdutySchedule(name="Schedule1",
                                      oncall_users=[pd_user1, pd_user2])
        attachment = SlackAttachment(
            color="#36a64f",
            fallback="*Schedule1* - User 1, User 2",
            text="*Schedule1* - User 1, User 2",
            mrkdwn_in=["text"]
        )
        expected = call('chat.postMessage',
                        channel="chan1",
                        attachments=attachment,
                        as_user=False,
                        username="Currently On-Call",
                        icon_url="https://slack.global.ssl.fastly.net/11699/img/services/pagerduty_48.png")  # NOQA
        yield from self.send_response(self.slack_connection,
                                      [pd_sched1],
                                      "chan1")
        self.assertEqual(self.mock_api_call.mock_calls, [expected])

    def test_two_schedules_no_oncall_people(self):
        pd_sched1 = PagerdutySchedule(name="Schedule1",
                                      oncall_users=[])
        pd_sched2 = PagerdutySchedule(name="Schedule2",
                                      oncall_users=[])
        attachment = SlackAttachment(
            color="#36a64f",
            fallback="*Schedule1* - could not determine who's on call :disappointed:\n*Schedule2* - could not determine who's on call :disappointed:",  # NOQA
            text="*Schedule1* - could not determine who's on call :disappointed:\n*Schedule2* - could not determine who's on call :disappointed:",  # NOQA
            mrkdwn_in=["text"]
        )
        expected = call('chat.postMessage',
                        channel="chan1",
                        attachments=attachment,
                        as_user=False,
                        username="Currently On-Call",
                        icon_url="https://slack.global.ssl.fastly.net/11699/img/services/pagerduty_48.png")  # NOQA
        yield from self.send_response(self.slack_connection,
                                      [pd_sched1, pd_sched2],
                                      "chan1")
        self.assertEqual(self.mock_api_call.mock_calls, [expected])

    def test_two_schedules_one_oncall_person(self):
        pd_user1 = PagerdutyUser(user_id="PDUSER1",
                                 full_name="User 1")
        pd_sched1 = PagerdutySchedule(name="Schedule1",
                                      oncall_users=[pd_user1])
        pd_sched2 = PagerdutySchedule(name="Schedule2",
                                      oncall_users=[])
        attachment = SlackAttachment(
            color="#36a64f",
            fallback="*Schedule1* - User 1\n*Schedule2* - could not determine who's on call :disappointed:",  # NOQA
            text="*Schedule1* - User 1\n*Schedule2* - could not determine who's on call :disappointed:",  # NOQA
            mrkdwn_in=["text"]
        )
        expected = call('chat.postMessage',
                        channel="chan1",
                        attachments=attachment,
                        as_user=False,
                        username="Currently On-Call",
                        icon_url="https://slack.global.ssl.fastly.net/11699/img/services/pagerduty_48.png")  # NOQA
        yield from self.send_response(self.slack_connection,
                                      [pd_sched1, pd_sched2],
                                      "chan1")
        self.assertEqual(self.mock_api_call.mock_calls, [expected])

    def test_two_schedules_one_oncall_person_per_schedule(self):
        pd_user1 = PagerdutyUser(user_id="PDUSER1",
                                 full_name="User 1")
        pd_sched1 = PagerdutySchedule(name="Schedule1",
                                      oncall_users=[pd_user1])
        pd_sched2 = PagerdutySchedule(name="Schedule2",
                                      oncall_users=[pd_user1])
        attachment = SlackAttachment(
            color="#36a64f",
            fallback="*Schedule1* - User 1\n*Schedule2* - User 1",
            text="*Schedule1* - User 1\n*Schedule2* - User 1",
            mrkdwn_in=["text"]
        )
        expected = call('chat.postMessage',
                        channel="chan1",
                        attachments=attachment,
                        as_user=False,
                        username="Currently On-Call",
                        icon_url="https://slack.global.ssl.fastly.net/11699/img/services/pagerduty_48.png")  # NOQA
        yield from self.send_response(self.slack_connection,
                                      [pd_sched1, pd_sched2],
                                      "chan1")
        self.assertEqual(self.mock_api_call.mock_calls, [expected])

    def test_two_schedules_two_oncall_people(self):
        pd_user1 = PagerdutyUser(user_id="PDUSER1",
                                 full_name="User 1")
        pd_user2 = PagerdutyUser(user_id="PDUSER2",
                                 full_name="User 2")
        pd_sched1 = PagerdutySchedule(name="Schedule1",
                                      oncall_users=[pd_user1, pd_user2])
        pd_sched2 = PagerdutySchedule(name="Schedule2",
                                      oncall_users=[pd_user1, pd_user2])
        attachment = SlackAttachment(
            color="#36a64f",
            fallback="*Schedule1* - User 1, User 2\n*Schedule2* - User 1, User 2",  # NOQA
            text="*Schedule1* - User 1, User 2\n*Schedule2* - User 1, User 2",
            mrkdwn_in=["text"]
        )
        expected = call('chat.postMessage',
                        channel="chan1",
                        attachments=attachment,
                        as_user=False,
                        username="Currently On-Call",
                        icon_url="https://slack.global.ssl.fastly.net/11699/img/services/pagerduty_48.png")  # NOQA
        yield from self.send_response(self.slack_connection,
                                      [pd_sched1, pd_sched2],
                                      "chan1")
        self.assertEqual(self.mock_api_call.mock_calls, [expected])

    def test_two_schedules_three_oncall_people(self):
        pd_user1 = PagerdutyUser(user_id="PDUSER1",
                                 full_name="User 1")
        pd_user2 = PagerdutyUser(user_id="PDUSER2",
                                 full_name="User 2")
        pd_user3 = PagerdutyUser(user_id="PDUSER3",
                                 full_name="User 3")
        pd_sched1 = PagerdutySchedule(name="Schedule1",
                                      oncall_users=[pd_user1])
        pd_sched2 = PagerdutySchedule(name="Schedule2",
                                      oncall_users=[pd_user1, pd_user2, pd_user3])  # NOQA
        attachment = SlackAttachment(
            color="#36a64f",
            fallback="*Schedule1* - User 1\n*Schedule2* - User 1, User 2, User 3",  # NOQA
            text="*Schedule1* - User 1\n*Schedule2* - User 1, User 2, User 3",
            mrkdwn_in=["text"]
        )
        expected = call('chat.postMessage',
                        channel="chan1",
                        attachments=attachment,
                        as_user=False,
                        username="Currently On-Call",
                        icon_url="https://slack.global.ssl.fastly.net/11699/img/services/pagerduty_48.png")  # NOQA
        yield from self.send_response(self.slack_connection,
                                      [pd_sched1, pd_sched2],
                                      "chan1")
        self.assertEqual(self.mock_api_call.mock_calls, [expected])

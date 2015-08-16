import asynctest
import json
from asynctest.mock import patch
from asynctest.mock import call
from charlesbot.plugins.pagerduty.pagerduty_schedule import PagerdutySchedule


class TestGetPagerdutySchedules(asynctest.TestCase):

    def setUp(self):
        patcher = patch('charlesbot.plugins.pagerduty.pagerduty_helpers.http_get_auth_request')  # NOQA
        self.addCleanup(patcher.stop)
        self.mock_http = patcher.start()
        self.mock_http.side_effect = {}
        from charlesbot.plugins.pagerduty.pagerduty_helpers import get_pagerduty_schedules  # NOQA
        self.get_schedules = get_pagerduty_schedules
        self.mock_http.reset_mock()
        self.token = "sekrittoken"
        self.subdomain = "subdomain"

    def test_http_args(self):
        yield from self.get_schedules(self.token, self.subdomain)
        expected = call(auth_string="token=sekrittoken",
                        url="https://subdomain.pagerduty.com/api/v1/schedules")
        self.assertEqual(self.mock_http.mock_calls, [expected])

    def test_bogus_get_response_1(self):
        output = {}
        self.mock_http.side_effect = [json.dumps(output)]
        schedules = yield from self.get_schedules(self.token, self.subdomain)
        self.assertEqual(schedules, [])

    def test_bogus_get_response_2(self):
        output = "blahblahblah"
        self.mock_http.side_effect = [json.dumps(output)]
        schedules = yield from self.get_schedules(self.token, self.subdomain)
        self.assertEqual(schedules, [])

    def test_bogus_get_response_3(self):
        output = 42
        self.mock_http.side_effect = [json.dumps(output)]
        schedules = yield from self.get_schedules(self.token, self.subdomain)
        self.assertEqual(schedules, [])

    def test_bogus_get_response_4(self):
        output = None
        self.mock_http.side_effect = [json.dumps(output)]
        schedules = yield from self.get_schedules(self.token, self.subdomain)
        self.assertEqual(schedules, [])

    def test_bogus_get_response_5(self):
        output = ""
        self.mock_http.side_effect = [json.dumps(output)]
        schedules = yield from self.get_schedules(self.token, self.subdomain)
        self.assertEqual(schedules, [])

    def test_bogus_json(self):
        output = "[{]"
        self.mock_http.side_effect = [output]
        schedules = yield from self.get_schedules(self.token, self.subdomain)
        self.assertEqual(schedules, [])

    def test_timezone_key_not_present(self):
        output = {
            "schedules": [
                {
                    "description": "",
                    "escalation_policies": [
                        {
                            "id": "P46664",
                            "name": "Team Escalation"
                        }
                    ],
                    "id": "P123456",
                    "name": "On call schedule name",
                    "today": "2015-08-09"
                }
            ],
        }
        self.mock_http.side_effect = [json.dumps(output)]
        expected = PagerdutySchedule(
            description="",
            escalation_policies=[{"id": "P46664", "name": "Team Escalation"}],
            id="P123456",
            name="On call schedule name",
        )
        schedules = yield from self.get_schedules(self.token, self.subdomain)
        self.assertEqual(len(schedules), 1)
        self.assertTrue(expected in schedules)

    def test_one_schedule(self):
        response = {
            "schedules": [
                {
                    "description": "",
                    "escalation_policies": [
                        {
                            "id": "P46664",
                            "name": "Team Escalation"
                        }
                    ],
                    "id": "P123456",
                    "name": "On call schedule name",
                    "time_zone": "Eastern Time (US & Canada)",
                    "today": "2015-08-09"
                }
            ]
        }
        expected = PagerdutySchedule(
            description="",
            escalation_policies=[{"id": "P46664", "name": "Team Escalation"}],
            id="P123456",
            name="On call schedule name",
            time_zone="Eastern Time (US & Canada)",
            oncall_users=[]
        )
        self.mock_http.side_effect = [json.dumps(response)]
        schedules = yield from self.get_schedules(self.token, self.subdomain)
        self.assertEqual(len(schedules), 1)
        self.assertTrue(expected in schedules)

    def test_two_schedules(self):
        response = {
            "schedules": [
                {
                    "description": "",
                    "escalation_policies": [
                        {
                            "id": "ESC1",
                            "name": "Escalation 1"
                        }
                    ],
                    "id": "SCHED1",
                    "name": "Schedule 1",
                    "time_zone": "Eastern Time (US & Canada)",
                    "today": "2015-08-09"
                },
                {
                    "description": "",
                    "escalation_policies": [
                        {
                            "id": "ESC2",
                            "name": "Escalation 2"
                        }
                    ],
                    "id": "SCHED2",
                    "name": "Schedule 2",
                    "time_zone": "Eastern Time (US & Canada)",
                    "today": "2015-08-09"
                },
            ],
        }
        expected_1 = PagerdutySchedule(
            description="",
            escalation_policies=[{"id": "ESC1", "name": "Escalation 1"}],
            id="SCHED1",
            name="Schedule 1",
            time_zone="Eastern Time (US & Canada)"
        )
        expected_2 = PagerdutySchedule(
            description="",
            escalation_policies=[{"id": "ESC2", "name": "Escalation 2"}],
            id="SCHED2",
            name="Schedule 2",
            time_zone="Eastern Time (US & Canada)"
        )
        self.mock_http.side_effect = [json.dumps(response)]
        schedules = yield from self.get_schedules(self.token, self.subdomain)
        self.assertEqual(len(schedules), 2)
        self.assertTrue(expected_2 in schedules)
        self.assertTrue(expected_1 in schedules)

    @asynctest.ignore_loop
    def test_schedule_equality(self):
        sched_1 = PagerdutySchedule(
            description="sched_1",
            name="Schedule 1",
        )
        sched_2 = PagerdutySchedule(
            description="sched_2",
            name="Schedule 2",
        )
        self.assertNotEqual(sched_1, sched_2)
        sched_dict = {
            "description": "sched_1",
        }
        sched_2.load(sched_dict)
        self.assertNotEqual(sched_1, sched_2)
        sched_dict = {
            "name": "Schedule 1",
        }
        sched_2.load(sched_dict)
        self.assertEqual(sched_1, sched_2)

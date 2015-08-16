import asynctest
import asyncio
import json
from asynctest.mock import call
from asynctest.mock import patch
from charlesbot.plugins.pagerduty.pagerduty_schedule import PagerdutySchedule
from charlesbot.plugins.pagerduty.pagerduty_user import PagerdutyUser


class TestGetOncallUsers(asynctest.TestCase):

    def setUp(self):
        patcher = patch('charlesbot.plugins.pagerduty.pagerduty_helpers.http_get_auth_request')  # NOQA
        self.addCleanup(patcher.stop)
        self.mock_http = patcher.start()
        self.mock_http.side_effect = {}
        from charlesbot.plugins.pagerduty.pagerduty_helpers import get_oncall_users  # NOQA
        self.get_users = get_oncall_users
        self.mock_http.reset_mock()
        self.token = "tokensekrit"
        self.subdomain = "subdomain"
        self.pd_sched = PagerdutySchedule()

    @asyncio.coroutine
    def bogus_response_helper(self, output):
        self.pd_sched.id = "001"
        self.mock_http.side_effect = [json.dumps(output)]
        yield from self.get_users(self.token,
                                  self.subdomain,
                                  [self.pd_sched],
                                  "since",
                                  "until")
        self.assertEqual(self.pd_sched.oncall_users, [])

    def test_empty_schedules(self):
        yield from self.get_users(self.token,
                                  self.subdomain,
                                  [],
                                  "since",
                                  "until")
        self.assertEqual(self.mock_http.mock_calls, [])

    def test_one_schedule_no_scheduleid(self):
        yield from self.get_users(self.token,
                                  self.subdomain,
                                  [self.pd_sched],
                                  "since",
                                  "until")
        self.assertEqual(self.mock_http.mock_calls, [])

    def test_http_args(self):
        self.pd_sched.id = "001"
        yield from self.get_users(self.token,
                                  self.subdomain,
                                  [self.pd_sched],
                                  "since",
                                  "until")
        expected = call(auth_string="token=tokensekrit",
                        url="https://subdomain.pagerduty.com/api/v1/schedules/001/entries",  # NOQA
                        payload={"since": "since", "until": "until"})
        self.assertEqual(self.mock_http.mock_calls, [expected])

    def test_bogus_get_response_1(self):
        yield from self.bogus_response_helper({})

    def test_bogus_get_response_2(self):
        yield from self.bogus_response_helper("blahblahblah")

    def test_bogus_get_response_3(self):
        yield from self.bogus_response_helper(42)

    def test_bogus_get_response_4(self):
        yield from self.bogus_response_helper(None)

    def test_bogus_get_response_5(self):
        yield from self.bogus_response_helper("")

    def test_bogus_json(self):
        yield from self.bogus_response_helper("[{]")

    def test_color_key_not_present(self):
        self.pd_sched.id = "002"
        output = {
            "entries": [
                {
                    "user": {
                        "email": "gregory_hilll@deckow.us",
                        "name": "Gregory",
                        "id": "PRT2T0A"
                    }
                }
            ]
        }
        self.mock_http.side_effect = [json.dumps(output)]
        yield from self.get_users(self.token,
                                  self.subdomain,
                                  [self.pd_sched],
                                  "since",
                                  "until")
        pd_user = PagerdutyUser(pd_color="",
                                email="gregory_hilll@deckow.us",
                                user_id="PRT2T0A",
                                full_name="Gregory")
        self.assertEqual(len(self.pd_sched.oncall_users), 1)
        self.assertTrue(pd_user in self.pd_sched.oncall_users)

    def test_multiple_schedules(self):
        pd_sched1 = PagerdutySchedule(id="001")
        pd_sched2 = PagerdutySchedule(id="002")
        output1 = {
            "entries": [
                {
                    "user": {
                        "email": "user1@example.org",
                        "name": "User One",
                        "id": "PD1",
                        "color": "poop",
                    }
                },
                {
                    "user": {
                        "email": "user2@example.org",
                        "name": "User Two",
                        "id": "PD2",
                        "color": "green",
                    }
                }
            ]
        }
        output2 = {
            "entries": [
                {
                    "user": {
                        "email": "user2@example.org",
                        "name": "User Two",
                        "id": "PD2",
                        "color": "green",
                    }
                },
                {
                    "user": {
                        "email": "user1@example.org",
                        "name": "User One",
                        "id": "PD1",
                        "color": "poop",
                    }
                }
            ]
        }
        self.mock_http.side_effect = [json.dumps(output1), json.dumps(output2)]
        yield from self.get_users(self.token,
                                  self.subdomain,
                                  [pd_sched1, pd_sched2],
                                  "since",
                                  "until")
        pd_user1 = PagerdutyUser(pd_color="poop",
                                 email="user1@example.org",
                                 user_id="PD1",
                                 full_name="User One")
        pd_user2 = PagerdutyUser(pd_color="green",
                                 email="user2@example.org",
                                 user_id="PD2",
                                 full_name="User Two")
        self.assertEqual(len(pd_sched1.oncall_users), 2)
        self.assertTrue(pd_user1 in pd_sched1.oncall_users)
        self.assertTrue(pd_user2 in pd_sched1.oncall_users)
        self.assertEqual(len(pd_sched2.oncall_users), 2)
        self.assertTrue(pd_user1 in pd_sched2.oncall_users)
        self.assertTrue(pd_user2 in pd_sched2.oncall_users)

    @asynctest.ignore_loop
    def test_user_equality(self):
        user_1 = PagerdutyUser(
            pd_color="poop",
            email="user1@examples.org",
            user_id="PD111",
            full_name="User One"
        )
        user_2 = PagerdutyUser(
            pd_color="green",
            email="user2@examples.org",
            user_id="PD222",
            full_name="User Two"
        )
        self.assertNotEqual(user_1, user_2)
        sched_dict = {
            "user": {
                "color": "green",
            }
        }
        user_1.load(sched_dict)
        self.assertNotEqual(user_1, user_2)
        sched_dict = {
            "user": {
                "email": "user2@examples.org",
            }
        }
        user_1.load(sched_dict)
        self.assertNotEqual(user_1, user_2)
        sched_dict = {
            "user": {
                "id": "PD222",
            }
        }
        user_1.load(sched_dict)
        self.assertNotEqual(user_1, user_2)
        sched_dict = {
            "user": {
                "name": "User Two",
            }
        }
        user_1.load(sched_dict)
        self.assertEqual(user_1, user_2)

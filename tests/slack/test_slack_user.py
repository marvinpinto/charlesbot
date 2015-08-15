import asynctest
import json
from asynctest.mock import patch
from asynctest.mock import MagicMock
from asynctest.mock import call


class TestSlackUser(asynctest.TestCase):

    def setUp(self):
        patcher = patch('charlesbot.slack.slack_user.slack_rtm_api_call')
        self.addCleanup(patcher.stop)
        self.mock_slack_rtm = patcher.start()
        from charlesbot.slack.slack_user import SlackUser
        self.slack_client = MagicMock()
        self.su = SlackUser()

    @asynctest.ignore_loop
    def test_user_equality(self):
        from charlesbot.slack.slack_user import SlackUser
        user1 = SlackUser(id="SU01",
                          name="userone",
                          color="red")
        user2 = SlackUser(id="SU02",
                          name="usertwo",
                          color="blue")
        self.assertNotEqual(user1, user2)
        user2.id = "SU01"
        self.assertNotEqual(user1, user2)
        user2.name = "userone"
        self.assertNotEqual(user1, user2)
        user2.color = "red"
        self.assertEqual(user1, user2)

    @asynctest.ignore_loop
    def test_user_return_string(self):
        self.su.id = "SU01"
        self.su.name = "User One"
        self.su.deleted = False
        self.su.is_admin = False
        self.su.has_2fa = True
        user_json = json.loads(str(self.su))
        self.assertEqual(user_json.get('id'), "SU01")
        self.assertEqual(user_json.get('name'), "User One")
        self.assertEqual(user_json.get('deleted'), False)
        self.assertEqual(user_json.get('is_admin'), False)
        self.assertEqual(user_json.get('has_2fa'), True)
        self.assertEqual(user_json.get('is_owner'), "")

    def test_empty_rtm_response(self):
        self.su.name = "suser"
        self.mock_slack_rtm.side_effect = ["{}"]
        yield from self.su.retrieve_slack_user_info(self.slack_client,
                                                    "fake123")
        expected_call = call(self.slack_client, "users.info", user="fake123")
        self.assertEqual(self.mock_slack_rtm.mock_calls, [expected_call]),
        self.assertEqual(self.su.name, "suser")
        self.assertEqual(self.su.last_name, "")
        self.assertEqual(self.su.is_bot, "")

    def test_no_profile_key(self):
        self.su.name = "suser"
        user_info = {
            "ok": True,
            "user": {
                "id": "U023BECGF",
                "name": "bobby"
            }
        }
        self.mock_slack_rtm.side_effect = [json.dumps(user_info)]
        yield from self.su.retrieve_slack_user_info(self.slack_client,
                                                    "fake123")
        expected_call = call(self.slack_client, "users.info", user="fake123")
        self.assertEqual(self.mock_slack_rtm.mock_calls, [expected_call]),
        self.assertEqual(self.su.name, "bobby")
        self.assertEqual(self.su.id, "U023BECGF")
        self.assertEqual(self.su.last_name, "")
        self.assertEqual(self.su.is_bot, "")

    def test_with_profile_key(self):
        self.su.name = "suser"
        user_info = {
            "ok": True,
            "user": {
                "id": "U023BECGF",
                "name": "bobby",
                "profile": {
                    "real_name": "Bobby Tables",
                    "image_24": "https://www.tables.com",
                }
            }
        }
        self.mock_slack_rtm.side_effect = [json.dumps(user_info)]
        yield from self.su.retrieve_slack_user_info(self.slack_client,
                                                    "fake123")
        expected_call = call(self.slack_client, "users.info", user="fake123")
        self.assertEqual(self.mock_slack_rtm.mock_calls, [expected_call]),
        self.assertEqual(self.su.name, "bobby")
        self.assertEqual(self.su.id, "U023BECGF")
        self.assertEqual(self.su.real_name, "Bobby Tables")
        self.assertEqual(self.su.image_24, "https://www.tables.com")
        self.assertEqual(self.su.is_bot, "")

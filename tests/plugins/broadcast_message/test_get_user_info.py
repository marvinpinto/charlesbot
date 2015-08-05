import asynctest
import json
from asynctest.mock import patch
from asynctest.mock import MagicMock


class TestGetUserInfo(asynctest.TestCase):

    def setUp(self):
        patcher = patch('charlesbot.plugins.broadcast_message.slack_rtm_api_call')  # NOQA
        self.addCleanup(patcher.stop)
        self.mock_slack_rtm = patcher.start()
        from charlesbot.plugins.broadcast_message import BroadcastMessage
        self.slack_client = MagicMock()
        self.bm = BroadcastMessage(self.slack_client)
        self.bm.seed_initial_data = MagicMock()

    def test_get_user_info(self):
        users_info = {
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
        expected = {
            "id": "U023BECGF",
            "username": "bobby",
            "real_name": "Bobby Tables",
            "thumb_24": "https://www.tables.com"
        }
        self.mock_slack_rtm.return_value = json.dumps(users_info)
        retval = yield from self.bm.get_user_info("fake")
        self.assertEqual(retval, expected)

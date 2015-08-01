import unittest
from charlesbot.util.slack import parse_user_info
import json


class TestParseUserInfo(unittest.TestCase):

    def test_user_info_ok(self):
        users_info = {
            "ok": True,
            "user": {
                "id": "U023BECGF",
                "name": "bobby",
                "deleted": False,
                "color": "9f69e7",
                "profile": {
                    "first_name": "Bobby",
                    "last_name": "Tables",
                    "real_name": "Bobby Tables",
                    "email": "bobby@slack.com",
                    "skype": "my-skype-name",
                    "phone": "+1 (123) 456 7890",
                    "image_24": "https://www.tables.com",
                    "image_32": "https:\/\/...",
                    "image_48": "https:\/\/...",
                    "image_72": "https:\/\/...",
                    "image_192": "https:\/\/..."
                },
                "is_admin": True,
                "is_owner": True,
                "has_2fa": True,
                "has_files": True
            }
        }
        retval = parse_user_info(json.dumps(users_info))
        expected = {
            "id": "U023BECGF",
            "username": "bobby",
            "real_name": "Bobby Tables",
            "thumb_24": "https://www.tables.com"
        }
        self.assertEqual(retval, expected)

    def test_user_info_missing(self):
        users_info = {
            "ok": True,
            "user": {
                "name": "bobby",
                "deleted": False,
                "color": "9f69e7",
                "profile": {
                    "first_name": "Bobby",
                    "last_name": "Tables",
                    "email": "bobby@slack.com",
                    "skype": "my-skype-name",
                    "phone": "+1 (123) 456 7890",
                    "image_32": "https:\/\/...",
                    "image_48": "https:\/\/...",
                    "image_72": "https:\/\/...",
                    "image_192": "https:\/\/..."
                },
                "is_admin": True,
                "is_owner": True,
                "has_2fa": True,
                "has_files": True
            }
        }
        with self.assertRaises(KeyError):
            parse_user_info(json.dumps(users_info))

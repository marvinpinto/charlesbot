import unittest
from charlesbot.util.slack import get_robot_info
import json


class TestGetRobotInfo(unittest.TestCase):

    def test_robot_info_ok(self):
        auth_test = {
            "ok": True,
            "url": "https:\/\/myteam.slack.com\/",
            "team": "My Team",
            "user": "cal",
            "team_id": "T12345",
            "user_id": "U12345"
        }
        retval = get_robot_info(json.dumps(auth_test))
        self.assertEqual(retval, {"U12345": "cal"})

    def test_robot_info_missing(self):
        auth_test = {
            "ok": True,
            "url": "https:\/\/myteam.slack.com\/",
            "team": "My Team",
            "team_id": "T12345",
        }
        with self.assertRaises(KeyError):
            get_robot_info(json.dumps(auth_test))

    def test_robot_info_missing_user(self):
        auth_test = {
            "ok": True,
            "url": "https:\/\/myteam.slack.com\/",
            "team": "My Team",
            "team_id": "T12345",
            "user_id": "U12345"
        }
        with self.assertRaises(KeyError):
            get_robot_info(json.dumps(auth_test))

    def test_robot_info_missing_user_id(self):
        auth_test = {
            "ok": True,
            "url": "https:\/\/myteam.slack.com\/",
            "team": "My Team",
            "user": "cal",
            "team_id": "T12345",
        }
        with self.assertRaises(KeyError):
            get_robot_info(json.dumps(auth_test))

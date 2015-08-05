import unittest
from charlesbot.util.parse import parse_channel_message


class TestParseChannelMessage(unittest.TestCase):

    def test_return_none(self):
        message = {
            "type": "message",
            "user": "U2147483697",
            "text": "This is my message to you ooo oouuu",
        }
        channel, text, user = parse_channel_message(message)
        self.assertEqual(channel, None)
        self.assertEqual(text, None)
        self.assertEqual(user, None)

    def test_channel_empty(self):
        message = {
            "type": "message",
            "user": "user",
            "channel": "",
            "text": "Don't worry",
        }
        channel, text, user = parse_channel_message(message)
        self.assertEqual(channel, "")
        self.assertEqual(text, "Don't worry")
        self.assertEqual(user, "user")

    def test_text_empty(self):
        message = {
            "type": "message",
            "user": "U2147483697",
            "channel": "About a thang",
            "text": "",
        }
        channel, text, user = parse_channel_message(message)
        self.assertEqual(channel, "About a thang")
        self.assertEqual(text, "")
        self.assertEqual(user, "U2147483697")

    def test_user_empty(self):
        message = {
            "type": "message",
            "user": "",
            "channel": "About a thang",
            "text": "Cause every little thing, is going to be alright",
        }
        channel, text, user = parse_channel_message(message)
        self.assertEqual(channel, "About a thang")
        self.assertEqual(text, "Cause every little thing, is going to be alright")  # NOQA
        self.assertEqual(user, "")

    def test_return_ok(self):
        message = {
            "type": "message",
            "user": "U2147483697",
            "channel": "Cause every little thing",
            "text": "is going to be alright",
        }
        channel, text, user = parse_channel_message(message)
        self.assertEqual(channel, "Cause every little thing")
        self.assertEqual(text, "is going to be alright")
        self.assertEqual(user, "U2147483697")

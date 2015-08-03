import unittest
from charlesbot.util.parse import parse_channel_message
# from charlesbot.util.parse import filter_message_types


class TestParseChannelMessage(unittest.TestCase):

    def test_return_none(self):
        message = {
            "type": "message",
            "user": "U2147483697",
            "text": "This is my message to you ooo oouuu",
        }
        channel, text = parse_channel_message(message)
        self.assertEqual(channel, None)
        self.assertEqual(text, None)

    def test_channel_empty(self):
        message = {
            "type": "message",
            "user": "U2147483697",
            "channel": "",
            "text": "Don't worry",
        }
        channel, text = parse_channel_message(message)
        self.assertEqual(channel, "")
        self.assertEqual(text, "Don't worry")

    def test_text_empty(self):
        message = {
            "type": "message",
            "user": "U2147483697",
            "channel": "About a thang",
            "text": "",
        }
        channel, text = parse_channel_message(message)
        self.assertEqual(channel, "About a thang")
        self.assertEqual(text, "")

    def test_return_ok(self):
        message = {
            "type": "message",
            "user": "U2147483697",
            "channel": "Cause every little thing",
            "text": "is going to be alright",
        }
        channel, text = parse_channel_message(message)
        self.assertEqual(channel, "Cause every little thing")
        self.assertEqual(text, "is going to be alright")

import unittest
import json
from charlesbot.slack.slack_attachment import SlackAttachment


class TestSlackAttachment(unittest.TestCase):

    def test_attachment_equality(self):
        attach1 = SlackAttachment(color="red",
                                  fallback="fallback msg",
                                  text="real message")
        attach2 = SlackAttachment(color="blue",
                                  fallback="fallback msg 2",
                                  text="real message 2")
        self.assertNotEqual(attach1, attach2)
        attach_dict = {
            "color": "red"
        }
        attach2.load(attach_dict)
        self.assertNotEqual(attach1, attach2)
        attach_dict = {
            "fallback": "fallback msg"
        }
        attach2.load(attach_dict)
        self.assertNotEqual(attach1, attach2)
        attach_dict = {
            "text": "real message"
        }
        attach2.load(attach_dict)
        self.assertEqual(attach1, attach2)

    def test_attachment_string(self):
        attach1 = SlackAttachment(color="green",
                                  fallback="fallback msg green",
                                  text="real message green")
        dummy_json = json.loads(str(attach1))
        self.assertEqual(len(dummy_json), 1)
        self.assertEqual(len(dummy_json[0].keys()), 9)
        self.assertEqual(dummy_json[0].get('color'), "green")
        self.assertEqual(dummy_json[0].get('fallback'), "fallback msg green")
        self.assertEqual(dummy_json[0].get('text'), "real message green")

import unittest
from charlesbot.slack.slack_room_joined import SlackRoomJoined
import json


class TestSlackRoomJoined(unittest.TestCase):

    class DummyObject(SlackRoomJoined):

        properties = [
            "property1",
            "property2",
            "type",
        ]

        def __init__(myself, **kwargs):
            super().__init__(**kwargs)

        @property
        def compatibility_key(self):
            return "dummykey"

    def setUp(self):
        self.dc = TestSlackRoomJoined.DummyObject()

    def test_compatibility(self):
        self.assertTrue(self.dc.is_compatible({"type": "dummykey"}))

    def test_add_extra_property(self):
        property_dict = {
            "batman": "robin",
            "type": "such type",
        }
        self.dc.load(property_dict)
        dummy_json = json.loads(str(self.dc))
        self.assertEqual(len(dummy_json.keys()), 3)
        self.assertEqual(dummy_json.get('property1'), "")
        self.assertEqual(dummy_json.get('property2'), "")
        self.assertEqual(dummy_json.get('type'), "such type")
        self.assertEqual(dummy_json.get('batman', "default"), "default")

    def test_update_property_one(self):
        property_dict = {
            "type": "such type",
            "channel": {
                "property1": "property1 value",
            }
        }
        self.dc.load(property_dict)
        dummy_json = json.loads(str(self.dc))
        self.assertEqual(len(dummy_json.keys()), 3)
        self.assertEqual(dummy_json.get('property1'), "property1 value")
        self.assertEqual(dummy_json.get('property2'), "")
        self.assertEqual(dummy_json.get('type'), "such type")

    def test_update_property_two(self):
        property_dict = {
            "type": "such type",
            "channel": {
                "property2": "property2 value",
            }
        }
        self.dc.load(property_dict)
        dummy_json = json.loads(str(self.dc))
        self.assertEqual(len(dummy_json.keys()), 3)
        self.assertEqual(dummy_json.get('property1'), "")
        self.assertEqual(dummy_json.get('property2'), "property2 value")
        self.assertEqual(dummy_json.get('type'), "such type")

    def test_update_properties(self):
        property_dict = {
            "type": "such type",
            "channel": {
                "property1": "property1 value",
                "property2": "property2 value",
            }
        }
        self.dc.load(property_dict)
        dummy_json = json.loads(str(self.dc))
        self.assertEqual(len(dummy_json.keys()), 3)
        self.assertEqual(dummy_json.get('property1'), "property1 value")
        self.assertEqual(dummy_json.get('property2'), "property2 value")
        self.assertEqual(dummy_json.get('type'), "such type")

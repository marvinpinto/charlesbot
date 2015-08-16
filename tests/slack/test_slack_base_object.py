import unittest
from charlesbot.slack.slack_base_object import SlackBaseObject


class TestSlackBaseObject(unittest.TestCase):

    class DummyObject(SlackBaseObject):

        properties = [
            "property1",
            "property2",
            "type",
        ]

        def __init__(myself, **kwargs):
            super().__init__(**kwargs)

        @property
        def compatibility_key(self):
            return "dummymessage"

    def setUp(self):
        self.dc = TestSlackBaseObject.DummyObject()

    def test_compatibility_type_not_present(self):
        object_dict = {}
        self.assertFalse(self.dc.is_compatible(object_dict))  # NOQA

    def test_compatibility_type_empty(self):
        object_dict = {
            "type": "",
        }
        self.assertFalse(self.dc.is_compatible(object_dict))  # NOQA

    def test_compatibility_type_invalid(self):
        object_dict = {
            "type": "boo",
        }
        self.assertFalse(self.dc.is_compatible(object_dict))  # NOQA

    def test_compatibility_valid(self):
        object_dict = {
            "type": "dummymessage",
        }
        self.assertTrue(self.dc.is_compatible(object_dict))  # NOQA

import unittest
from charlesbot.base_object import BaseObject
import json


class TestBaseObject(unittest.TestCase):

    class DummyObject(BaseObject):

        properties = [
            "property1",
            "property2",
        ]

        def __init__(myself, **kwargs):
            super().__init__(**kwargs)

        def is_compatible(object_dict):
            return True

    def setUp(self):
        self.dc = TestBaseObject.DummyObject()

    def test_compatibility(self):
        self.assertTrue(TestBaseObject.DummyObject.is_compatible({}))

    def test_add_extra_property(self):
        property_dict = {
            "batman": "robin"
        }
        self.dc.load(property_dict)
        dummy_json = json.loads(str(self.dc))
        self.assertEqual(len(dummy_json.keys()), 2)
        self.assertEqual(dummy_json.get('property1'), "")
        self.assertEqual(dummy_json.get('property2'), "")
        self.assertEqual(dummy_json.get('batman', "default"), "default")

    def test_update_property_one(self):
        property_dict = {
            "property1": "property1 value",
        }
        self.dc.load(property_dict)
        dummy_json = json.loads(str(self.dc))
        self.assertEqual(len(dummy_json.keys()), 2)
        self.assertEqual(dummy_json.get('property1'), "property1 value")
        self.assertEqual(dummy_json.get('property2'), "")

    def test_update_property_two(self):
        property_dict = {
            "property2": "property2 value",
        }
        self.dc.load(property_dict)
        dummy_json = json.loads(str(self.dc))
        self.assertEqual(len(dummy_json.keys()), 2)
        self.assertEqual(dummy_json.get('property1'), "")
        self.assertEqual(dummy_json.get('property2'), "property2 value")

    def test_update_properties(self):
        property_dict = {
            "property1": "property1 value",
            "property2": "property2 value",
        }
        self.dc.load(property_dict)
        dummy_json = json.loads(str(self.dc))
        self.assertEqual(len(dummy_json.keys()), 2)
        self.assertEqual(dummy_json.get('property1'), "property1 value")
        self.assertEqual(dummy_json.get('property2'), "property2 value")

    def test_equality(self):
        do1 = TestBaseObject.DummyObject(property1="do1 prop1 value",
                                         property2="do1 prop2 value")
        do2 = TestBaseObject.DummyObject(property1="do2 prop1 value",
                                         property2="do2 prop2 value")
        self.assertNotEqual(do1, do2)
        do2.property1 = "do1 prop1 value"
        self.assertNotEqual(do1, do2)
        do2.property2 = "do1 prop2 value"
        self.assertEqual(do1, do2)

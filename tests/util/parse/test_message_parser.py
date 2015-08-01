import unittest
from charlesbot.util.parse import parse_msg_with_prefix
from charlesbot.util.parse import filter_message_types


class TestMessageParser(unittest.TestCase):

    def test_prefix_uppercase(self):
        msg = "!ALL hi, there!"
        retval = parse_msg_with_prefix("!all", msg)
        self.assertEqual("hi, there!", retval)

    def test_prefix_mixed(self):
        msg = "!AlL hi, there!"
        retval = parse_msg_with_prefix("!all", msg)
        self.assertEqual("hi, there!", retval)

    def test_prefix_colon(self):
        msg = "!all: hi, there!"
        retval = parse_msg_with_prefix("!all", msg)
        self.assertEqual("hi, there!", retval)

    def test_prefix_colon_two(self):
        msg = "!all:hi, there!"
        retval = parse_msg_with_prefix("!all", msg)
        self.assertEqual("hi, there!", retval)

    def test_prefix_space(self):
        msg = "!all hi, there!"
        retval = parse_msg_with_prefix("!all", msg)
        self.assertEqual("hi, there!", retval)

    def test_prefix_whitespace(self):
        msg = "!all  hi, there!"
        retval = parse_msg_with_prefix("!all", msg)
        self.assertEqual("hi, there!", retval)

    def test_prefix_leading_whitespace(self):
        msg = " !all  hi, there!"
        retval = parse_msg_with_prefix("!all", msg)
        self.assertEqual("hi, there!", retval)

    def test_prefix_leading_whitespace_two(self):
        msg = "  !all  hi, there!"
        retval = parse_msg_with_prefix("!all", msg)
        self.assertEqual("hi, there!", retval)

    def test_prefix_invalid_one(self):
        msg = "s  !all  hi, there!"
        retval = parse_msg_with_prefix("!all", msg)
        self.assertEqual(None, retval)

    def test_prefix_invalid_two(self):
        msg = "!allhi, there!"
        retval = parse_msg_with_prefix("!all", msg)
        self.assertEqual(None, retval)

    def test_filter_okay(self):
        msg = {"type": "group_joined", "channel": "fun"}
        types = ['group_joined', 'channel_joined']
        fields = ['channel']
        self.assertEqual(filter_message_types(msg, types, fields), True)

    def test_filter_type_not_present(self):
        msg = {"types": "group_joined", "channel": "fun"}
        types = ['group_joined', 'channel_joined']
        fields = ['channel']
        self.assertEqual(filter_message_types(msg, types, fields), False)

    def test_filter_type_not_in_types(self):
        msg = {"type": "group_joined", "channel": "fun"}
        types = ['group_joining', 'channel_joined']
        fields = ['channel']
        self.assertEqual(filter_message_types(msg, types, fields), False)

    def test_filter_field_not_present(self):
        msg = {"type": "group_joined", "channel": "fun"}
        types = ['group_joined', 'channel_joined']
        fields = ['channels']
        self.assertEqual(filter_message_types(msg, types, fields), False)

    def test_filter_too_many_fields(self):
        msg = {"type": "group_joined", "channel": "fun"}
        types = ['group_joined', 'channel_joined']
        fields = ['channel', 'type', 'channels']
        self.assertEqual(filter_message_types(msg, types, fields), False)

    def test_filter_exact_amount_of_fields(self):
        msg = {"type": "group_joined", "channel": "fun"}
        types = ['group_joined', 'channel_joined']
        fields = ['channel', 'type']
        self.assertEqual(filter_message_types(msg, types, fields), True)

    def test_filter_no_fields(self):
        msg = {"type": "group_joined", "channel": "fun"}
        types = ['group_joined', 'channel_joined']
        fields = []
        self.assertEqual(filter_message_types(msg, types, fields), True)

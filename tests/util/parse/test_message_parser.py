import unittest
from charlesbot.util.parse import parse_msg_with_prefix


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

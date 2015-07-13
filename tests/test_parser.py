import unittest
from charlesbot.util.parser import parse_args
from charlesbot.util.parser import capture_sys_output


class TestParser(unittest.TestCase):

    def setUp(self):
        self.regex_1 = "CharlesBOT is a Slack RTM robot!"
        self.regex_2 = \
            "See https://github.com/marvinpinto/charlesbot for details"

    def test_empty_config(self):
        parse_args([])
        self.assertEqual("", "")

    def test_config_help_1(self):
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                parse_args(['-h'])
        output = stdout.getvalue().strip().replace('\n', ' ')
        self.assertEqual(cm.exception.code, 0)
        self.assertRegexpMatches(output, self.regex_1)
        self.assertRegexpMatches(output, self.regex_2)

    def test_config_help_2(self):
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                parse_args(['--help'])
        output = stdout.getvalue().strip().replace('\n', ' ')
        self.assertEqual(cm.exception.code, 0)
        self.assertRegexpMatches(output, self.regex_1)
        self.assertRegexpMatches(output, self.regex_2)

    def test_bogus_args(self):
        with self.assertRaises(SystemExit) as cm:
            with capture_sys_output() as (stdout, stderr):
                parse_args(['--bogus'])
        self.assertEqual(cm.exception.code, 2)

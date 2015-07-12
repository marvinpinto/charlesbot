import unittest
from charlesbot.util.parser import parse_args


class TestParser(unittest.TestCase):

    def test_empty_config(self):
        with self.assertRaises(SystemExit) as cm:
            parse_args([])
        self.assertEqual(cm.exception.code, 2)

    def test_config_supplied_1(self):
        parsed_args = parse_args(['--config', 'hello'])
        self.assertEqual(parsed_args.config, "hello")

    def test_config_supplied_2(self):
        parsed_args = parse_args(['-c', 'hello'])
        self.assertEqual(parsed_args.config, "hello")

    def test_config_blank_1(self):
        parsed_args = parse_args(['--config', ''])
        self.assertEqual(parsed_args.config, "")

    def test_config_blank_2(self):
        parsed_args = parse_args(['-c', ''])
        self.assertEqual(parsed_args.config, "")

    def test_config_invalid_1(self):
        with self.assertRaises(SystemExit) as cm:
            parse_args(['--config'])
        self.assertEqual(cm.exception.code, 2)

    def test_config_invalid_2(self):
        with self.assertRaises(SystemExit) as cm:
            parse_args(['-c'])
        self.assertEqual(cm.exception.code, 2)

    def test_bogus_args(self):
        with self.assertRaises(SystemExit) as cm:
            parse_args(['--bogus'])
        self.assertEqual(cm.exception.code, 2)

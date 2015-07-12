import unittest
from charlesbot.util.parser import parse_args


class TestParser(unittest.TestCase):

    def test_default_values(self):
        parsed_args = parse_args([])
        self.assertEqual(parsed_args.debug, False)
        self.assertEqual(parsed_args.config, "")

    def test_debug_arg(self):
        parsed_args = parse_args(['--debug'])
        self.assertEqual(parsed_args.debug, True)
        self.assertEqual(parsed_args.config, "")

    def test_config_supplied_1(self):
        parsed_args = parse_args(['--config', 'hello'])
        self.assertEqual(parsed_args.debug, False)
        self.assertEqual(parsed_args.config, "hello")

    def test_config_supplied_2(self):
        parsed_args = parse_args(['-c', 'hello'])
        self.assertEqual(parsed_args.debug, False)
        self.assertEqual(parsed_args.config, "hello")

    def test_config_blank_1(self):
        parsed_args = parse_args(['--config', ''])
        self.assertEqual(parsed_args.debug, False)
        self.assertEqual(parsed_args.config, "")

    def test_config_blank_2(self):
        parsed_args = parse_args(['-c', ''])
        self.assertEqual(parsed_args.debug, False)
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

    def test_combination_args_1(self):
        parsed_args = parse_args(['--debug', '-c', 'config file'])
        self.assertEqual(parsed_args.debug, True)
        self.assertEqual(parsed_args.config, "config file")

    def test_combination_args_2(self):
        parsed_args = parse_args(['-c', 'config file', '--debug'])
        self.assertEqual(parsed_args.debug, True)
        self.assertEqual(parsed_args.config, "config file")

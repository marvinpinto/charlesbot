import unittest
from charlesbot.util.parse import does_msg_contain_prefix


class TestDoesMsgContainPrefix(unittest.TestCase):

    def test_prefix_one(self):
        msg = "!HELP"
        retval = does_msg_contain_prefix("!help", msg)
        self.assertTrue(retval)

    def test_prefix_two(self):
        msg = "!HelP"
        retval = does_msg_contain_prefix("!help", msg)
        self.assertTrue(retval)

    def test_prefix_three(self):
        msg = "!help"
        retval = does_msg_contain_prefix("!help", msg)
        self.assertTrue(retval)

    def test_prefix_four(self):
        msg = "!helps"
        retval = does_msg_contain_prefix("!help", msg)
        self.assertFalse(retval)

    def test_prefix_five(self):
        msg = "!helps "
        retval = does_msg_contain_prefix("!help", msg)
        self.assertFalse(retval)

    def test_prefix_six(self):
        msg = "!helps asdfsdf"
        retval = does_msg_contain_prefix("!help", msg)
        self.assertFalse(retval)

    def test_prefix_seven(self):
        msg = "!help asdfsadfa"
        retval = does_msg_contain_prefix("!help", msg)
        self.assertTrue(retval)

    def test_prefix_eight(self):
        msg = "!help  asdfsadfa"
        retval = does_msg_contain_prefix("!help", msg)
        self.assertTrue(retval)

    def test_prefix_nine(self):
        msg = "!help  "
        retval = does_msg_contain_prefix("!help", msg)
        self.assertTrue(retval)

    def test_prefix_ten(self):
        msg = " !help  "
        retval = does_msg_contain_prefix("!help", msg)
        self.assertTrue(retval)

    def test_prefix_eleven(self):
        msg = "  !help  "
        retval = does_msg_contain_prefix("!help", msg)
        self.assertTrue(retval)

    def test_prefix_twelve(self):
        msg = "!helpsasdfsdf"
        retval = does_msg_contain_prefix("!help", msg)
        self.assertFalse(retval)

    def test_prefix_thirteen(self):
        msg = "  !help lllllllllllllllll  asdfsadf"
        retval = does_msg_contain_prefix("!help", msg)
        self.assertTrue(retval)

    def test_prefix_fourteen(self):
        msg = "  !help                                    "
        retval = does_msg_contain_prefix("!help", msg)
        self.assertTrue(retval)

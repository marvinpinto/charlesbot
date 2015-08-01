import unittest
from charlesbot.util.slack import get_robot_channel_membership
from tests import load_fixture


class TestGetRobotChannelMembership(unittest.TestCase):

    def setUp(self):
        self.channel_list_one = load_fixture('channel_list_one.json')
        self.channel_list_two = load_fixture('channel_list_two.json')
        self.channel_list_three = load_fixture('channel_list_three.json')
        self.channel_list_four = load_fixture('channel_list_four.json')
        self.channel_list_five = load_fixture('channel_list_five.json')
        self.channel_list_six = load_fixture('channel_list_six.json')
        self.channel_list_seven = load_fixture('channel_list_seven.json')
        self.channel_list_eight = load_fixture('channel_list_eight.json')
        self.channel_list_nine = load_fixture('channel_list_nine.json')
        self.channel_list_ten = load_fixture('channel_list_ten.json')

    def test_slack_channel_membership_single(self):
        channel_list = self.channel_list_one
        membership = get_robot_channel_membership(channel_list)
        self.assertEqual(len(membership), 1)
        self.assertCountEqual(membership, {'C024BE91L': 'fun1'})

    def test_slack_channel_membership_none(self):
        channel_list = self.channel_list_three
        membership = get_robot_channel_membership(channel_list)
        self.assertEqual(len(membership), 0)
        self.assertCountEqual(membership, {})

    def test_slack_channel_membership_error_1(self):
        # malformed json
        channel_list = self.channel_list_four
        with self.assertRaises(ValueError):
            get_robot_channel_membership(channel_list)

    def test_slack_channel_membership_error_2(self):
        # channel key not present in json file
        channel_list = self.channel_list_five
        with self.assertRaises(KeyError):
            get_robot_channel_membership(channel_list)

    def test_slack_channel_membership_multiple_0(self):
        # member of none of three channels
        channel_list = self.channel_list_six
        membership = get_robot_channel_membership(channel_list)
        self.assertEqual(len(membership), 0)
        self.assertCountEqual(membership, {})

    def test_slack_channel_membership_multiple_1(self):
        # member of one of three channels
        channel_list = self.channel_list_seven
        membership = get_robot_channel_membership(channel_list)
        self.assertEqual(len(membership), 1)
        self.assertCountEqual(membership, {'C024BE91B': 'fun2'})

    def test_slack_channel_membership_multiple_2(self):
        # member of two of three channels
        channel_list = self.channel_list_eight
        membership = get_robot_channel_membership(channel_list)
        self.assertEqual(len(membership), 2)
        self.assertCountEqual(
            membership,
            {'C024BE91B': 'fun2', 'C024BE91C': 'fun3'}
        )

    def test_slack_channel_membership_multiple_3(self):
        # member of three of three channels
        channel_list = self.channel_list_nine
        membership = get_robot_channel_membership(channel_list)
        self.assertEqual(len(membership), 3)
        self.assertCountEqual(
            membership,
            {'C024BE91B': 'fun2', 'C024BE91C': 'fun3', 'C024BE91A': 'fun1'}
        )

    def test_slack_channel_membership_general(self):
        # general channel
        channel_list = self.channel_list_ten
        membership = get_robot_channel_membership(channel_list)
        self.assertEqual(len(membership), 1)
        self.assertCountEqual(
            membership,
            {'C024BE91B': 'fun2'}
        )

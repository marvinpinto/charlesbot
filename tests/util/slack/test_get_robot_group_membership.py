import unittest
from charlesbot.util.slack import get_robot_group_membership
from tests import load_fixture


class TestGetRobotGroupMembership(unittest.TestCase):

    def setUp(self):
        self.group_list_one = load_fixture('group_list_one.json')
        self.group_list_two = load_fixture('group_list_two.json')
        self.group_list_three = load_fixture('group_list_three.json')
        self.group_list_four = load_fixture('group_list_four.json')

    def test_slack_group_membership_single(self):
        group_list = self.group_list_one
        membership = get_robot_group_membership(group_list)
        self.assertEqual(len(membership), 1)
        self.assertCountEqual(membership, {'G024BE91L': 'secretplans'})

    def test_slack_group_membership_none(self):
        group_list = "{}"
        membership = get_robot_group_membership(group_list)
        self.assertEqual(len(membership), 0)
        self.assertCountEqual(membership, {})

    def test_slack_group_membership_error_1(self):
        # malformed json
        group_list = self.group_list_two
        with self.assertRaises(ValueError):
            get_robot_group_membership(group_list)

    def test_slack_group_membership_error_2(self):
        # group key not present in json file
        group_list = self.group_list_three
        membership = get_robot_group_membership(group_list)
        self.assertEqual(len(membership), 0)
        self.assertCountEqual(membership, {})

    def test_slack_group_membership_multiple(self):
        # member of more than one group
        group_list = self.group_list_four
        membership = get_robot_group_membership(group_list)
        self.assertEqual(len(membership), 3)
        self.assertCountEqual(
            membership,
            {'G024BE91A': 'secretplans1',
             'G024BE91B': 'secretplans2',
             'G024BE91C': 'secretplans3'}
        )

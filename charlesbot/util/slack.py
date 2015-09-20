import json
import logging
log = logging.getLogger(__name__)


def get_robot_info(auth_test):
    json_str = json.loads(auth_test)
    robot_name = json_str["user"]
    robot_id = json_str["user_id"]
    return {robot_id: robot_name}


def get_robot_channel_membership(channel_list):
    json_list = json.loads(channel_list)
    membership = {}
    for channel in json_list['channels']:
        if channel['is_member'] and not channel['is_general']:
            channel_id = channel['id']
            channel_name = channel['name']
            membership[channel_id] = channel_name
    return membership


def get_robot_group_membership(group_list):
    json_list = json.loads(group_list)
    membership = {}

    if 'groups' not in json_list:
        return membership

    for group in json_list['groups']:
        group_id = group['id']
        group_name = group['name']
        membership[group_id] = group_name
    return membership

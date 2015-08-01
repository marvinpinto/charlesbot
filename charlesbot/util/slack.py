import json
import logging
import asyncio
log = logging.getLogger(__name__)


@asyncio.coroutine
def slack_rtm_api_call(slack_client, api_endpoint, **kwargs):
    val = slack_client.api_call(api_endpoint, **kwargs)
    json_str = json.loads(val.decode('utf-8'))
    if not json_str['ok']:
        log.error(
            "Error fetching %s - response: %s",
            api_endpoint,
            str(json_str['ok'])
        )
        log.error(json_str)
        return json.dumps("[]")
    return json.dumps(json_str)


def parse_user_info(users_info):
    user = {}
    json_resp = json.loads(users_info)
    user.update({"id": json_resp['user']['id']})
    user.update({"username": json_resp['user']['name']})
    user.update({"real_name": json_resp['user']['profile']['real_name']})
    user.update({"thumb_24": json_resp['user']['profile']['image_24']})
    return user


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

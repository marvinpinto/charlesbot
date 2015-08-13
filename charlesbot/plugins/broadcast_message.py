from charlesbot.util.slack import (
    slack_rtm_api_call,
    get_robot_channel_membership,
    get_robot_group_membership,
    parse_user_info
)

from charlesbot.util.parse import (
    parse_msg_with_prefix,
    filter_message_types,
    parse_channel_message
)

from charlesbot.base_plugin import BasePlugin
from charlesbot.slack.slack_attachment import SlackAttachment
import asyncio


class BroadcastMessage(BasePlugin):

    def __init__(self, slack_client):
        super().__init__(slack_client, "Broadcast Message")
        self.room_membership = {}
        self.robot_info = {}
        self.seed_initial_data()

    def seed_initial_data(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.seed_channel_membership())
        loop.create_task(self.seed_group_membership())

    def log_room_membership(self):
        self.log.info("Currently in: %s"
                      % ", ".join(sorted(self.room_membership.values())))

    @asyncio.coroutine
    def seed_channel_membership(self):
        result = yield from slack_rtm_api_call(self.sc,
                                               'channels.list',
                                               exclude_archived=1)
        channels = get_robot_channel_membership(result)
        self.room_membership.update(channels)
        self.log_room_membership()

    @asyncio.coroutine
    def seed_group_membership(self):
        result = yield from slack_rtm_api_call(self.sc,
                                               'groups.list',
                                               exclude_archived=1)
        groups = get_robot_group_membership(result)
        self.room_membership.update(groups)
        self.log_room_membership()

    @asyncio.coroutine
    def process_message(self, messages):
        for msg in messages:
            tasks = [
                self.add_to_room(msg),
                self.remove_from_room(msg),
                self.parse_wall_message(msg)
            ]
            yield from asyncio.gather(*tasks)

    @asyncio.coroutine
    def add_to_room(self, msg):
        types = ['group_joined', 'channel_joined']
        fields = ['channel']
        if not filter_message_types(msg, types, fields):
            return
        room_name = msg['channel']['name']
        room_id = msg['channel']['id']
        self.room_membership.update({room_id: room_name})
        self.log.info("I was invited to join %s" % room_name)
        self.log_room_membership()

    @asyncio.coroutine
    def remove_from_room(self, msg):
        types = ['group_left', 'channel_left']
        fields = ['channel']
        if not filter_message_types(msg, types, fields):
            return
        room_id = msg['channel']

        room_name = ""
        if room_id in self.room_membership:
            room_name = self.room_membership[room_id]

        self.room_membership.pop(room_id, None)

        if room_name:
            self.log.info("I have been removed from %s" % room_name)

        self.log_room_membership()

    def handle_single_prefixed_message(self, channel_id):
        pass

    @asyncio.coroutine
    def parse_wall_message(self, msg):
        channel, msg, sent_by = parse_channel_message(msg)
        if not channel or not msg or not sent_by:
            return
        parsed = parse_msg_with_prefix("!wall", msg)
        if parsed:
            user = yield from self.get_user_info(sent_by)
            yield from self.send_broadcast_message(parsed, user)

    @asyncio.coroutine
    def get_user_info(self, user_id):
        result = yield from slack_rtm_api_call(
            self.sc,
            'users.info',
            user=user_id
        )
        return parse_user_info(result)

    @asyncio.coroutine
    def send_broadcast_message(self, msg, user):
        wall = "Broadcast message from %s - %s" % (user['real_name'], msg)

        attachment = SlackAttachment(fallback=wall,
                                     author_name=user['real_name'],
                                     author_icon=user['thumb_24'],
                                     text=msg)

        for key in self.room_membership.keys():
            yield from slack_rtm_api_call(
                self.sc,
                'chat.postMessage',
                channel=key,
                attachments=attachment,
                as_user=False,
                username="Broadcast Message",
                icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2015-07-26/8217958308_48.png"  # NOQA
            )

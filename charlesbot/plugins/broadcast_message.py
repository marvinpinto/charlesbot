from charlesbot.util.slack import (
    get_robot_channel_membership,
    get_robot_group_membership
)

from charlesbot.util.parse import (
    parse_msg_with_prefix,
    does_msg_contain_prefix
)

from charlesbot.base_plugin import BasePlugin
from charlesbot.slack.slack_attachment import SlackAttachment
from charlesbot.slack.slack_user import SlackUser
import asyncio

from charlesbot.slack.slack_channel_joined import SlackChannelJoined
from charlesbot.slack.slack_channel_left import SlackChannelLeft
from charlesbot.slack.slack_group_joined import SlackGroupJoined
from charlesbot.slack.slack_group_left import SlackGroupLeft
from charlesbot.slack.slack_message import SlackMessage


class BroadcastMessage(BasePlugin):

    def __init__(self):
        super().__init__("Broadcast Message")
        self.room_membership = {}
        self.seed_initial_data()

    def seed_initial_data(self):  # pragma: no cover
        loop = asyncio.get_event_loop()
        loop.create_task(self.seed_channel_membership())
        loop.create_task(self.seed_group_membership())

    def get_help_message(self):  # pragma: no cover
        return "!wall <msg> - Broadcast a message to all channels I'm a part of"  # NOQA

    def log_room_membership(self):
        self.log.info("Currently in: %s"
                      % ", ".join(sorted(self.room_membership.values())))

    @asyncio.coroutine
    def seed_channel_membership(self):
        result = yield from self.slack.api_call('channels.list',
                                                exclude_archived=1)
        channels = get_robot_channel_membership(result)
        self.room_membership.update(channels)
        self.log_room_membership()

    @asyncio.coroutine
    def seed_group_membership(self):
        result = yield from self.slack.api_call('groups.list',
                                                exclude_archived=1)
        groups = get_robot_group_membership(result)
        self.room_membership.update(groups)
        self.log_room_membership()

    @asyncio.coroutine
    def process_message(self, message):
        tasks = [
            self.add_to_room(message),
            self.remove_from_room(message),
            self.parse_wall_message(message)
        ]
        yield from asyncio.gather(*tasks)

    @asyncio.coroutine
    def add_to_room(self, message):
        if not type(message) is SlackChannelJoined and not type(message) is SlackGroupJoined:  # NOQA
            return
        self.room_membership.update({message.id: message.name})
        self.log.info("I was invited to join %s" % message.name)
        self.log_room_membership()

    @asyncio.coroutine
    def remove_from_room(self, message):
        if not type(message) is SlackChannelLeft and not type(message) is SlackGroupLeft:  # NOQA
            return
        room_name = self.room_membership.get(message.channel, "")
        self.room_membership.pop(message.channel, None)
        if room_name:
            self.log.info("I have been removed from %s" % room_name)
        self.log_room_membership()

    @asyncio.coroutine
    def parse_wall_message(self, message):
        if not type(message) is SlackMessage:
            return
        if not does_msg_contain_prefix("!wall", message.text):
            return
        parsed_message = parse_msg_with_prefix("!wall", message.text)
        if not parsed_message:  # pragma: no cover
            return
        slack_user = SlackUser()
        yield from slack_user.retrieve_slack_user_info(self.slack,
                                                       message.user)
        yield from self.send_broadcast_message(parsed_message, slack_user)

    @asyncio.coroutine
    def send_broadcast_message(self, msg, user):
        wall = "Broadcast message from %s - %s" % (user.real_name, msg)

        attachment = SlackAttachment(fallback=wall,
                                     author_name=user.real_name,
                                     author_icon=user.image_24,
                                     text=msg)

        for key in self.room_membership.keys():
            yield from self.slack.api_call(
                'chat.postMessage',
                channel=key,
                attachments=attachment,
                as_user=False,
                username="Broadcast Message",
                icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2015-07-26/8217958308_48.png"  # NOQA
            )

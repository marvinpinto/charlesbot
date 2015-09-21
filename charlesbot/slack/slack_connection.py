from charlesbot.util.borg import Borg
from slackclient import SlackClient
from charlesbot.config import configuration
import traceback
import asyncio
import json
import sys
import logging
import importlib


class SlackConnection(Borg):

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(__name__)
        self.initialized = False

    def initialize(self):  # pragma: no cover
        if not self.initialized:
            self.get_slack_token()
            self.connect()
            self.initialized = True

    def get_slack_token(self):  # pragma: no cover
        config_dict = configuration.get()
        self.token = config_dict['main']['slackbot_token']

    def connect(self):  # pragma: no cover
        self.sc = SlackClient(self.token)
        if not self.sc.rtm_connect():
            self.log.critical("Error conecting to Slack - token issue?")
            self.log.critical("--- full stack trace ---")
            self.log.critical(traceback.format_exc())
            sys.exit(1)

    @asyncio.coroutine
    def get_stream_messages(self):
        self.initialize()
        return_messages = []
        try:
            messages = self.sc.rtm_read()
            for msg in messages:
                message_object = self.get_message_type(msg)
                return_messages.append(message_object)
        except BrokenPipeError as b:
            self.log.critical("Error reading from slack socket: %s" % b)
            self.log.critical("--- full stack trace ---")
            self.log.critical(traceback.format_exc())
            sys.exit(1)
        return return_messages

    def get_message_type(self, msg):
        self.initialize()
        obj_list = [
            "charlesbot.slack.slack_pong.SlackPong",
            "charlesbot.slack.slack_channel_joined.SlackChannelJoined",
            "charlesbot.slack.slack_channel_left.SlackChannelLeft",
            "charlesbot.slack.slack_group_joined.SlackGroupJoined",
            "charlesbot.slack.slack_group_left.SlackGroupLeft",
            "charlesbot.slack.slack_message.SlackMessage",
        ]
        for obj in obj_list:
            module_name, class_name = obj.rsplit(".", 1)
            obj_class = getattr(importlib.import_module(module_name), class_name)  # NOQA
            return_obj = obj_class()

            if getattr(return_obj, 'is_compatible')(msg):
                return_obj.load(msg)
                return return_obj
        return None

    @asyncio.coroutine
    def send_channel_message(self, channel_id, message):  # pragma: no cover
        self.initialize()
        self.sc.rtm_send_message(channel_id, message)

    @asyncio.coroutine
    def send_ping_message(self):  # pragma: no cover
        self.initialize()
        self.sc.server.ping()

    @asyncio.coroutine
    def api_call(self, api_endpoint, **kwargs):
        self.initialize()
        val = self.sc.api_call(api_endpoint, **kwargs)
        json_str = json.loads(val.decode('utf-8'))
        if not json_str['ok']:
            self.log.error(
                "Error fetching %s - response: %s",
                api_endpoint,
                str(json_str['ok'])
            )
            self.log.error(json_str)
            return json.dumps("{}")
        return json.dumps(json_str)

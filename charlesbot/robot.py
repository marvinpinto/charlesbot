from slackclient import SlackClient
import logging
import asyncio
import sys
import signal
import traceback
import functools
import importlib
from charlesbot.config import configuration


class Robot(object):

    def __init__(self):  # pragma: no cover
        self.log = logging.getLogger(__name__)
        config_dict = configuration.get()
        self.token = config_dict['main']['slackbot_token']
        self.enabled_plugins = config_dict['main']['enabled_plugins']
        self.sc = None
        self.is_running = True

    def connect(self):  # pragma: no cover
        """Convenience method that creates Server instance"""
        self.sc = SlackClient(self.token)
        return self.sc.rtm_connect()

    @asyncio.coroutine
    def produce(self):  # pragma: no cover
        while self.is_running:
            yield from self.route_message_to_plugin()

    @asyncio.coroutine
    def route_message_to_plugin(self):  # pragma: no cover
        try:
            messages = self.sc.rtm_read()
            for msg in messages:
                message_object = self.get_message_type(msg)
                for plug in self.plugin_list:
                    yield from self.queue_message(message_object, plug)
        except BrokenPipeError as b:
            self.log.error("Error reading from slack socket: %s" % b)
            self.log.debug(traceback.format_exc())
        yield from asyncio.sleep(0.5)

    def get_message_type(self, msg):  # pragma: no cover
        obj_list = [
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

    def initialize_plugins(self):  # pragma: no cover
        return_list = []
        if not self.enabled_plugins:
            return return_list
        for x in self.enabled_plugins:
            module_name, class_name = x.rsplit(".", 1)
            obj_class = getattr(importlib.import_module(module_name), class_name)  # NOQA
            return_obj = obj_class(self.sc)
            return_list.append(return_obj)
        return return_list

    @asyncio.coroutine
    def queue_message(self, message, plugin):
        if message:
            yield from plugin.queue_message(message)

    def exit_cleanly(self):  # pragma: no cover
        loop = asyncio.get_event_loop()
        self.log.info("Shutting down charlesbot")
        self.is_running = False

        for plug in self.plugin_list:
            self.log.info("Shutting down plugin: %s" % plug.get_plugin_name())
            plug.is_running = False

        pending = asyncio.Task.all_tasks()
        asyncio.gather(*pending).cancel()
        loop.stop()

    def start(self):  # pragma: no cover
        if not self.connect():
            self.log.error("Error conecting to Slack - possible token issue?")
            sys.exit(1)
        loop = asyncio.get_event_loop()
        self.plugin_list = self.initialize_plugins()
        loop.create_task(self.produce())
        loop.add_signal_handler(
            signal.SIGINT,
            functools.partial(self.exit_cleanly)
        )
        try:
            loop.run_forever()
        finally:
            loop.close()

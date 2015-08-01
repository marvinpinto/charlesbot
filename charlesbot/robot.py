from charlesbot.util.config import get_config_file_name
from charlesbot.util.config import read_config
from charlesbot.util.plugins import initialize_plugins
from slackclient import SlackClient
import logging
import asyncio
import sys
import signal
import traceback
import functools


class Robot(object):

    def __init__(self):
        self.config = read_config(get_config_file_name())
        self.log = logging.getLogger(__name__)
        self.token = self.config.get('main', 'slackbot_token')
        self.enabled_plugins = self.config.get('main', 'enabled_plugins')
        self.sc = None
        self.is_running = True

    def connect(self):
        """Convenience method that creates Server instance"""
        self.sc = SlackClient(self.token)
        return self.sc.rtm_connect()

    @asyncio.coroutine
    def produce(self):
        while self.is_running:
            yield from self.route_message_to_plugin()

    @asyncio.coroutine
    def route_message_to_plugin(self):
        try:
            msg = self.sc.rtm_read()
            for plug in self.plugin_list:
                yield from self.queue_message(msg, plug)
        except BrokenPipeError as b:
            self.log.error("Error reading from slack socket: %s" % b)
            self.log.debug(traceback.format_exc())
        yield from asyncio.sleep(0.5)

    @asyncio.coroutine
    def queue_message(self, message, plugin):
        if message:
            self.log.debug(
                "Routing message %s to plugin %s" % (message, plugin)
            )
            yield from plugin.q.put(message)

    def exit_cleanly(self):
        loop = asyncio.get_event_loop()
        self.log.info("Shutting down charlesbot")
        self.is_running = False

        for plug in self.plugin_list:
            self.log.info("Shutting down plugin: %s" % plug.get_plugin_name())
            plug.is_running = False

        pending = asyncio.Task.all_tasks()
        asyncio.gather(*pending).cancel()
        loop.stop()

    def start(self):
        if not self.connect():
            self.log.error("Error conecting to Slack - possible token issue?")
            sys.exit(1)
        loop = asyncio.get_event_loop()
        self.plugin_list = initialize_plugins(self.sc, self.enabled_plugins)
        loop.create_task(self.produce())
        loop.add_signal_handler(
            signal.SIGINT,
            functools.partial(self.exit_cleanly)
        )
        try:
            loop.run_forever()
        finally:
            loop.close()

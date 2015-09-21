import logging
import asyncio
import signal
import functools
import importlib
from charlesbot.config import configuration
from charlesbot.slack.slack_connection import SlackConnection


class Robot(object):

    def __init__(self):  # pragma: no cover
        self.log = logging.getLogger(__name__)
        self.initialize_robot()

    def initialize_robot(self):  # pragma: no cover
        config_dict = configuration.get()
        self.token = config_dict['main']['slackbot_token']
        self.enabled_plugins = config_dict['main']['enabled_plugins']

    def is_running(self):
        return self._is_running

    def set_running(self, running):
        self._is_running = running

    @asyncio.coroutine
    def produce(self):
        while self.is_running():
            yield from self.route_message_to_plugin()

    @asyncio.coroutine
    def route_message_to_plugin(self):
        messages = yield from self.slack.get_stream_messages()
        for msg in messages:
            for plugin in self.plugin_list:
                yield from self.queue_message(msg, plugin)
        yield from asyncio.sleep(0.5)

    def initialize_plugins(self):
        return_list = []
        if not self.enabled_plugins:
            return return_list
        for x in self.enabled_plugins:
            module_name, class_name = x.rsplit(".", 1)
            obj_class = getattr(importlib.import_module(module_name), class_name)  # NOQA
            return_obj = obj_class()
            return_list.append(return_obj)
        return return_list

    def initialize_static_plugins(self):
        self.initialize_ping_plugin()
        self.initialize_help_plugin()

    def initialize_ping_plugin(self):
        from charlesbot.plugins.ping_plugin import Ping
        p = Ping()
        self.plugin_list.append(p)

    def initialize_help_plugin(self):
        from charlesbot.plugins.help_plugin import Help
        h = Help()
        for plugin in self.plugin_list:
            h.add_help_message(plugin.get_help_message())
        self.plugin_list.append(h)

    @asyncio.coroutine
    def queue_message(self, message, plugin):
        if message:
            yield from plugin.queue_message(message)

    def exit_cleanly(self):
        loop = asyncio.get_event_loop()
        self.log.info("Shutting down charlesbot")
        self.set_running(False)

        for plug in self.plugin_list:
            self.log.info("Shutting down plugin: %s" % plug.get_plugin_name())
            plug.is_running = False

        pending = asyncio.Task.all_tasks()
        asyncio.gather(*pending).cancel()
        loop.stop()

    def start(self):  # pragma: no cover
        self.set_running(True)
        self.slack = SlackConnection()
        loop = asyncio.get_event_loop()
        self.plugin_list = self.initialize_plugins()
        self.initialize_static_plugins()
        loop.create_task(self.produce())
        loop.add_signal_handler(
            signal.SIGINT,
            functools.partial(self.exit_cleanly)
        )
        try:
            loop.run_forever()
        finally:
            loop.close()

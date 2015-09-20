from abc import ABCMeta, abstractmethod
from charlesbot.slack.slack_message import SlackMessage
from charlesbot.slack.slack_connection import SlackConnection
import asyncio
import logging


class BasePlugin(metaclass=ABCMeta):

    def __init__(self, plugin_name):
        self.set_running(True)
        self.log = logging.getLogger(__name__)
        self.slack = SlackConnection()
        self._plugin_name = plugin_name
        self.log.info("Initializing the %s plugin" % plugin_name)
        self._q = asyncio.Queue()
        self.initialize_queue_consumer()

    def initialize_queue_consumer(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.consume())

    @asyncio.coroutine
    def consume(self):
        while self.is_running():
            value = yield from self._q.get()
            if self.is_bot_message(value):
                continue
            yield from self.process_message(value)

    def is_bot_message(self, message):
        if not type(message) is SlackMessage:
            return False
        if message.subtype == "bot_message":
            return True
        return False

    def get_plugin_name(self):
        return self._plugin_name

    def is_running(self):
        return self._is_running

    def set_running(self, running):
        self._is_running = running

    @asyncio.coroutine
    def queue_message(self, message):
        yield from self._q.put(message)

    @abstractmethod
    def get_help_message(self):
        pass

    @abstractmethod
    def process_message(self, message):
        pass

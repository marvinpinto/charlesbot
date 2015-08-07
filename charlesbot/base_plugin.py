from abc import ABCMeta, abstractmethod
from charlesbot.util.parse import parse_channel_message
from charlesbot.util.parse import does_msg_contain_prefix
import asyncio
import logging


class BasePlugin(metaclass=ABCMeta):

    def __init__(self, slack_client, plugin_name):
        self.set_running(True)
        self.log = logging.getLogger(__name__)
        self.sc = slack_client
        self._plugin_name = plugin_name
        self.log.info("Initializing the %s plugin" % plugin_name)
        self._q = asyncio.Queue()
        self.initialize_queue_consumer()

    def initialize_queue_consumer(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.consume())

    @asyncio.coroutine
    def parse_single_prefixed_message(self, msg, prefix):
        channel, msg, sent_by = parse_channel_message(msg)
        if not channel or not msg or not sent_by:
            return
        parsed = does_msg_contain_prefix(prefix, msg)
        if parsed:
            yield from self.handle_single_prefixed_message(channel)

    @abstractmethod
    def handle_single_prefixed_message(self, channel_id):
        pass

    @asyncio.coroutine
    def consume(self):
        while self.is_running():
            value = yield from self._q.get()
            yield from self.process_message(value)

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
    def process_message(self, messages):
        pass

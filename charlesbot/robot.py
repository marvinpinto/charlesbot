from charlesbot.util.config import get_config_file_name
from charlesbot.util.config import read_config
from slackclient import SlackClient
import logging.config
import asyncio
import sys


class Robot(object):

    def __init__(self):
        self.config = read_config(get_config_file_name())
        logging.config.fileConfig(self.config.get('main', 'logging_config'))
        self.log = logging.getLogger(__name__)
        self.token = self.config.get('main', 'slackbot_token')
        self.sc = None
        self.q = asyncio.Queue()

    def connect(self):
        """Convenience method that creates Server instance"""
        self.sc = SlackClient(self.token)
        return self.sc.rtm_connect()

    @asyncio.coroutine
    def produce(self):
        while True:
            yield from self.q.put(self.sc.rtm_read())
            yield from asyncio.sleep(0.5)

    @asyncio.coroutine
    def consume(self):
        while True:
            value = yield from self.q.get()
            print("Consumed: ", value)

    def start(self):
        if not self.connect():
            self.log.error("Error conecting to Slack - possible token issue?")
            sys.exit(1)

        asyncio.Task(self.produce())
        asyncio.Task(self.consume())
        loop = asyncio.get_event_loop()
        loop.run_forever()

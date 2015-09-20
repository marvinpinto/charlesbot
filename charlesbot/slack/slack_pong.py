from charlesbot.slack.slack_base_object import SlackBaseObject


class SlackPong(SlackBaseObject):

    properties = ['type',
                  'reply_to',
                  'time']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def compatibility_key(self):
        return "pong"

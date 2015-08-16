from charlesbot.slack.slack_base_object import SlackBaseObject


class SlackChannelLeft(SlackBaseObject):

    properties = ['channel',
                  'type']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def compatibility_key(self):
        return "channel_left"

from charlesbot.slack.slack_base_object import SlackBaseObject


class SlackMessage(SlackBaseObject):

    properties = ['type',
                  'channel',
                  'user',
                  'text',
                  'subtype']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def compatibility_key(self):
        return "message"

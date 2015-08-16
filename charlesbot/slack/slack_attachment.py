from charlesbot.base_object import BaseObject


class SlackAttachment(BaseObject):

    properties = ['color',
                  'fallback',
                  'text',
                  'mrkdwn_in',
                  'author_name',
                  'author_icon']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

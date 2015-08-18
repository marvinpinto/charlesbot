from charlesbot.base_object import BaseObject
import json


class SlackAttachment(BaseObject):

    properties = ['color',
                  'fallback',
                  'text',
                  'mrkdwn_in',
                  'author_name',
                  'author_icon',
                  'thumb_url',
                  'title',
                  'title_link']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return_dict = {}
        for prop in self.properties:
            return_dict.update({prop: getattr(self, prop)})
        return "[%s]" % json.dumps(return_dict)

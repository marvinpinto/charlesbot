from abc import ABCMeta, abstractproperty
from charlesbot.slack.slack_base_object import SlackBaseObject


class SlackRoomJoined(SlackBaseObject, metaclass=ABCMeta):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractproperty
    def compatibility_key(self):
        pass

    def load(self, object_dict):
        for prop in self.properties:
            default = getattr(self, prop)
            setattr(self, prop, object_dict.get('channel', {}).get(prop, default))  # NOQA
        self.type = object_dict.get('type')

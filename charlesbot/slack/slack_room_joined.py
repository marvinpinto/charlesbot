from abc import ABCMeta, abstractmethod
from charlesbot.base_object import BaseObject


class SlackRoomJoined(BaseObject, metaclass=ABCMeta):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def is_compatible(object_dict):
        pass

    def load(self, object_dict):
        for prop in self.properties:
            default = getattr(self, prop)
            setattr(self, prop, object_dict.get('channel', {}).get(prop, default))  # NOQA
        self.type = object_dict.get('type')

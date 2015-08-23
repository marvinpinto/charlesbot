from abc import ABCMeta, abstractproperty
from charlesbot.base_object import BaseObject


class SlackBaseObject(BaseObject, metaclass=ABCMeta):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractproperty
    def compatibility_key(self):
        pass

    def is_compatible(self, object_dict):
        try:
            my_type = object_dict.get('type', "")
            return my_type == self.compatibility_key
        except AttributeError:
            return False

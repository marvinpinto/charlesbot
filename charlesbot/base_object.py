from abc import ABCMeta
import logging
import json


class BaseObject(metaclass=ABCMeta):

    def __init__(self, **kwargs):
        self.log = logging.getLogger(__name__)
        for prop in self.properties:
            setattr(self, prop, kwargs.get(prop, ""))

    def load(self, object_dict):
        for prop in self.properties:
            default = getattr(self, prop)
            setattr(self, prop, object_dict.get(prop, default))

    def __str__(self):
        return_dict = {}
        for prop in self.properties:
            return_dict.update({prop: getattr(self, prop)})
        return json.dumps(return_dict)

    def __eq__(self, other):
        for prop in self.properties:
            if not getattr(self, prop) == getattr(other, prop):
                self.log.debug("Property %s is different" % prop)
                self.log.debug("%s != %s" % (getattr(self, prop),
                                             getattr(other, prop)))
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

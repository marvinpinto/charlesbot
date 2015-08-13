import logging


class PagerdutyUser(object):

    def __init__(self,
                 pd_color="",
                 email="",
                 user_id="",
                 full_name=""):
        self.pd_color = pd_color
        self.email = email
        self.user_id = user_id
        self.full_name = full_name
        self.log = logging.getLogger(__name__)

    def load_entry(self, entries_dict):
        self.pd_color = entries_dict.get('user', {}).get("color", self.pd_color)  # NOQA
        self.email = entries_dict.get('user', {}).get("email", self.email)
        self.user_id = entries_dict.get('user', {}).get("id", self.user_id)
        self.full_name = entries_dict.get('user', {}).get("name", self.full_name)  # NOQA

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        for element in ['pd_color',
                        'email',
                        'user_id',
                        'full_name']:
            if not getattr(self, element) == getattr(other, element):
                self.log.debug("Element %s is different" % element)
                self.log.debug("%s != %s" % (getattr(self, element),
                                             getattr(other, element)))
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

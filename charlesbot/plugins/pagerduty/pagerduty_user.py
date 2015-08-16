from charlesbot.base_object import BaseObject


class PagerdutyUser(BaseObject):

    properties = ['pd_color',
                  'email',
                  'user_id',
                  'full_name']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load(self, entries_dict):
        self.pd_color = entries_dict.get('user', {}).get("color", self.pd_color)  # NOQA
        self.email = entries_dict.get('user', {}).get("email", self.email)
        self.user_id = entries_dict.get('user', {}).get("id", self.user_id)
        self.full_name = entries_dict.get('user', {}).get("name", self.full_name)  # NOQA

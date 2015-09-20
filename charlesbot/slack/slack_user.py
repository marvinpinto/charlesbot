import json
import asyncio
from charlesbot.base_object import BaseObject


class SlackUser(BaseObject):

    main_properties = ['id',
                       'name',
                       'deleted',
                       'color',
                       'is_admin',
                       'is_owner',
                       'has_2fa',
                       'is_bot']

    profile_properties = ['first_name',
                          'last_name',
                          'real_name',
                          'email',
                          'image_24']

    properties = main_properties + profile_properties

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @asyncio.coroutine
    def retrieve_slack_user_info(self, slack_connection, user_id):
        result = yield from slack_connection.api_call('users.info',
                                                      user=user_id)
        self.load(json.loads(result))

    def load(self, user_dict):
        for prop in self.main_properties:
            default = getattr(self, prop)
            setattr(self, prop, user_dict.get('user', {}).get(prop, default))  # NOQA

        for prop in self.profile_properties:
            default = getattr(self, prop)
            setattr(self, prop, user_dict.get('user', {}).get('profile', {}).get(prop, default))  # NOQA

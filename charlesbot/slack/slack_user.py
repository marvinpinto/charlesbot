import logging
import json
import asyncio
from charlesbot.util.slack import slack_rtm_api_call


class SlackUser(object):

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

    def __init__(self, **kwargs):
        self.log = logging.getLogger(__name__)
        merged_properties = self.main_properties + self.profile_properties
        for prop in merged_properties:
            setattr(self, prop, kwargs.get(prop, ""))

    @asyncio.coroutine
    def retrieve_slack_user_info(self, slack_client, user_id):
        result = yield from slack_rtm_api_call(
            slack_client,
            'users.info',
            user=user_id
        )
        self.load(json.loads(result))

    def load(self, user_dict):
        for prop in self.main_properties:
            default = getattr(self, prop)
            setattr(self, prop, user_dict.get('user', {}).get(prop, default))  # NOQA

        for prop in self.profile_properties:
            default = getattr(self, prop)
            setattr(self, prop, user_dict.get('user', {}).get('profile', {}).get(prop, default))  # NOQA

    def __str__(self):
        return_dict = {}
        merged_properties = self.main_properties + self.profile_properties
        for prop in merged_properties:
            return_dict.update({prop: getattr(self, prop)})
        return json.dumps(return_dict)

    def __eq__(self, other):
        merged_properties = self.main_properties + self.profile_properties
        for prop in merged_properties:
            if not getattr(self, prop) == getattr(other, prop):
                self.log.debug("Property %s is different" % prop)
                self.log.debug("%s != %s" % (getattr(self, prop),
                                             getattr(other, prop)))
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

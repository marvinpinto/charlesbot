from charlesbot.base_object import BaseObject


class PagerdutySchedule(BaseObject):

    properties = ['description',
                  'escalation_policies',
                  'id',
                  'name',
                  'time_zone',
                  'oncall_users']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.oncall_users:
            self.oncall_users = []
        if not self.escalation_policies:
            self.escalation_policies = []

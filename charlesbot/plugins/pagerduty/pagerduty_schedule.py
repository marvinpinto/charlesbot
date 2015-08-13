import logging


class PagerdutySchedule(object):

    def __init__(self,
                 description="",
                 escalation_policies=None,
                 schedule_id="",
                 schedule_name="",
                 time_zone="",
                 oncall_users=None):
        self.description = description
        self.escalation_policies = escalation_policies
        self.schedule_id = schedule_id
        self.schedule_name = schedule_name
        self.time_zone = time_zone
        self.log = logging.getLogger(__name__)

        if oncall_users is None:
            self.oncall_users = []
        else:
            self.oncall_users = oncall_users

        if escalation_policies is None:
            self.escalation_policies = []
        else:
            self.escalation_policies = escalation_policies

    def load_schedule(self, schedule_dict):
        self.description = schedule_dict.get('description',
                                             self.description)
        self.escalation_policies = schedule_dict.get('escalation_policies',
                                                     self.escalation_policies)
        self.schedule_id = schedule_dict.get('id',
                                             self.schedule_id)
        self.schedule_name = schedule_dict.get('name',
                                               self.schedule_name)
        self.time_zone = schedule_dict.get('time_zone',
                                           self.time_zone)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        for element in ['description',
                        'escalation_policies',
                        'schedule_id',
                        'schedule_name',
                        'time_zone',
                        'oncall_users']:
            if not getattr(self, element) == getattr(other, element):
                self.log.debug("Element %s is different" % element)
                self.log.debug("%s != %s" % (getattr(self, element),
                                             getattr(other, element)))
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

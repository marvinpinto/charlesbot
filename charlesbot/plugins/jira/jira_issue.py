from charlesbot.base_object import BaseObject
from urllib.parse import urlparse
from urllib.parse import urlunparse


class JiraIssue(BaseObject):

    default_assignee_gravatar = "https://slack.global.ssl.fastly.net/12d4/img/services/jira_48.png"  # NOQA
    properties = ['id',
                  'key',
                  'assignee_name',
                  'assignee_gravatar',
                  'status',
                  'description',
                  'summary']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.assignee_gravatar = self.default_assignee_gravatar
        self.status = self.get_status_color(1)

    def load(self, jira_dict):  # NOQA C901 'JiraIssue.load' is too complex (14)
        if not jira_dict:
            return

        if self.is_dict_key_available(jira_dict, 'id'):
            self.id = jira_dict['id']

        if self.is_dict_key_available(jira_dict, 'key'):
            self.key = jira_dict['key']

        if not self.is_dict_key_available(jira_dict, 'fields'):
            return

        fields = jira_dict['fields']
        if self.is_dict_key_available(fields, 'assignee'):
            assignee = fields['assignee']
            if self.is_dict_key_available(assignee, 'displayName'):
                self.assignee_name = assignee['displayName']
            if self.is_dict_key_available(assignee, 'avatarUrls'):
                avatarUrls = assignee['avatarUrls']
                if self.is_dict_key_available(avatarUrls, '48x48'):
                    temp_gravatar = avatarUrls['48x48']
                    self.assignee_gravatar = self.parse_jira_base_gravatar_url(temp_gravatar)  # NOQA

        if self.is_dict_key_available(fields, 'description'):
            self.description = fields['description']

        if self.is_dict_key_available(fields, 'summary'):
            self.summary = fields['summary']

        if self.is_dict_key_available(fields, 'status'):
            status = fields['status']
            if self.is_dict_key_available(status, 'statusCategory'):
                statusCategory = status['statusCategory']
                if self.is_dict_key_available(statusCategory, 'id'):
                    temp_status_id = statusCategory['id']
                    self.status = self.get_status_color(temp_status_id)

    def is_dict_key_available(self, mdict, key):
        return key in mdict and mdict[key]

    def parse_jira_base_gravatar_url(self, gravatar_str):
        if not gravatar_str:
            return self.default_assignee_gravatar
        o = urlparse(gravatar_str)
        return urlunparse((o.scheme, o.netloc, o.path, '', '', ''))

    def get_status_color(self, status_id):
        status_colors = {
            1: "#A4ADAD",  # Default (grey)
            2: "#19689C",  # Todo (blue)
            3: "#6AC36A",  # Done (green)
            4: "#FFC875",  # In progress (yellow)
        }
        return status_colors.get(status_id, status_colors[1])

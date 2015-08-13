import logging
import json
log = logging.getLogger(__name__)


class SlackAttachment(object):

    def __init__(self,
                 color=None,
                 fallback="",
                 text=None,
                 mrkdwn_in=None,
                 author_name=None,
                 author_icon=None):
        self.color = color
        self.fallback = fallback
        self.text = text
        if mrkdwn_in is None:
            self.mrkdwn_in = []
        else:
            self.mrkdwn_in = mrkdwn_in
        self.author_name = author_name
        self.author_icon = author_icon

    def load(self, attachment_dict):
        self.color = attachment_dict.get('color', self.color)
        self.fallback = attachment_dict.get('fallback', self.fallback)
        self.text = attachment_dict.get('text', self.text)
        self.mrkdwn_in = attachment_dict.get('mrkdwn_in', self.mrkdwn_in)
        self.author_name = attachment_dict.get('author_name', self.author_name)
        self.author_icon = attachment_dict.get('author_icon', self.author_icon)

    def __str__(self):
        return_dict = {}
        for element in ['color',
                        'fallback',
                        'text',
                        'mrkdwn_in',
                        'author_name',
                        'author_icon']:
            return_dict.update({element: getattr(self, element)})
        return "[%s]" % json.dumps(return_dict)

    def __eq__(self, other):
        for element in ['color',
                        'fallback',
                        'text',
                        'mrkdwn_in',
                        'author_name',
                        'author_icon']:
            if not getattr(self, element) == getattr(other, element):
                log.debug("Element %s is different" % element)
                log.debug("%s != %s" % (getattr(self, element),
                                        getattr(other, element)))
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

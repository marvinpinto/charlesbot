import re
import logging
log = logging.getLogger(__name__)


def parse_msg_with_prefix(prefix, msg):
    regex_str = "^\s*%s[ :](.*)" % prefix
    p = re.compile(regex_str, re.IGNORECASE)
    m = p.match(msg)
    if m:
        return m.group(1).strip()
    else:
        return None


def filter_message_types(msg, types, fields):
    if 'type' not in msg.keys():
        return False
    if msg['type'] in types:
        if set(fields).issubset(msg.keys()):
            return True
    return False


def does_msg_contain_prefix(prefix, msg):
    regex_str = "^\s*%s(\s+\S+.*|\s+)?$" % prefix
    p = re.compile(regex_str, re.IGNORECASE)
    m = p.match(msg)
    if m:
        return True
    else:
        return False

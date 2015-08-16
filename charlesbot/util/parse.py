import re


def parse_msg_with_prefix(prefix, msg):
    regex_str = "^\s*%s[ :](.*)" % prefix
    p = re.compile(regex_str, re.IGNORECASE)
    m = p.match(msg)
    if m:
        return m.group(1).strip()
    else:
        return None


def does_msg_contain_prefix(prefix, msg):
    regex_str = "^\s*%s(\s+\S+.*|\s+)?$" % prefix
    p = re.compile(regex_str, re.IGNORECASE)
    m = p.match(msg)
    if m:
        return True
    else:
        return False

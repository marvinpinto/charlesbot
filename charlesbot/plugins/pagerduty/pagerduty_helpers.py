import asyncio
from charlesbot.util.http import http_get_auth_request
from charlesbot.slack.slack_attachment import SlackAttachment
import logging
import traceback
import json
from charlesbot.plugins.pagerduty.pagerduty_schedule import PagerdutySchedule
from charlesbot.plugins.pagerduty.pagerduty_user import PagerdutyUser
log = logging.getLogger(__name__)


@asyncio.coroutine
def get_pagerduty_schedules(token, subdomain):
    response = yield from http_get_auth_request(
        auth_string="token=%s" % token,
        url="https://%s.pagerduty.com/api/v1/schedules" % subdomain
    )
    schedules = []
    try:
        json_str = json.loads(response)
        for schedule in json_str['schedules']:
            pd_schedule = PagerdutySchedule()
            pd_schedule.load(schedule)
            schedules.append(pd_schedule)
    except (ValueError, KeyError, TypeError):
        log.error("Error parsing json response from pagerduty")
        log.error(traceback.format_exc())
    return schedules


@asyncio.coroutine
def get_oncall_users(token, subdomain, schedules, since, until):
    for schedule in schedules:

        # Move on to the next schedule if we don't have a schedule ID for
        # whatever reason
        if not schedule.id:
            log.error("Could not find a schedule ID for: %s" % schedule)
            continue

        payload = {
            "since": since,
            "until": until,
        }
        response = yield from http_get_auth_request(
            auth_string="token=%s" % token,
            url="https://%s.pagerduty.com/api/v1/schedules/%s/entries" % (subdomain, schedule.id),  # NOQA
            payload=payload
        )
        try:
            json_str = json.loads(response)
            for entry in json_str['entries']:
                pd_user = PagerdutyUser()
                pd_user.load(entry)
                schedule.oncall_users.append(pd_user)
        except (ValueError, KeyError, TypeError):
            log.error("Error parsing json response from pagerduty")
            log.error(traceback.format_exc())


@asyncio.coroutine
def send_oncall_response(slack_connection, schedules, channel_id):
    message = []
    for schedule in schedules:
        oncall_people = ", ".join(sorted(user.full_name for user in schedule.oncall_users))  # NOQA
        if not oncall_people:
            oncall_people = "could not determine who's on call :disappointed:"
        message.append("*%s* - %s" % (schedule.name, oncall_people))
    final_msg = "\n".join(message)
    attachment = SlackAttachment(color="#36a64f",
                                 fallback=final_msg,
                                 text=final_msg,
                                 mrkdwn_in=["text"])

    yield from slack_connection.api_call(
        'chat.postMessage',
        channel=channel_id,
        attachments=attachment,
        as_user=False,
        username="Currently On-Call",
        icon_url="https://slack.global.ssl.fastly.net/11699/img/services/pagerduty_48.png"  # NOQA
    )

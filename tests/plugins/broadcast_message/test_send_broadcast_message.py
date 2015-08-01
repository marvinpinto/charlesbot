import asynctest
from asynctest.mock import call
from asynctest.mock import patch
import json


class TestSendBroadcastMessage(asynctest.TestCase):

    def test_send_broadcast_message(self):
        with patch('charlesbot.plugins.broadcast_message.BroadcastMessage.__init__') as mock_init:  # NOQA
            from charlesbot.plugins.broadcast_message import BroadcastMessage
            mock_init.return_value = None
            slack_client = asynctest.MagicMock()
            with patch('charlesbot.plugins.broadcast_message.slack_rtm_api_call') as mock_slack:  # NOQA
                user = {"real_name": "bob", "thumb_24": "tumb"}
                attachment = [
                    {
                        "fallback": "Broadcast message from bob - message",
                        "author_name": "bob",
                        "author_icon": "tumb",
                        "text": "message",
                    }
                ]
                t_bm = BroadcastMessage(slack_client)
                t_bm.sc = slack_client

                # No rooms
                t_bm.room_membership = {}
                yield from t_bm.send_broadcast_message("message", user)
                self.assertEqual(mock_slack.call_args, None)
                mock_slack.reset_mock()

                # One room
                t_bm.room_membership = {"1234": "fun"}
                yield from t_bm.send_broadcast_message("message", user)
                expected_call = call(
                    slack_client,
                    'chat.postMessage',
                    channel="1234",
                    attachments=json.dumps(attachment),
                    as_user=False,
                    username="Broadcast Message",
                    icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2015-07-26/8217958308_48.png"  # NOQA
                )
                self.assertEqual(len(mock_slack.call_args_list), 1)
                self.assertEqual(mock_slack.call_args_list[0], expected_call)
                mock_slack.reset_mock()

                # Two rooms
                t_bm.room_membership = {"1234": "fun", "4567": "funner"}
                yield from t_bm.send_broadcast_message("message", user)
                expected_call_1 = call(
                    slack_client,
                    'chat.postMessage',
                    channel="1234",
                    attachments=json.dumps(attachment),
                    as_user=False,
                    username="Broadcast Message",
                    icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2015-07-26/8217958308_48.png"  # NOQA
                )
                expected_call_2 = call(
                    slack_client,
                    'chat.postMessage',
                    channel="4567",
                    attachments=json.dumps(attachment),
                    as_user=False,
                    username="Broadcast Message",
                    icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2015-07-26/8217958308_48.png"  # NOQA
                )
                self.assertEqual(len(mock_slack.call_args_list), 2)
                self.assertTrue(expected_call_1 in mock_slack.call_args_list)
                self.assertTrue(expected_call_2 in mock_slack.call_args_list)
                mock_slack.reset_mock()

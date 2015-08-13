import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from asynctest.mock import MagicMock
from charlesbot.slack.slack_attachment import SlackAttachment


class TestSendBroadcastMessage(asynctest.TestCase):

    def setUp(self):
        patcher = patch('charlesbot.plugins.broadcast_message.slack_rtm_api_call')  # NOQA
        self.addCleanup(patcher.stop)
        self.mock_slack_rtm = patcher.start()
        from charlesbot.plugins.broadcast_message import BroadcastMessage
        self.slack_client = MagicMock()
        self.bm = BroadcastMessage(self.slack_client)
        self.expected_attachment = SlackAttachment(
            fallback="Broadcast message from bob - message",
            author_name="bob",
            author_icon="tumb",
            text="message"
        )

    def test_in_no_rooms(self):
        self.mock_slack_rtm.reset_mock()
        user = {"real_name": "bob", "thumb_24": "tumb"}
        self.bm.room_membership = {}
        yield from self.bm.send_broadcast_message("message", user)
        self.assertEqual(self.mock_slack_rtm.call_args, None)

    def test_in_one_room(self):
        self.mock_slack_rtm.reset_mock()
        user = {"real_name": "bob", "thumb_24": "tumb"}
        self.bm.room_membership = {"1234": "fun"}
        yield from self.bm.send_broadcast_message("message", user)
        expected_call = call(
            self.slack_client,
            'chat.postMessage',
            channel="1234",
            attachments=self.expected_attachment,
            as_user=False,
            username="Broadcast Message",
            icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2015-07-26/8217958308_48.png"  # NOQA
        )
        self.assertEqual(len(self.mock_slack_rtm.call_args_list), 1)
        self.assertEqual(self.mock_slack_rtm.call_args_list[0], expected_call)

    def test_in_two_rooms(self):
        self.mock_slack_rtm.reset_mock()
        user = {"real_name": "bob", "thumb_24": "tumb"}
        self.bm.room_membership = {"1234": "fun", "4567": "funner"}
        yield from self.bm.send_broadcast_message("message", user)
        expected_call_1 = call(
            self.slack_client,
            'chat.postMessage',
            channel="1234",
            attachments=self.expected_attachment,
            as_user=False,
            username="Broadcast Message",
            icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2015-07-26/8217958308_48.png"  # NOQA
        )
        expected_call_2 = call(
            self.slack_client,
            'chat.postMessage',
            channel="4567",
            attachments=self.expected_attachment,
            as_user=False,
            username="Broadcast Message",
            icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2015-07-26/8217958308_48.png"  # NOQA
        )
        self.assertEqual(len(self.mock_slack_rtm.call_args_list), 2)
        self.assertTrue(expected_call_1 in self.mock_slack_rtm.call_args_list)
        self.assertTrue(expected_call_2 in self.mock_slack_rtm.call_args_list)

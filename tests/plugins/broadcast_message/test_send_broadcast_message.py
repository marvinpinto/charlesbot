import asynctest
from asynctest.mock import call
from asynctest.mock import patch
from charlesbot.slack.slack_attachment import SlackAttachment
from charlesbot.slack.slack_user import SlackUser


class TestSendBroadcastMessage(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot.plugins.broadcast_message.BroadcastMessage.seed_initial_data')  # NOQA
        self.addCleanup(patcher1.stop)
        self.mock_seed_initial_data = patcher1.start()

        patcher2 = patch('charlesbot.slack.slack_connection.SlackConnection.api_call')  # NOQA
        self.addCleanup(patcher2.stop)
        self.mock_api_call = patcher2.start()

        from charlesbot.plugins.broadcast_message import BroadcastMessage
        self.bm = BroadcastMessage()

        self.expected_attachment = SlackAttachment(
            fallback="Broadcast message from bob - message",
            author_name="bob",
            author_icon="tumb",
            text="message"
        )
        self.su = SlackUser(real_name="bob", image_24="tumb")

    def tearDown(self):
        self.bm.slack._drop()

    def test_in_no_rooms(self):
        self.bm.room_membership = {}
        yield from self.bm.send_broadcast_message("message", self.su)
        self.assertEqual(self.bm.slack.api_call.call_args, None)

    def test_in_one_room(self):
        self.bm.room_membership = {"1234": "fun"}
        yield from self.bm.send_broadcast_message("message", self.su)
        expected_call = call(
            'chat.postMessage',
            channel="1234",
            attachments=self.expected_attachment,
            as_user=False,
            username="Broadcast Message",
            icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2015-07-26/8217958308_48.png"  # NOQA
        )
        self.assertEqual(len(self.mock_api_call.call_args_list), 1)
        self.assertEqual(self.mock_api_call.call_args_list[0], expected_call)

    def test_in_two_rooms(self):
        self.bm.room_membership = {"1234": "fun", "4567": "funner"}
        yield from self.bm.send_broadcast_message("message", self.su)
        expected_call_1 = call(
            'chat.postMessage',
            channel="1234",
            attachments=self.expected_attachment,
            as_user=False,
            username="Broadcast Message",
            icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2015-07-26/8217958308_48.png"  # NOQA
        )
        expected_call_2 = call(
            'chat.postMessage',
            channel="4567",
            attachments=self.expected_attachment,
            as_user=False,
            username="Broadcast Message",
            icon_url="https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2015-07-26/8217958308_48.png"  # NOQA
        )
        self.assertEqual(len(self.mock_api_call.call_args_list), 2)
        self.assertTrue(expected_call_1 in self.mock_api_call.call_args_list)
        self.assertTrue(expected_call_2 in self.mock_api_call.call_args_list)

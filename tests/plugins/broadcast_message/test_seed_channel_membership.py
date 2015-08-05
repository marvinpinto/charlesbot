import asynctest
import json
from asynctest.mock import patch
from asynctest.mock import MagicMock


class TestSeedChannelMembership(asynctest.TestCase):

    def setUp(self):
        patcher = patch('charlesbot.plugins.broadcast_message.slack_rtm_api_call')  # NOQA
        self.addCleanup(patcher.stop)
        self.mock_slack_rtm = patcher.start()
        from charlesbot.plugins.broadcast_message import BroadcastMessage
        self.slack_client = MagicMock()
        self.bm = BroadcastMessage(self.slack_client)
        self.bm.seed_initial_data = MagicMock()

    def test_seed_channel_membership(self):
        channel_info = {
            "ok": True,
            "channels": [
                {
                    "id": "C024BE91L",
                    "name": "fun1",
                    "created": 1360782804,
                    "creator": "U024BE7LH",
                    "is_archived": False,
                    "is_general": False,
                    "is_member": True,
                    "num_members": 6,
                    "topic": {
                        "value": "Fun times",
                        "creator": "U024BE7LV",
                        "last_set": 1369677212
                    },
                    "purpose": {
                        "value": "This channel is for fun",
                        "creator": "U024BE7LH",
                        "last_set": 1360782804
                    }
                }
            ]
        }
        self.mock_slack_rtm.return_value = json.dumps(channel_info)
        yield from self.bm.seed_channel_membership()
        self.assertEqual(self.bm.room_membership, {'C024BE91L': 'fun1'})

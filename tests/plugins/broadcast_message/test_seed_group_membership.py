import asynctest
import json
from asynctest.mock import patch
from asynctest.mock import MagicMock


class TestSeedGroupMembership(asynctest.TestCase):

    def setUp(self):
        patcher = patch('charlesbot.plugins.broadcast_message.slack_rtm_api_call')  # NOQA
        self.addCleanup(patcher.stop)
        self.mock_slack_rtm = patcher.start()
        from charlesbot.plugins.broadcast_message import BroadcastMessage
        self.slack_client = MagicMock()
        self.bm = BroadcastMessage(self.slack_client)
        self.bm.seed_initial_data = MagicMock()

    def test_seed_channel_membership(self):
        group_info = {
            "ok": True,
            "groups": [
                {
                    "id": "G024BE91L",
                    "name": "secretplans",
                    "created": 1360782804,
                    "creator": "U024BE7LH",
                    "is_archived": False,
                    "members": [
                        "U024BE7LH"
                    ],
                    "topic": {
                        "value": "Secret plans on hold",
                        "creator": "U024BE7LV",
                        "last_set": 1369677212
                    },
                    "purpose": {
                        "value": "Discuss secret plans that no-one else should know",  # NOQA
                        "creator": "U024BE7LH",
                        "last_set": 1360782804
                    }
                }
            ]
        }
        self.mock_slack_rtm.return_value = json.dumps(group_info)
        yield from self.bm.seed_group_membership()
        self.assertEqual(self.bm.room_membership, {'G024BE91L': 'secretplans'})

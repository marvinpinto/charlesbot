import asynctest
import json
from asynctest.mock import patch


class TestSeedGroupMembership(asynctest.TestCase):

    def setUp(self):
        patcher1 = patch('charlesbot.plugins.broadcast_message.BroadcastMessage.seed_initial_data')  # NOQA
        self.addCleanup(patcher1.stop)
        self.mock_seed_initial_data = patcher1.start()

        patcher2 = patch('charlesbot.slack.slack_connection.SlackConnection.api_call')  # NOQA
        self.addCleanup(patcher2.stop)
        self.mock_api_call = patcher2.start()

        from charlesbot.plugins.broadcast_message import BroadcastMessage
        self.bm = BroadcastMessage()

    def tearDown(self):
        self.bm.slack._drop()

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
        self.mock_api_call.side_effect = [json.dumps(group_info)]
        yield from self.bm.seed_group_membership()
        self.assertEqual(self.bm.room_membership, {'G024BE91L': 'secretplans'})

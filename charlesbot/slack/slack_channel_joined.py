from charlesbot.slack.slack_room_joined import SlackRoomJoined


class SlackChannelJoined(SlackRoomJoined):

    properties = ['is_general',
                  'members',
                  'is_channel',
                  'is_archived',
                  'creator',
                  'id',
                  'is_member',
                  'name',
                  'type']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def compatibility_key(self):
        return "channel_joined"

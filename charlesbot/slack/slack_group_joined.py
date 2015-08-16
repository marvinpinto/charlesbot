from charlesbot.slack.slack_room_joined import SlackRoomJoined


class SlackGroupJoined(SlackRoomJoined):

    properties = ['members',
                  'is_group',
                  'is_archived',
                  'creator',
                  'id',
                  'name',
                  'type']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def compatibility_key(self):
        return "group_joined"

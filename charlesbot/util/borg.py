class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

    def _drop(self):
        "Drop the instance (for testing purposes)."
        self.__dict__ = {}

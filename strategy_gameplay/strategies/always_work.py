from .base import BaseStrategy

class AlwaysWork(BaseStrategy):
    def __init__(self):
        pass

    def get_action(self, state = None):
        return 'work'
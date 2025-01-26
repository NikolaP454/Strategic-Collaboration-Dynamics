from .base import BaseStrategy

class AlwaysLazy(BaseStrategy):
    def __init__(self):
        pass

    def get_action(self, state = None):
        return 'lazy'
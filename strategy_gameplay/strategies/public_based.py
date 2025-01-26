from .base import BaseStrategy
import numpy as np

class PublicBased(BaseStrategy):
    def __init__(self):
        pass

    def get_action(self, state = None):
        assert state is not None, "State cannot be None"
        
        # Get the public opinion of the state
        public_opinion = state['public_work_ethic']
        
        # Randomly choose between work and lazy
        action = np.random.choice(['work', 'lazy'], p=[public_opinion, 1 - public_opinion])
        
        return action
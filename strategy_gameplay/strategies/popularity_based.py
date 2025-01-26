from .base import BaseStrategy
import numpy as np

class PopularityBased(BaseStrategy):
    def __init__(self):
        pass

    def get_action(self, state = None):
        assert state is not None, "State cannot be None"
        
        # Get the popularity from the state
        popularity = state['popularity']
        
        # p = 1/(1+e^(-x/2))
        prob_work = 1/(1+np.exp(-(popularity)/2))
        prob_lazy = 1 - prob_work
        
        # Randomly choose between work and lazy
        action = np.random.choice(['work', 'lazy'], p=[prob_work, prob_lazy])
        
        return action
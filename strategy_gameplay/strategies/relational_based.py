from .base import BaseStrategy
import numpy as np

class RelationStrengthBased(BaseStrategy):
    def __init__(self):
        pass

    def get_action(self, state = None):
        assert state is not None, "State cannot be None"
        
        # Get the relation strength of the state
        relation_strength = state['relation_strength']
        
        # p = 1/(1+e^(-(x-2)/2))
        prob_work = 1/(1+np.exp(-(relation_strength-2)/2))
        prob_lazy = 1 - prob_work
        
        # Randomly choose between work and lazy
        action = np.random.choice(['work', 'lazy'], p=[prob_work, prob_lazy])
        
        return action
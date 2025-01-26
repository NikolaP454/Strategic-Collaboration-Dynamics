import numpy as np
from tqdm import tqdm

from .strategies import *

class AgentFactory:
    @staticmethod    
    def generate_single_agent(agent_type):
        agents = {
            'lazy': AlwaysLazy(),
            'workaholic': AlwaysWork(),
            'public_based': PublicBased(),
            'relation_based': RelationStrengthBased(),
            'popularity_based': PopularityBased(),
        }
        
        assert agent_type in agents, f"Agent type {agent_type} not found"
        
        return agents[agent_type]
    
    @staticmethod
    def generate_agents(agent_types, shuffle=True, seed=42):
        agents = [
            AgentFactory.generate_single_agent(agent_type)
            for agent_type in tqdm(agent_types)
        ]
        
        # Shuffle the agents
        if shuffle:
            np.random.seed(seed)
            np.random.shuffle(agents)
        
        return agents
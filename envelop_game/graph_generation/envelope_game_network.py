import numpy as np
from tqdm import tqdm

from .envelope_game import EnvelopeGame

"""
Strategy space for player 1:
1. Cooperate without looking (CWOL)
2. Cooperate with looking (CWL)
3. Cooperate if temptation is low (ONLYL)
4. Cooperate if temptation is high (ONLYH)
5. Look and defect
6. Defect without looking

Strategy space for player 2:
1. Always continue
2. Exit if player 1 looks
3. Exit if player 1 does not look
4. Always exit
"""

class EnvelopeGameNetwork:

    def __init__(self, N, G, T, p, a, cl, ch, b, d1, d2, lmbd, beta, mu=0):
        """
        Constructor for the simulation
        :param N: number of nodes (DEPRECATED)
        :param G: the network graph
        :param T: number of simulation iterations
        :param p: probability that the temptation is low
        :param a: cooperation gain for player1
        :param cl: defection gain for player1 if temptation is low
        :param ch: defection gain for player1 if temptation is high
        :param b: cooperation gain for player2
        :param d1: parameter for calculating the defection cost for player 2
        :param d2: parameter for calculating the defection cost for player 2
        :param lmbd: weight parameter for d1 and d2
        :param beta: strength of selection
        :param mu: mutation probability
        :return:
        """
        # Check if the constraints are satisfied
        self.check_parameters(d1, d2, lmbd, beta)
        
        # initialize parameters
        self.N = len(list(G.nodes))
        self.G = G
        self.T =  T
        self.p = p
        self.a = a
        self.cl = cl
        self.ch = ch
        self.b = b
        self.dl = lmbd*d1 + (1-lmbd)*d2
        self.dh = (1-lmbd)*d1 + lmbd*d2
        self.beta = beta
        self.mu = mu
        
        # Create the envelope game object and check constraints
        self.envelope_game = EnvelopeGame(self.p, self.a, self.cl, self.ch, self.b, self.dl, self.dh)
        
        # Generate the players with random strategies
        self.players = np.column_stack((np.random.randint(6, size=self.N), np.random.randint(4, size=self.N)))
        
        # Initialize looking, exit & cooperation frequency
        self.f_look = []
        self.f_exit = []
        self.f_coop = []

    def check_parameters(self, d1, d2, lmbd, beta):
        """
        Check whether the parameters satisfy the envelope game constraints
        :return:
        """
        constraints_desc = """Parameter s don't satisfy the constraints of the experimental environment!
        \nThe following errors have been found:"""
        error = False
        if lmbd < 0 or lmbd > 1:
            constraints_desc =+ "\nThe lambda parameter needs to be in the interval [0, 1]"
            error = True
        if d1 >= d2 or d1 >= 0 or d2 >= 0:
            constraints_desc += "\nParameters d1 and d2 must satisfy the following: d1 < d2 < 0"
            error = True
        if beta < 0:
            constraints_desc += "\nThe strength of selection (beta) must be nonnegative: beta >= 0"
            error = True
        if error:
            raise ValueError(constraints_desc)

    def perform_simulation(self):
        """
        Perform the required simulation.
        """
        
        for iteration in tqdm(range(self.T), desc="Simulation progress"):
            # choose random player and let him play with his neighbors
            player_i = np.random.randint(0, self.N)
            payoff_i = 0
            
            # see whether the player will play as player 1 or player 2
            role = np.random.choice([1, 2])
            
            # extract the neighbors of the player
            opponents = list(self.G.neighbors(player_i))
            
            # calculate the average payoff of the player
            for opponent in opponents:
                if role == 1:
                    payoff_i += self.envelope_game.play_game(self.players[player_i], self.players[opponent])[0]
                else:
                    payoff_i += self.envelope_game.play_game(self.players[opponent], self.players[player_i])[1]
                    
            average_payoff_i = payoff_i / len(opponents)
            
            # choose random neighbor and calculate his average payoff
            player_j = np.random.choice(opponents)
            payoff_j = 0
            
            opponents = list(self.G.neighbors(player_j))
            
            for opponent in opponents:
                if role == 1:
                    payoff_j += self.envelope_game.play_game(self.players[player_j], self.players[opponent])[0]
                else:
                    payoff_j += self.envelope_game.play_game(self.players[opponent], self.players[player_j])[1]
                    
            average_payoff_j = payoff_j / len(opponents)
            
            # allow player_i to change his strategy according to his model (player_j)
            
            change = np.random.binomial(1, 1/(1 + np.exp(-self.beta * (average_payoff_j - average_payoff_i))), 1)
            if change:
                if role == 1:
                    self.players[player_i][0] = self.players[player_j][0]
                else:
                    self.players[player_i][1] = self.players[player_j][1]
                    
            mutation = np.random.binomial(1, self.mu, 1)
            if mutation:
                if role == 1:
                    new_strategy = np.random.choice(range(6))
                    self.players[player_i][0] = new_strategy
                else:
                    new_strategy = np.random.choice(range(4))
                    self.players[player_i][1] = new_strategy
                    
            # log frequencies
            lookers = np.where((self.players[:, 0] != 0) & (self.players[:, 0] != 5))[0]
            look_prob = len(lookers)/self.N
            
            exit_prob = len(np.where((self.players[:, 1] == 3))[0]) / self.N + len(
                np.where((self.players[:, 1] == 1))[0]) / self.N * look_prob + len(
                np.where((self.players[:, 1] == 2))[0]) / self.N * (1 - look_prob)
                
            coop_prob = (len(np.where((self.players[:, 0] == 0) | (self.players[:, 0] == 1))[0]) / self.N + len(
                np.where((self.players[:, 0] == 2))[0]) / self.N * self.p + len(
                np.where((self.players[:, 0] == 4))[0]) / self.N * (1 - self.p))*(1-exit_prob)
            
            self.f_look.append(look_prob)
            self.f_exit.append(exit_prob)
            self.f_coop.append(coop_prob)

    def get_f_look(self):
        """
        Getter for the frequency of looking
        :return: the simulated looking frequency
        """
        return self.f_look

    def get_f_exit(self):
        """
        Getter for the frequency of exiting
        :return: the simulated exit frequency
        """
        return self.f_exit

    def get_f_coop(self):
        """
        Getter for the frequency of cooperation
        :return: the simulated cooperation frequency
        """
        return self.f_coop
import numpy as np

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

class EnvelopeGame:

    # Constructor
    def __init__(self, p, a, cl, ch, b, dl, dh):
        """
        Constructor for the EnvelopeGame class
        :param p: probability that the temptation is low
        :param a: cooperation gain for player1
        :param cl: defection gain for player1 if temptation is low
        :param ch: defection gain for player1 if temptation is high
        :param b: cooperation gain for player2
        :param dl: defection "gain" for player2 if temptation is low
        :param dh: defection "gain" for player2 if temptation is high
        :return:
        """
        self.check_parameters(p, a, cl, ch, b, dl, dh)
        self.p = p
        # payoff matrix for all possible strategy combinations
        self.payoffs = np.full((2, 6, 4, 2), [[[[a, b], [a, b], [0, 0], [0, 0]],\
                                          [[a, b], [0, 0], [a, b], [0, 0]],\
                                          [[a, b], [0, 0], [a, b], [0, 0]],\
                                          [[cl, dl], [0, 0], [cl, dl], [0, 0]],\
                                          [[cl, dl], [0, 0], [cl, dl], [0, 0]],\
                                          [[cl, dl], [cl, dl], [0, 0], [0, 0]]],\
                                         [[[a, b], [a, b], [0, 0], [0, 0]],\
                                          [[a, b], [0, 0], [a, b], [0, 0]],\
                                          [[ch, dh], [0, 0], [ch, dh], [0, 0]],\
                                          [[a, b], [0, 0], [a, b], [0, 0]],\
                                          [[ch, dh], [0, 0], [ch, dh], [0, 0]],\
                                          [[ch, dh], [ch, dh], [0, 0], [0, 0]]]])

    def check_parameters(self, p, a, cl, ch, b, dl, dh):
        """
        Check whether the parameters satisfy the envelope game constraints
        :return:
        """
        constraints_desc = """Parameter s don't satisfy the constraints of the one shot envelop game!
        \nThe following errors have been found:"""
        error = False
        if p<0 or p>1:
            constraints_desc +="\nParameter p needs to be a valid probability (in the interval [0.1])"
            error = True
        if a<= 0 or b <=0:
            constraints_desc +="\nBoth players need to have positive gain in case of cooperation: a > 0 and b > 0"
            error = True
        if a >= ch or a <= cl:
            constraints_desc +="\nPlayer 1 needs to think about whether he should defect: a > 0 and cl < a < ch"
            error = True
        if p*dl + (1-p)*dh >= 0:
            constraints_desc += "\nPlayer 2 needs to avoid players that are likely to defect: pdl + (1-p)dh < 0 < b"
            error = True
        if error:
            raise ValueError(constraints_desc)

    def play_game(self, player1, player2):
        """
        Play the Envelop Game with two playersand  update their gains
        :param player1: 1x4 numpy array representing player1's strategy, accumulated gain and number of games
        :param player2: 1x4 numpy array representing player2's strategy, accumulated gain and number of games
        :return: the payoffs of player 1 and player 2
        """
        is_low = np.random.binomial(1, self.p, 1)
        if is_low:
            payoff1 = self.payoffs[0][player1[0]][player2[1]][0]
            payoff2 = self.payoffs[0][player1[0]][player2[1]][1]
        else:
            payoff1 = self.payoffs[1][player1[0]][player2[1]][0]
            payoff2 = self.payoffs[1][player1[0]][player2[1]][1]
        return payoff1, payoff2
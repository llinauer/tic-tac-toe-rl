"""
player.py
Author: Lukas Linauer

Player module, keeps track of board configurations the player has seen,
chooses actions for a given board configuration and gives reward for won/lost games


------------------------------------
Reinforcement Learning parameters:

The player class has three important parameters:

epsilon: Chance of choosing a random action rather than the best
         e.g. if epsilon=0.4, the agent chooses a random action 40% of the time
         this helps the agent explore different actions which might lead to
         better outcomes in the future
         Epsilon is only relevant during the training, we don't want the agent to
         take random actions during a play against a human

learning_rate: influences how fast the values for certain board configurations are updated
               the learning rate should not be too high, e.g. values between 0.1 and 0.4
               have proven fruitful

decay_gamma: Also called discounting function
             Has a similar function as lr, a higher decay_gamma assigns higher values to
             board configurations that occur late during the game

You can experiment with those parameters and see if you can improve the agents performance

"""

import pickle
import numpy as np
from state import get_hash


class Player:
    """Player class"""

    def __init__(self, name, epsilon=0.4, vs_human=False):
        """init method"""

        self.name = name
        self.states = []  # states is a list of coordinate tuples (e.g. [(0,0), (0,2), ...]
        self.states_values = {}

        # RL parameters
        self.learning_rate = 0.3

        # when playing against a human, deactivate epsilon by setting it to -1
        if vs_human:
            self.epsilon = -1
        else:
            self.epsilon = epsilon
        self.decay_gamma = 0.9

    def reset(self):
        """Resets the player"""

        self.states = []

    def add_state(self, board_hash):
        """Adds the board_hash(string) to the list of states"""

        self.states.append(board_hash)

    def choose_action(self, positions, current_board, symbol):
        """Choose action for the player based on the available positions (list),
           the current_board (np.array)
           symbol is either 1 for player 1 or -1 for player 2
           return which action(tuple) should be taken"""

        # generate random number between (0,1), if number <= epsilon => explore
        if np.random.uniform(0, 1) <= self.epsilon:
            idx = np.random.choice(len(positions))
            action = positions[idx]

        # choose action that leads to the maximum value
        else:

            max_value = -999

            # loop over all available positions
            for position in positions:
                next_board = current_board.copy()
                next_board[position] = symbol
                next_board_hash = get_hash(next_board)

                # check if the next_board_state already has a value assigned
                value = self.states_values.get(next_board_hash)
                if not value:
                    value = 0

                if value >= max_value:
                    max_value = value
                    action = position

        return action


    def feed_reward(self, reward):
        """At the end of the game, the player gets a reward(int)
           Win -> Reward = 1, Loss -> Reward = -1, Draw -> Reward = 0.1
           All states that have been visited during the course of the game are
           in the states list. Update their values according to the formula
           V_new(state) = V_old(state) + self.learning_rate * [ gamma*V(next_state) - V_old(state) ] """

        # loop over all states
        for state in reversed(self.states):
            if not self.states_values.get(state):
                self.states_values[state] = 0

            # update the value of the state
            self.states_values[state] += self.learning_rate * \
                                         (self.decay_gamma * reward - self.states_values[state])
            reward = self.states_values[state]

    def save_policy(self):
        """Saves the states_values dict to a binary file with pickle"""

        with open('policy_' + str(self.name), 'wb') as policy_file:
            pickle.dump(self.states_values, policy_file)

    def load_policy(self):
        """Loads the states_values dict from a binary file with pickle"""

        with open('policy_' + str(self.name), 'rb') as policy_file:
            self.states_values = pickle.load(policy_file)

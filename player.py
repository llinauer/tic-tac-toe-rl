import numpy as np
from state import get_hash
import pickle


class Player:

    def __init__(self, name, epsilon=0.4):
        self.name = name
        self.states = [] #states is a list of coordinate tuples (e.g. [(0,0), (0,2), ...]
        self.lr = 0.3
        self.epsilon = epsilon
        self.decay_gamma = 0.9
        self.states_values = {}
        
    def reset(self):
        '''Resets the player'''
        self.states = []
        
    def add_state(self, board_hash):
        self.states.append(board_hash)
        
    def choose_action(self, positions, current_board, symbol):
        '''Choose action for the player based on the available positions (list),
           the current_board (np.array)
           symbol is either 1 for player 1 or -1 for player 2
           return which action(tuple) should be taken'''
           

        #generate random number between (0,1), if < epsilon => explore
        if np.random.uniform(0, 1) <= self.epsilon:
            idx = np.random.choice(len(positions))
            action = positions[idx]
        
        #greedy action
        else:

            max_value = -999
            
            #loop over all available positions
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_board_hash = get_hash(next_board)
                
                #check if the next_board_state already has a value assigned
                value = self.states_values.get(next_board_hash)
                if not value:
                    value = 0
                
                if value >= max_value:
                    max_value = value
                    action = p
                    
        return action
        
        
        
    def feed_reward(self, reward):
        ''' '''
        #loop over all states
        for st in reversed(self.states):
            if not self.states_values.get(st):
                self.states_values[st] = 0
                
            self.states_values[st] += self.lr * (self.decay_gamma * reward - self.states_values[st])
            reward = self.states_values[st]

    def save_policy(self):
        '''Saves the states_values dict'''
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_values, fw)
        fw.close()

    def load_policy(self):
        file_name = 'policy_' + str(self.name)
        fr = open(file_name, 'rb')
        self.states_values = pickle.load(fr)
        fr.close()

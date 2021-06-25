"""
state.py
Author: Lukas Linauer

Keeps track of board states

"""

import numpy as np

# 3x3 board
BOARD_ROWS = 3
BOARD_COLS = 3


def get_hash(board):
    """Returns hash of current board configuration"""

    return str(board.reshape(BOARD_COLS*BOARD_ROWS))


class State:
    """State class"""

    def __init__(self, p1, p2):
        """init method"""

        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.p1 = p1
        self.p2 = p2
        self.is_end = False

        # init p1 plays first
        self.player_symbol = 1

    def reset(self):
        """Resets the board"""

        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.is_end = False

        # init p1 plays first
        self.player_symbol = 1

    def get_available_positions(self):
        """Return positions with no X or O in them"""

        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions

    def update_state(self, position):
        """Update the board with position (tuple(i,j))"""

        self.board[position] = self.player_symbol
        # switch to other player
        self.player_symbol = -1 if self.player_symbol == 1 else 1

    def check_win(self):
        """
        Checks the board if a a player has won
        Return 1 if player 1 won, -1 if player 2 won, 2 in case of draw
        """

        # check rows
        for i in range(BOARD_ROWS):
            if sum(self.board[i, :]) == 3:
                self.is_end = True
                return 1
            elif sum(self.board[i, :]) == -3:
                self.is_end = True
                return -1

        # check cols
        for i in range(BOARD_COLS):
            if sum(self.board[:, i]) == 3:
                self.is_end = True
                return 1
            elif sum(self.board[:, i]) == -3:
                self.is_end = True
                return -1

        # check diagonals
        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
        diag_sum2 = sum([self.board[i, BOARD_COLS - i - 1] for i in range(BOARD_COLS)])

        if diag_sum1 == 3 or diag_sum2 == 3:
            self.is_end = True
            return 1
        if diag_sum1 == -3 or diag_sum2 == -3:
            self.is_end = True
            return -1

        # check for draw
        if len(self.get_available_positions()) == 0:
            self.is_end = True
            return 2

        return None

    def give_reward(self, win_result):
        """If a player has won, give 1 as a reward.
           In case of a loss, give -1.
           In case of draw every player gets 0.1"""

        if win_result == 1:
            self.p1.feed_reward(1)
            self.p2.feed_reward(-1)
        elif win_result == -1:
            self.p1.feed_reward(-1)
            self.p2.feed_reward(1)
        elif win_result == 2:
            self.p1.feed_reward(0.1)
            self.p2.feed_reward(0.1)

"""
tic_tac_toe.py
Author: Lukas Linauer

Main module, parses command line arguments and sets up game

"""

import argparse
from game import Game


def main():
    """Main function"""

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', help='Do training of RL agent', action='store_true')
    parser.add_argument('--play', help='Play vs. the computer', action='store_true')
    parser.add_argument('-n', help='Number of rounds for training', dest='n_rounds')
    args = parser.parse_args()

    if args.train:
        tic_tac_toe_game = Game()
        try:
            n_rounds = int(args.n_rounds)  # cast n into an int
        except ValueError:
            print('Invalid value for n')
            return False
        except TypeError:
            n_rounds = 100  # default to 100 rounds
        tic_tac_toe_game.computer_vs_computer(n_rounds)

    elif args.play:
        # initialize new game
        tic_tac_toe_game = Game(vs_human=True)
        tic_tac_toe_game.player_vs_computer()


if __name__ == '__main__':
    main()

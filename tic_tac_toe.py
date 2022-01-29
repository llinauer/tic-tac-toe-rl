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
    parser = argparse.ArgumentParser(description='Train an Reinforcement Learning agent in Tic '
                                                 'Tac Toe and play against it')
    parser.add_argument('-a', '--action', choices=['train', 'play'],
                        help='Train the agent or play against it', type=str)
    parser.add_argument('-n', help='Number of rounds for training (Default: 100)', dest='n_rounds',
                        default=100)
    args = parser.parse_args()


    # check if an action was given
    if 'action' not in args:
        print('Please provide a valid action. Valid actions are: train, play')
        return

    if args.action == 'train':
        tic_tac_toe_game = Game()
        try:
            n_rounds = int(args.n_rounds)
        except ValueError:
            print('Invalid value for n')
            return
        tic_tac_toe_game.computer_vs_computer(n_rounds)

    elif args.action == 'play':
        # initialize new game
        tic_tac_toe_game = Game(vs_human=True)
        tic_tac_toe_game.player_vs_computer()


if __name__ == '__main__':
    main()

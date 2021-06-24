import argparse
from game import Game


def main():
    '''Main function'''

    
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', help='Do training of RL agent', action='store_true')
    parser.add_argument('--play', help='Play vs. the computer', action='store_true')
    parser.add_argument('-n', help='Number of rounds for training', dest='n_rounds')
    args = parser.parse_args()


    if args.train:
        tic_tac_toe_game = Game()
        if args.n_rounds:
            tic_tac_toe_game.computer_vs_computer(int(args.n_rounds))
        else:
            tic_tac_toe_game.computer_vs_computer()
        return True
        
    elif args.play:    
        # initialize new game
        tic_tac_toe_game = Game(vs_human=True)
        tic_tac_toe_game.player_vs_computer()
    
    
if __name__ == '__main__':
    main()    

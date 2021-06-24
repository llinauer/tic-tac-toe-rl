import numpy as np
import tkinter
from state import State, get_hash
from player import Player

BOARD_ROWS = 3
BOARD_COLS = 3


class Game:

    def __init__(self, vs_human=False):
        """init method"""
        if vs_human:
            epsilon = -1
        else:
            epsilon = 0.4
        self.player1 = Player('X')
        self.player2 = Player('O', epsilon=epsilon)
        self.state = State(self.player1, self.player2)
        


    def player_vs_computer(self):
        """Gets called on start of the game"""
        
        #init window 
        
        self.game_fields = np.zeros((BOARD_ROWS, BOARD_COLS)).tolist()
        self.window = tkinter.Tk()
        self.window.title("Tic Tac Toe")

        #init player
        # Human = Player 1
        # Computer = Player 2
        self.player2.load_policy()


        #initialize Fields
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.game_fields[i][j] = tkinter.Button(text='', font=('normal', 60, 'normal'),
                                                  width=5, height=3,
                                                  command=lambda r=i, c=j: self.field_clicked(r, c))
                self.game_fields[i][j].grid(row=i, column=j)

        
        self.announce_label = tkinter.Label(text = "It's X's turn", font = ("Arial", 20))
        self.announce_label.grid(row=3,column=1)
 
        
        self.exit_button = tkinter.Button(self.window, text="Exit", font=("Arial", 20),
                                          fg = "black", command=self.window.quit)
        self.exit_button.grid(row=3,column=3)
        
        self.window.mainloop()
        return None
        
        
        
    def computer_vs_computer(self, rounds=100):
        '''Computer plays against itself for rounds(int)'''
        
        for i in range(rounds):

            while not self.state.is_end:
            
                #Player 1 turn

                available_positions = self.state.get_available_positions()
                p1_action = self.player1.choose_action(available_positions,
                                                       self.state.board, self.state.player_symbol)
                self.state.update_state(p1_action)
                board_hash = get_hash(self.state.board)
                self.player1.add_state(board_hash)

                win_int = self.state.check_win()
                if win_int:
                    self.state.give_reward(win_int)
                    self.player1.reset()
                    self.player2.reset()
                    self.state.reset()
                    break
                

                #Player 2 turn
                available_positions = self.state.get_available_positions()


                p2_action = self.player2.choose_action(available_positions,
                                                       self.state.board,
                                                       self.state.player_symbol)
                self.state.update_state(p2_action)
                board_hash = get_hash(self.state.board)
                self.player2.add_state(board_hash)

                win_int = self.state.check_win()
                if win_int:
                    self.state.give_reward(win_int)
                    self.player1.reset()
                    self.player2.reset()
                    self.state.reset()
                    break
                
        # save the learned values from each player
        self.player1.save_policy()
        self.player2.save_policy()


    def field_clicked(self, row, col):
        """Gets called when one of the fields is clicked.
           Input: Number of button clicked.
           Returns: 
        """
        if self.state.is_end:
            return

        #check if the chosen field is still available and if yes, update state
        if not (row, col) in self.state.get_available_positions():
            return None
            
        #print X or O 
        if self.state.player_symbol == 1:
            self.game_fields[row][col].config(text=self.player1.name)
            self.announce_label.config(text="It's " + self.player2.name + "s turn")
        else:
            self.game_fields[row][col].config(text=self.player2.name)
            self.announce_label.config(text="It's " + self.player1.name + "s turn")
        self.state.update_state((row, col))
        
        #check for win/draw
        win_int = self.state.check_win()
        
        if win_int == 1:
            self.announce_label.config(text="Player " + self.player1.name + " won!")
            return None
        elif win_int == -1:
            self.announce_label.config(text="Player " + self.player2.name + " won!")
            return None
        elif win_int == 2:
            self.announce_label.config(text="Draw!")
            return None
            
        #computer makes turn
        self.computer_turn()

  
            
    def end_game(self):
        """
        If one player has won, set all board_states to 1
        """
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.board_states[i][j] = 1
        
        
    def computer_turn(self):
        """
        Agent makes a turn
        """
        player_symbol = self.state.player_symbol
        available_positions = self.state.get_available_positions()
        if player_symbol == 1:
            action = self.player1.choose_action(available_positions,
                                                self.state.board, player_symbol)
        else:
            action = self.player2.choose_action(available_positions,
                                                self.state.board, player_symbol)    
                                                
        #print X or O 
        if player_symbol == 1:
            self.game_fields[action[0]][action[1]].config(text=self.player1.name)
            self.announce_label.config(text="It's " + self.player2.name + "s turn")
        else:
            self.game_fields[action[0]][action[1]].config(text=self.player2.name)
            self.announce_label.config(text="It's " + self.player1.name + "s turn")
                                                   
        self.state.update_state(action)        
        
        
        #check for win/draw
        win_int = self.state.check_win()
        
        if win_int == 1:
            self.announce_label.config(text="Player " + self.player1.name + " won!")
            return None
        elif win_int == -1:
            self.announce_label.config(text="Player " + self.player2.name + " won!")
            return None
        elif win_int == 2:
            self.announce_label.config(text="Draw!")
            return None


  
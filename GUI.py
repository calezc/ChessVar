import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import json
from ChessVar import *

class GUI:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("ChessVar")
        self._game = ChessVar()
        self._game_board_instance = self._game.get_game_board().get_board_state()

        # Menu Bar
        self._menu_bar = tk.Menu(self._root)
        self._root.config(menu=self._menu_bar)

        # File Menu
        self._file_menu = tk.Menu(self._menu_bar, tearoff=0)
        self._file_menu.add_command(label="New Game", command=self.new_game)
        self._file_menu.add_command(label="Load Game", command=self.load_game)
        self._file_menu.add_command(label="Save Game", command=self.save_game)
        self._file_menu.add_separator()
        self._file_menu.add_command(label="Close", command=self._root.destroy)
        self._menu_bar.add_cascade(label="Menu", menu=self._file_menu)

        # Main Frame
        self._main_frame = tk.Frame(self._root)
        self._main_frame.grid(row=0, column=0, padx=10, pady=10)

        # Initialize game board GUI.
        self.setup_board_GUI(False)

        # Monitor mouse clicks
        self._selected_spaces = [None] * 2
        self._background_holder = None

        self._root.mainloop()

    def new_game(self):
        """
        Initializes a new game.  Re-initializes game (data member) to a new instance
        of ChessVar(), and re-initializes the GUI game board to reflect all pieces
        in their starting positions.
        """

        self._game = ChessVar()
        self.setup_board_GUI(True)

    def load_game(self):
        """
        Loads previously saved game state and updates game board.
        """

        # Prompt for saved game file to load and load file.
        file_path = filedialog.askopenfilename(title="Load Game", filetypes=[("CHV", "*.chv")])
        with open(file_path, "r") as infile:
            game_state = json.load(infile)

        # Initialize new game.
        self._game = ChessVar()

        # Update turn variable to state saved in saved game file.
        self._game.set_turn(game_state[0])

        # Update piece and board position data to match data in saved game file.
        updated_board_positions = []
        piece_list = self._game.get_player_list()[0].get_piece_list()
        new_piece_list_index = 0
        saved_piece_index = 0
        while new_piece_list_index < len(piece_list):
            if piece_list[new_piece_list_index].get_type() == game_state[1][saved_piece_index][0]:
                board_position = self._game.get_game_board().get_board_position(game_state[1][saved_piece_index][1])
                piece_list[new_piece_list_index].set_position(board_position)
                board_position.set_piece(piece_list[new_piece_list_index])
                updated_board_positions.append(game_state[1][saved_piece_index][1])
                new_piece_list_index += 1
                saved_piece_index += 1
            else:
                del piece_list[new_piece_list_index]

        piece_list = self._game.get_player_list()[1].get_piece_list()
        new_piece_list_index = 0
        saved_piece_index = 0
        while new_piece_list_index < len(piece_list):
            if piece_list[new_piece_list_index].get_type() == game_state[2][saved_piece_index][0]:
                board_position = self._game.get_game_board().get_board_position(game_state[2][saved_piece_index][1])
                piece_list[new_piece_list_index].set_position(board_position)
                board_position.set_piece(piece_list[new_piece_list_index])
                updated_board_positions.append(game_state[2][saved_piece_index][1])
                new_piece_list_index += 1
                saved_piece_index += 1
            else:
                del piece_list[new_piece_list_index]

        board = self._game.get_game_board().get_board_state()
        for position in board:
            if position not in updated_board_positions:
                board[position].set_piece(None)

        # Reset game board with saved board position data.
        self.setup_board_GUI(True)

    def save_game(self):
        """
        Method that saves current game state.
        """

        # If game is over, prompts to start new game.
        if self._game.get_game_state() != "UNFINISHED":
            if self._game.get_game_state() == "WHITE_WON":
                winner = "White"
            else:
                winner = "Black"
            response = messagebox.askyesnocancel(title="Game Over",
                                                 message=f"The game is over.  {winner} won! Start a new game?")
            if response is None:
                pass
            elif response:
                self.new_game()
            else:
                self._root.destroy()

        # If game is not over, saves turn, piece, and position data to file.
        else:
            turn = self._game.get_turn().get_color()
            piece_list = self._game.get_player_list()[0].get_piece_list()
            piece_list_white = []
            for piece in piece_list:
                piece_tuple = piece.get_type(), piece.get_position().get_string()
                piece_list_white.append(piece_tuple)
            piece_list = self._game.get_player_list()[1].get_piece_list()
            piece_list_black = []
            for piece in piece_list:
                piece_tuple = piece.get_type(), piece.get_position().get_string()
                piece_list_black.append(piece_tuple)
            game_state = (turn, piece_list_white, piece_list_black)

            # Prompt for file save location and save.
            file_path = filedialog.asksaveasfilename(title="Save Game", defaultextension=".chv",
                                                     filetypes=[("CHV", "*.chv")])
            with open(file_path, "w") as outfile:
                json.dump(game_state, outfile)



    def setup_board_GUI(self, reset=False):
        """
        Initializes a new game board.

        :param reset:   Boolean (True/False).  Indicates whether this is the initial board setup
                        for the game or a reset of the board (e.g., upon selecting "New Game" or "Load Game").
        """

        self._game_board_instance = self._game.get_game_board().get_board_state()

        # Fill 10x10 matrix with preliminary values.
        self._temp_grid_labels = [None] * 10
        self._temp_grid_labels[0] = ["", "1", "2", "3", "4", "5", "6", "7", "8", ""]
        self._temp_grid_labels[1] = ["a", "", "", "", "", "", "", "", "", "a"]
        self._temp_grid_labels[2] = ["b", "", "", "", "", "", "", "", "", "b"]
        self._temp_grid_labels[3] = ["c", "", "", "", "", "", "", "", "", "c"]
        self._temp_grid_labels[4] = ["d", "", "", "", "", "", "", "", "", "d"]
        self._temp_grid_labels[5] = ["e", "", "", "", "", "", "", "", "", "e"]
        self._temp_grid_labels[6] = ["f", "", "", "", "", "", "", "", "", "f"]
        self._temp_grid_labels[7] = ["g", "", "", "", "", "", "", "", "", "g"]
        self._temp_grid_labels[8] = ["h", "", "", "", "", "", "", "", "", "h"]
        self._temp_grid_labels[9] = ["", "1", "2", "3", "4", "5", "6", "7", "8", ""]

        # Update matrix with abbreviated strings to represent each piece in starting positions
        for key in self._game_board_instance:
            index_list = self.index_converter(key)
            piece = self._game_board_instance[key].get_piece()
            if piece:
                owner = piece.get_owner()
                self._temp_grid_labels[index_list[0]][index_list[1]] = self.piece_display_string(piece, owner)

        # If initial game board setup, create a label widget for each grid space.
        if not reset:
            # 10x10 matrix to represent spaces and labels on the game board
            self._grid_labels = [None] * 10
            for i in range (10):
                self._grid_labels[i] = self._temp_grid_labels[i]

            # Create and arrange labels for 10x10 game board within Main Frame,
            # populate with values from grid_labels matrix, and update grid_labels
            # matrix such that values are the TK labels (rather than just strings).
            for i in range(10):
                for j in range(10):
                    label = tk.Label(self._main_frame, text=self._temp_grid_labels[j][i], borderwidth=1, relief="solid", width=5,
                                     height=2)
                    self._grid_labels[j][i] = label
                    label.grid(row=9 - i, column=j)

                    # Define handler for left-mouse click
                    label.bind("<Button-1>", self.mouse_click)

                    # Define color of spaces in grid
                    if j != 0 and j != 9 and i != 0 and i != 9:
                        if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                            label.configure(background="gray")
                        else:
                            label.configure(background="white")
                    else:
                        label.configure(background="light gray")

        # If resetting game board after initial setup, just update text associated
        # with each label.
        else:
            for i in range(10):
                for j in range(10):
                    self._grid_labels[j][i].configure(text=self._temp_grid_labels[j][i])

    def index_converter(self, board_position_string):
         """
         Converts the string representation of a board position into a list of 2 integer values
         representing the indices of the associated board position string in the matrix of values
         displayed in the GUI.

         :param board_position_string: String representation of a given board position.
         :return: List of 2 integers representing the indices in the GUI matrix.
         """

         index_list = [None] * 2
         index_list[0] = ord(board_position_string[0]) - 96
         index_list[1] = int(board_position_string[1])

         return index_list

    def piece_display_string(self, piece, owner):
        """
        Accepts a piece sub-type object and its owner and
        returns a string to display on the GUI game board.

        :param piece: A piece sub-type object
        :param owner: The Player object that owns the given piece
        :return: A string representing the piece and owner, to display on the
                GUI game board.
        """

        return piece.get_type_abrv() + "(" + owner.get_color()[0] + ")"

    def label_to_position_string(self, label):
        """
        Converts the numerical portion of the board position label widget name
        into the equivalent board position string representation.
        """

        position_string = chr(int(label[1]) + 95) + label[0]

        return position_string

    def mouse_click(self, event):
        """
        Handler function for mouse clicks on the game board.

        :param event: A left-button mouse click event.
        """

        # Filter mouse clicks that are not within active game board (i.e., the row/column labels)
        if len(str(event.widget)) == 16 and str(event.widget)[14] != "9" and str(event.widget)[15] != "1" and str(event.widget)[15] != "0":
            # If selection is the first (of 2) selected spaces, record space and change color to green.
            if self._selected_spaces[0] is None:
                self._selected_spaces[0] = event.widget
                self._background_holder = event.widget["background"]
                self._selected_spaces[0].configure(background="green")
            # If selection is the second (of 2) selecte spaces, revert background color of first selected
            # space to original color and attempt move.  If move is invalid, trigger popup notification
            # stating error.  If move is valid, update board position labels (and other relevant variables).
            else:
                self._selected_spaces[1] = event.widget
                self._selected_spaces[0].configure(background=self._background_holder)
                start_pos = self.label_to_position_string(str(self._selected_spaces[0])[14:16])
                end_pos = self.label_to_position_string(str(self._selected_spaces[1])[14:16])
                try:
                    move = self._game.make_move(start_pos, end_pos)
                except GameOverError:
                    if self._game.get_game_state() == "WHITE_WON":
                        winner = "White"
                    else:
                        winner = "Black"
                    response = messagebox.askyesnocancel(title="Game Over",
                                              message=f"The game is over.  {winner} won! Start a new game?")
                    if response is None:
                        pass
                    elif response:
                        self.new_game()
                    else:
                        self._root.destroy()
                except MoveOutOfTurnError:
                    if self._game.get_turn().get_color() == "White":
                        turn = "White"
                    else:
                        turn = "Black"
                    messagebox.askokcancel(title="Move Out of Turn", message=f"{turn}'s move. Please try again.")
                except IllegalMoveError:
                    messagebox.askokcancel(title="Illegal Move", message="Please try again.")
                else:
                    temp_text = self._selected_spaces[0]["text"]
                    self._selected_spaces[0].configure(text="")
                    self._selected_spaces[1].configure(text=temp_text)

                # Reset variables
                self._background_holder = None
                self._selected_spaces[0] = None
                self._selected_spaces[1] = None

if __name__ == "__main__":
    game = GUI()

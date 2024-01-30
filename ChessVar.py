
class GameOverError(Exception):
    """
    Exception thrown if move attempted when current game has already ended.
    """
    pass

class MoveOutOfTurnError(Exception):
    """
    Exception thrown if move attempted out of turn.
    """
    pass

class IllegalMoveError(Exception):
    """
    Exception thrown if attempted move is illegal.
    """
    pass

class ChessVar:
    """
    Defines a ChessVar object, which represents an instance of a ChessVar game. This class
    is intended (i) to instantiate the game board, the pieces, and the players, (ii) to manage the overall
    flow of the game, including piece moves and board state, and (iii) to track when the game is ultimately
    won/lost.

    Includes the following data members:
        - game_board - This is an instance of a Board (class) object
        - game_state - This is a string object representing the current state of the game (i.e.,
                        "UNFINISHED", "WHITE_WON", or "BLACK_WON"
        - player_list - This is a list containing two objects of the class Player, one representing the white Player
                        and the other representing the black Player.
        - turn - This is assigned one of the two Player objects in the player_list, representing the Player whose
                    turn it is.

    Includes the following methods (excluding __init__):
        - get_game_state() - Returns the value of game_state (data member)
        - get_turn() - Returns the value of turn (data member)
        - make_move() - Communicates with (i) the game_board object to obtain the piece subtype object currently
                        on the relevant space, and (ii) the piece subtype object on that space (a) to confirm the owner
                        of that piece is the player whose turn it is, (b) to confirm that the requested move is legal,
                        and (c) to execute the move (and any associated captures)

    PARAMETERS: None
    RETURN: None
    """

    def __init__(self):
        """
        Initializes a ChessVar object with (i) game_board assigned to a new Board object, (ii) game_state set to
        "UNFINISHED", (iii) player_list initialized with two new Player objects, and (iv) turn set to the white Player
        object.
        """

        self._game_board = Board()
        self._game_state = "UNFINISHED"
        self._player_list = [Player("White", self._game_board), Player("Black", self._game_board)]
        self._turn = self._player_list[0]

    def get_game_board(self):
        """
        Returns value of game_board (data member).
        """

        return self._game_board

    def get_game_state(self):
        """
        Returns the value of game_state (data member).
        """

        return self._game_state

    def get_player_list(self):
        """
        Returns the value of player_list (data member).
        """

        return self._player_list

    def get_turn(self):
        """
        Returns the value of turn (data member).
        """

        return self._turn

    def set_turn(self, turn):
        """
        Sets the value of turn (data member).

        :param turn:    The string representation of the Player that is being set as the current turn holder.
        """

        if turn == "White":
            self._turn = self._player_list[0]
        else:
            self._turn = self._player_list[1]

    def make_move(self, string1, string2):
        """
        Method that executes a move from one board position to another board position.
        PARAMETERS:
            - string1 - Starting board position
            - string2 - Ending board position
        RETURNS:
            - Illegal / invalid move --> Returns False
            - Legal move / no capture --> Returns True
            - Legal move / capture --> Returns piece subtype object of captured piece
        """

        current_piece = None
        current_player = None
        current_move = None

        # Test if game is already over.
        if self._game_state == "WHITE_WON" or self._game_state == "BLACK_WON":
            raise GameOverError

        # Test if string arguments for starting and ending board positions are outside game board.
        if string1[0] < "a" or string1[0] > "h" or string2[0] < "a" or string2[0] > "h" or \
                string1[1] < "1" or string1[1] > "8" or string2[1] < "1" or string2[1] > "8":
            raise IllegalMoveError

        # Test if there is a piece located on the board position passed as the starting board position.
        current_piece = self._game_board.get_position_state(string1)
        if current_piece is None:
            raise IllegalMoveError

        # Test if owner of piece on starting board position has the current turn.
        current_player = current_piece.get_owner()
        if current_player != self._turn:
            raise MoveOutOfTurnError

        current_move = current_piece.move(self._game_board.get_board_position(string2), self._game_board)

        # Test whether move() returned a piece subtype object.  If so, a piece has been captured.
        if issubclass(current_move.__class__, Piece):
            # Re-initialize variables
            captured_type = None
            captured_player_pieces = None
            last_piece = True

            # Test if captured piece was the last of that piece type in play for its owner. If so, game over.
            captured_type = current_move.get_type()
            captured_player_pieces = current_move.get_owner().get_piece_list()
            for piece in captured_player_pieces:
                if captured_type == piece.get_type():
                    last_piece = False
            if last_piece is True:
                if self._turn == self._player_list[0]:
                    self._game_state = "WHITE_WON"
                else:
                    self._game_state = "BLACK_WON"
            if self._turn == self._player_list[0]:
                self._turn = self._player_list[1]
            else:
                self._turn = self._player_list[0]
            return True

        # If no capture, but move was otherwise legal.
        elif current_move is True:
            if self._turn == self._player_list[0]:
                self._turn = self._player_list[1]
            else:
                self._turn = self._player_list[0]
            return True

        # If move was illegal.
        else:
            raise IllegalMoveError

    def print_game_board(self):
        """
        Method that prints the game board to the console.
        """

        row_label_list = ["    ", "  a ", "  b ", "  c ", "  d ", "  e ", "  f ", "  g ", "  h ", "    "]
        temp_row_list = []
        row_counter = 8
        column_counter = 0
        temp_position_string = ""
        temp_piece = None
        temp_piece_owner = None
        temp_piece_type = None
        temp_status_string = None
        print(row_label_list)
        while row_counter > 0:
            while column_counter < 10:
                if column_counter == 0 or column_counter == 9:
                    temp_row_list.append("  " + str(row_counter) + " ")
                else:
                    temp_position_string = row_label_list[column_counter][2] + str(row_counter)
                    temp_piece = self._game_board.get_position_state(temp_position_string)
                    if temp_piece is None:
                        temp_status_string = "____"
                    elif temp_piece.get_type() == "Knight":
                        temp_piece_owner = temp_piece.get_owner().get_color()
                        temp_status_string = " KN" + temp_piece_owner[0]
                    else:
                        temp_piece_owner = temp_piece.get_owner().get_color()
                        temp_piece_type = temp_piece.get_type()
                        temp_status_string = " " + temp_piece_type[0] + temp_piece_owner[0] + " "
                    temp_row_list.append(temp_status_string)
                column_counter += 1
            print(temp_row_list)
            temp_row_list = []
            column_counter = 0
            row_counter -= 1
        print(row_label_list)
        print("\n")


class Player:
    """
    Defines a Player object, which represents the white or black player in a game of ChessVar. This class
    is intended (i) to instantiate a player and a list of its associated pieces, and (ii) to manage the list of
    active pieces for the given player.

    Includes the following data members:
        - color - This is a string set to either "White" or "Black"
        - piece_list - This is a list containing all of the piece subtype objects associated with the Player that
                        are still active on the board.
        - game_board - The Board object that is the game board for this instance of ChessVar

    Includes the following methods (excluding __init__):
        - get_color() - Returns the value of color (data member)
        - get_piece_list() - Returns piece_list (data member)
        - set_piece_list() - Modifies piece_list (data member) to remove a piece subtype object.  This method is invoked
                                by a piece subtype object (through its owner data member, which is a player object) when
                                a piece has been captured.  The piece subtype object that has been captured is passed as
                                a parameter and removed from the piece_list.

    PARAMETERS:
        - color - "White" or "Black"
        - game_board - The Board object that is the game board for this instance of ChessVar
    RETURN: None
    """

    def __init__(self, color, game_board):
        """
        Initializes a Player object with (i) color (data member) initialized to color (parameter), and (ii) piece_list
        initialized with a full collection of new piece subtype objects.  Also updates each Board Position object's
        piece (data member) using its set_piece() method to assign the relevant piece subtype object to that
        Board Position object.
        """

        self._color = color
        if color == "White":
            self._piece_list = [Pawn(self, game_board.get_board_position("a2")),
                                Pawn(self, game_board.get_board_position("b2")),
                                Pawn(self, game_board.get_board_position("c2")),
                                Pawn(self, game_board.get_board_position("d2")),
                                Pawn(self, game_board.get_board_position("e2")),
                                Pawn(self, game_board.get_board_position("f2")),
                                Pawn(self, game_board.get_board_position("g2")),
                                Pawn(self, game_board.get_board_position("h2")),
                                Rook(self, game_board.get_board_position("a1")),
                                Rook(self, game_board.get_board_position("h1")),
                                Knight(self, game_board.get_board_position("b1")),
                                Knight(self, game_board.get_board_position("g1")),
                                Bishop(self, game_board.get_board_position("c1")),
                                Bishop(self, game_board.get_board_position("f1")),
                                Queen(self, game_board.get_board_position("d1")),
                                King(self, game_board.get_board_position("e1"))]
            game_board.get_board_position("a2").set_piece(self._piece_list[0])
            game_board.get_board_position("b2").set_piece(self._piece_list[1])
            game_board.get_board_position("c2").set_piece(self._piece_list[2])
            game_board.get_board_position("d2").set_piece(self._piece_list[3])
            game_board.get_board_position("e2").set_piece(self._piece_list[4])
            game_board.get_board_position("f2").set_piece(self._piece_list[5])
            game_board.get_board_position("g2").set_piece(self._piece_list[6])
            game_board.get_board_position("h2").set_piece(self._piece_list[7])
            game_board.get_board_position("a1").set_piece(self._piece_list[8])
            game_board.get_board_position("h1").set_piece(self._piece_list[9])
            game_board.get_board_position("b1").set_piece(self._piece_list[10])
            game_board.get_board_position("g1").set_piece(self._piece_list[11])
            game_board.get_board_position("c1").set_piece(self._piece_list[12])
            game_board.get_board_position("f1").set_piece(self._piece_list[13])
            game_board.get_board_position("d1").set_piece(self._piece_list[14])
            game_board.get_board_position("e1").set_piece(self._piece_list[15])
        else:
            self._piece_list = [Pawn(self, game_board.get_board_position("a7")),
                                Pawn(self, game_board.get_board_position("b7")),
                                Pawn(self, game_board.get_board_position("c7")),
                                Pawn(self, game_board.get_board_position("d7")),
                                Pawn(self, game_board.get_board_position("e7")),
                                Pawn(self, game_board.get_board_position("f7")),
                                Pawn(self, game_board.get_board_position("g7")),
                                Pawn(self, game_board.get_board_position("h7")),
                                Rook(self, game_board.get_board_position("a8")),
                                Rook(self, game_board.get_board_position("h8")),
                                Knight(self, game_board.get_board_position("b8")),
                                Knight(self, game_board.get_board_position("g8")),
                                Bishop(self, game_board.get_board_position("c8")),
                                Bishop(self, game_board.get_board_position("f8")),
                                Queen(self, game_board.get_board_position("d8")),
                                King(self, game_board.get_board_position("e8"))]
            game_board.get_board_position("a7").set_piece(self._piece_list[0])
            game_board.get_board_position("b7").set_piece(self._piece_list[1])
            game_board.get_board_position("c7").set_piece(self._piece_list[2])
            game_board.get_board_position("d7").set_piece(self._piece_list[3])
            game_board.get_board_position("e7").set_piece(self._piece_list[4])
            game_board.get_board_position("f7").set_piece(self._piece_list[5])
            game_board.get_board_position("g7").set_piece(self._piece_list[6])
            game_board.get_board_position("h7").set_piece(self._piece_list[7])
            game_board.get_board_position("a8").set_piece(self._piece_list[8])
            game_board.get_board_position("h8").set_piece(self._piece_list[9])
            game_board.get_board_position("b8").set_piece(self._piece_list[10])
            game_board.get_board_position("g8").set_piece(self._piece_list[11])
            game_board.get_board_position("c8").set_piece(self._piece_list[12])
            game_board.get_board_position("f8").set_piece(self._piece_list[13])
            game_board.get_board_position("d8").set_piece(self._piece_list[14])
            game_board.get_board_position("e8").set_piece(self._piece_list[15])

    def get_color(self):
        """
        Returns the value of color (data member).
        """

        return self._color

    def get_piece_list(self):
        """
        Returns piece_list (data member).
        """

        return self._piece_list

    def set_piece_list(self, piece):
        """
        Modifies piece_list (data member) to remove a piece subtype object.  This method is invoked
        by a piece subtype object (through its owner data member, which is a player object) when a
        piece has been captured.  The piece subtype object that has been captured is passed as
        a parameter and removed from the piece_list.
        """

        self._piece_list.remove(piece)


class Board:
    """
    Defines a Board object, which represents the game board in a game of ChessVar. This class
    is intended (i) to instantiate the board and its various board positions, and (ii) to manage where pieces
    are located on the board.

    Includes the following data members:
        - board_state - This is a dictionary with keys equal to the string representation of each board position and
                        values equal to a Board Position object.

    Includes the following methods (excluding __init__):
        - get_position_state() - Returns piece subtype object (if any) currently located at a given board position.
                                    If no piece subtype object is located at the given board position, returns None.
        - get_board_position() - Returns the Board Position object associated with a given board position string in
                                    board_state (data member).
        - set_position_state() - Uses a string (parameter) to access a given Board Position object in game_state, then
                                    uses the set_piece() method of the Board Position object, passing a new piece
                                    subtype object (parameter) to update the piece subtype object located at that
                                    board position.

    PARAMETERS: None
    RETURN: None
    """

    def __init__(self):
        """
        Initializes a Board object with board_state initialized as a dictionary with keys equal to the string
        representation of each board position and values equal to a Board Position object.
        """

        self._board_state = {
            "a1"    :   BoardPosition("a1"),
            "a2"    :   BoardPosition("a2"),
            "a3"    :   BoardPosition("a3"),
            "a4"    :   BoardPosition("a4"),
            "a5"    :   BoardPosition("a5"),
            "a6"    :   BoardPosition("a6"),
            "a7"    :   BoardPosition("a7"),
            "a8"    :   BoardPosition("a8"),
            "b1"    :   BoardPosition("b1"),
            "b2"    :   BoardPosition("b2"),
            "b3"    :   BoardPosition("b3"),
            "b4"    :   BoardPosition("b4"),
            "b5"    :   BoardPosition("b5"),
            "b6"    :   BoardPosition("b6"),
            "b7"    :   BoardPosition("b7"),
            "b8"    :   BoardPosition("b8"),
            "c1"    :   BoardPosition("c1"),
            "c2"    :   BoardPosition("c2"),
            "c3"    :   BoardPosition("c3"),
            "c4"    :   BoardPosition("c4"),
            "c5"    :   BoardPosition("c5"),
            "c6"    :   BoardPosition("c6"),
            "c7"    :   BoardPosition("c7"),
            "c8"    :   BoardPosition("c8"),
            "d1"    :   BoardPosition("d1"),
            "d2"    :   BoardPosition("d2"),
            "d3"    :   BoardPosition("d3"),
            "d4"    :   BoardPosition("d4"),
            "d5"    :   BoardPosition("d5"),
            "d6"    :   BoardPosition("d6"),
            "d7"    :   BoardPosition("d7"),
            "d8"    :   BoardPosition("d8"),
            "e1"    :   BoardPosition("e1"),
            "e2"    :   BoardPosition("e2"),
            "e3"    :   BoardPosition("e3"),
            "e4"    :   BoardPosition("e4"),
            "e5"    :   BoardPosition("e5"),
            "e6"    :   BoardPosition("e6"),
            "e7"    :   BoardPosition("e7"),
            "e8"    :   BoardPosition("e8"),
            "f1"    :   BoardPosition("f1"),
            "f2"    :   BoardPosition("f2"),
            "f3"    :   BoardPosition("f3"),
            "f4"    :   BoardPosition("f4"),
            "f5"    :   BoardPosition("f5"),
            "f6"    :   BoardPosition("f6"),
            "f7"    :   BoardPosition("f7"),
            "f8"    :   BoardPosition("f8"),
            "g1"    :   BoardPosition("g1"),
            "g2"    :   BoardPosition("g2"),
            "g3"    :   BoardPosition("g3"),
            "g4"    :   BoardPosition("g4"),
            "g5"    :   BoardPosition("g5"),
            "g6"    :   BoardPosition("g6"),
            "g7"    :   BoardPosition("g7"),
            "g8"    :   BoardPosition("g8"),
            "h1"    :   BoardPosition("h1"),
            "h2"    :   BoardPosition("h2"),
            "h3"    :   BoardPosition("h3"),
            "h4"    :   BoardPosition("h4"),
            "h5"    :   BoardPosition("h5"),
            "h6"    :   BoardPosition("h6"),
            "h7"    :   BoardPosition("h7"),
            "h8"    :   BoardPosition("h8")
        }

    def get_board_state(self):
        """
        Returns the board_state (data member).
        """

        return self._board_state

    def get_board_position(self, position_string):
        """
        Queries board_state (data member) using position_string (parameter) as the key and returns
        the Board Position object that is the value associated with that key.
        """

        return self._board_state[position_string]

    def get_position_state(self, position_string):
        """
        Queries board_state (data member) using position_string (parameter) as the key to access
        the Board Position object that is the value associated with that key.  Then uses the get_piece() method
        of the given Board Position object to return the piece subtype object located at that board position.  If
        no piece subtype object is located at that board position, returns None.
        """

        return self._board_state[position_string].get_piece()

    def set_position_state(self, position_string, piece):
        """
        Queries board_state (data member) using position_string (parameter) as the key to access
        the Board Position object that is the value associated with that key.  Then uses the set_piece() method
        of the given Board Position object to set the piece subtype object located at that board position.
        """

        self._board_state[position_string].set_piece(piece)


class BoardPosition:
    """
    Defines a Board Position object, which represents a position on the game board in a game of ChessVar. This class
    is intended (i) to instantiate a board position and (ii) to manage which piece (if any) is located at that
    board position

    Includes the following data members:
        - position_string - This is the string representation of the given board position.
        - piece - This is the piece subtype object located at the given board position (if any).

    Includes the following methods (excluding __init__):
        - get_string() - Returns the value of position_string (data member)
        - get_piece() - Returns the value of piece (data member)
        - set_piece() - Updates the value of piece (data member) to a new piece subtype object (parameter)

    PARAMETERS:
        - position_string - This is the string representation of the given board position.
    RETURN: None
    """

    def __init__(self, position_string):
        """
        Initializes a Board Position object with (i) position_string (data member) initialized to
        position_string (parameter) (i.e., the string representation of the given board position,
        and (ii) piece initialized to None.
        """

        self._position_string = position_string
        self._piece = None

    def get_string(self):
        """
        Returns the value of position_string (data member).
        """

        return self._position_string

    def get_piece(self):
        """
        Returns the value of piece (data member).
        """

        return self._piece

    def set_piece(self, piece):
        """
        Updates the value of piece (data member) to a new piece subtype object (parameter).
        """

        self._piece = piece


class Piece:
    """
    Defines a Piece object, which represents a piece in a game of ChessVar. This class
    is intended (i) to instantiate a piece, (ii) assign an owner and initial board position, and
    (iii) to execute moves of the piece on the game board, including captures.

    Includes the following data members:
        - owner - This is the Player object to which the piece is assigned.
        - position - This is the board position on which the piece is currently located (if any). If the piece
                        is no longer active in the game, set to None.

    Includes the following methods (excluding __init__):
        - get_owner() - Returns the value of owner (data member)
        - get_position() - Returns the value of position (data member)
        - set_position() - Updates the value of position (data member) to a new Board Position object (parameter)
        - move() - Takes a destination Board Position object and Board object as parameters and determines whether a
                    move to that board position is legal.  If not legal, returns False. If legal, (i) updates the value
                    of position (data member) and (ii) updates piece (data member) value of the destination
                    Board Position object to the new piece subtype object. If a piece was captured,
                    returns that piece subtype object, otherwise returns True.
        - next_position() - Used within the move() method to calculate the next board position along the path
                            from the current board position to the destination board position. If the calculated
                            next board position on the path entails an illegal move for the given piece subtype object,
                            returns None.  Otherwise, returns the next Board Position object.
        - iterate_position_str() - Used within the next_position() method to calculate the string representation
                                    of the next board position. Returns a string representing the iterated portion
                                    of the board position string. If iteration results in a string that is an invalid
                                    board position, returns None.

    PARAMETERS:
        - owner - This is the Player object to which the piece is assigned.
        - position - This is the initial Board Position object to which the piece is assigned.
    RETURNS:  None
    """

    def __init__(self, owner, position):
        """
        Initializes a Piece object with (i) owner (data member) initialized to owner (parameter)
        and (ii) position (data member) initialized to position (parameter).
        """

        self._owner = owner
        self._position = position

    def get_owner(self):
        """
        Returns the value of owner (data member)
        """

        return self._owner

    def get_position(self):
        """
        Returns the value of position (data member)
        """

        return self._position

    def set_position(self, position):
        """
        Updates the value of position (data member) to position (parameter)
        """

        self._position = position

    def move(self, position, board):
        """
        Takes a destination Board Position object and Board object as parameters and determines whether a move to that
        board position is legal.  If not legal, returns False. If legal, (i) updates the value of
        position (data member) and (ii) updates the piece (data member) value of the destination
        Board Position object to the new piece subtype object. If a piece was captured,
        returns that piece subtype object, otherwise returns True.
        """

        captured_piece = None
        starting_position = self._position
        legal_move = False

        # Determine direction of move.
        starting_position_string = starting_position.get_string()
        destination_position_string = position.get_string()
        vertical = None
        horizontal = None
        direction = None
        if starting_position_string[0] < destination_position_string[0]:
            horizontal = 1
        elif starting_position_string[0] == destination_position_string[0]:
            horizontal = 0
        else:
            horizontal = -1
        if starting_position_string[1] < destination_position_string[1]:
            vertical = 1
        elif starting_position_string[1] == destination_position_string[1]:
            vertical = 0
        else:
            vertical = -1
        if horizontal == 0 and vertical == 0:  # This implies no move has been made.
            return False
        elif horizontal == 0 and vertical == 1:
            direction = "up"
        elif horizontal == 0 and vertical == -1:
            direction = "down"
        elif horizontal == 1 and vertical == 0:
            direction = "right"
        elif horizontal == 1 and vertical == 1:
            direction = "diagonal up right"
        elif horizontal == 1 and vertical == -1:
            direction = "diagonal down right"
        elif horizontal == -1 and vertical == 0:
            direction = "left"
        elif horizontal == -1 and vertical == 1:
            direction = "diagonal up left"
        else:
            direction = "diagonal down left"

        next_position = starting_position

        # Determine whether move to specified position is legal. If not, returns False. If so, proceeds to code below.
        # Legal move test (Pawn)
        if self.get_type() == "Pawn":
            # Test if Pawn is still in starting position.  If so, it can move 1 or 2 spaces.
            if (starting_position_string[1] == "2" and self._owner.get_color() == "White") or \
                    (starting_position_string[1] == "7" and self._owner.get_color() == "Black"):
                # If move is diagonal, can move only 1 space, and move must be a capture.
                if "diagonal" in direction:
                    next_position = self.next_position(board, next_position, direction, position)
                    if next_position is None:
                        return False
                    elif next_position.get_piece() is None:
                        return False
                    else:
                        if next_position != position:
                            return False
                        elif self._owner == next_position.get_piece().get_owner():
                            return False
                # If move is not diagonal, can move 1 or 2 spaces.
                if "diagonal" not in direction:
                    for loop in range(0, 2):
                        next_position = self.next_position(board, next_position, direction, position)
                        if next_position is None:
                            return False
                        elif next_position.get_piece() is None:
                            if next_position != position:
                                if loop == 0:
                                    continue
                                else:
                                    return False
                            else:
                                break
                        else:
                            return False

            # If Pawn is not in starting position, can only move 1 space forward or diagonal.
            else:
                next_position = self.next_position(board, next_position, direction, position)
                if next_position is None:
                    return False
                # If move is diagonal, can move 1 space, only with a capture.
                elif "diagonal" in direction:
                    if next_position.get_piece() is None:
                        return False
                    else:
                        if next_position != position:
                            return False
                        elif self._owner == next_position.get_piece().get_owner():
                            return False
                # If move is not diagonal, can move 1 space without capturing.
                else:
                    if next_position.get_piece() is None:
                        if next_position != position:
                            return False
                    else:
                        return False

        # Legal move test (King / Knight)
        elif self.get_type() == "King" or self.get_type() == "Knight":
            next_position = self.next_position(board, next_position, direction, position)
            if next_position is None:
                return False
            elif next_position != position:
                return False
            elif next_position.get_piece() is not None and self._owner == next_position.get_piece().get_owner():
                return False

        # Legal move test (All others)
        else:
            while True:
                next_position = self.next_position(board, next_position, direction, position)
                if next_position is None:
                    return False
                elif next_position.get_piece() is None:
                    if next_position != position:
                        continue
                    else:
                        break
                else:
                    if next_position != position:
                        return False
                    elif self._owner == next_position.get_piece().get_owner():
                        return False
                    else:
                        break

        # If move is legal (per tests above), this code is executed.
        starting_position.set_piece(None)
        self._position = position
        captured_piece = position.get_piece()
        position.set_piece(self)
        if captured_piece is None:
            return True
        else:
            captured_piece.set_position(None)
            captured_piece.get_owner().set_piece_list(captured_piece)
            return captured_piece

    def next_position(self, board, current_position, direction, destination_position):
        """
        Used within the move() method to calculate the next board position along the path
        from the current board position to the destination board position. If the calculated
        next board position on the path entails an illegal move for the given piece subtype object,
        returns None.  Otherwise, returns the next Board Position object.

        Accepts the following parameters:
        - board - Board object
        - current_position - Current Board Position object
        - direction - String representing the direction of path from the current position to the destination position
        - destination_position - Destination Board Position object
        """

        current_position_string = current_position.get_string()
        destination_position_string = destination_position.get_string()
        next_position_string = None
        new_letter = None
        new_num = None

        if self.get_type() == "Pawn":
            if self.get_owner().get_color() == "White":
                if direction == "up":
                    new_num = self.iterate_position_str(current_position_string[1], 1)
                    if new_num is None:
                        return None
                    next_position_string = current_position_string[0] + new_num
                if direction == "down":
                    return None
                if direction == "left":
                    return None
                if direction == "right":
                    return None
                if direction == "diagonal up right":
                    new_letter = self.iterate_position_str(current_position_string[0], 1)
                    new_num = self.iterate_position_str(current_position_string[1], 1)
                    if new_letter is None or new_num is None:
                        return None
                    next_position_string = new_letter + new_num
                if direction == "diagonal up left":
                    new_letter = self.iterate_position_str(current_position_string[0], 0)
                    new_num = self.iterate_position_str(current_position_string[1], 1)
                    if new_letter is None or new_num is None:
                        return None
                    next_position_string = new_letter + new_num
                if direction == "diagonal down right":
                    return None
                if direction == "diagonal down left":
                    return None
            else:
                if direction == "up":
                    return None
                if direction == "down":
                    new_num = self.iterate_position_str(current_position_string[1], 0)
                    if new_num is None:
                        return None
                    next_position_string = current_position_string[0] + new_num
                if direction == "left":
                    return None
                if direction == "right":
                    return None
                if direction == "diagonal up right":
                    return None
                if direction == "diagonal up left":
                    return None
                if direction == "diagonal down right":
                    new_letter = self.iterate_position_str(current_position_string[0], 1)
                    new_num = self.iterate_position_str(current_position_string[1], 0)
                    if new_letter is None or new_num is None:
                        return None
                    next_position_string = new_letter + new_num
                if direction == "diagonal down left":
                    new_letter = self.iterate_position_str(current_position_string[0], 0)
                    new_num = self.iterate_position_str(current_position_string[1], 0)
                    if new_letter is None or new_num is None:
                        return None
                    next_position_string = new_letter + new_num
        if self.get_type() == "Bishop":
            if "diagonal" not in direction:
                return None
            elif direction == "diagonal up right":
                new_letter = self.iterate_position_str(current_position_string[0], 1)
                new_num = self.iterate_position_str(current_position_string[1], 1)
                if new_letter is None or new_num is None:
                    return None
            elif direction == "diagonal up left":
                new_letter = self.iterate_position_str(current_position_string[0], 0)
                new_num = self.iterate_position_str(current_position_string[1], 1)
                if new_letter is None or new_num is None:
                    return None
            elif direction == "diagonal down right":
                new_letter = self.iterate_position_str(current_position_string[0], 1)
                new_num = self.iterate_position_str(current_position_string[1], 0)
                if new_letter is None or new_num is None:
                    return None
            else:
                new_letter = self.iterate_position_str(current_position_string[0], 0)
                new_num = self.iterate_position_str(current_position_string[1], 0)
                if new_letter is None or new_num is None:
                    return None
            next_position_string = new_letter + new_num
        if self.get_type() == "Knight":
            if "diagonal" not in direction:
                return None
            elif direction == "diagonal up right":
                if int(current_position_string[1]) == int(destination_position_string[1]) - 1:
                    new_letter = self.iterate_position_str(current_position_string[0], 1, 2)
                    new_num = self.iterate_position_str(current_position_string[1], 1, 1)
                elif int(current_position_string[1]) == int(destination_position_string[1]) - 2:
                    new_letter = self.iterate_position_str(current_position_string[0], 1, 1)
                    new_num = self.iterate_position_str(current_position_string[1], 1, 2)
                if new_letter is None or new_num is None:
                    return None
            elif direction == "diagonal up left":
                if int(current_position_string[1]) == int(destination_position_string[1]) - 1:
                    new_letter = self.iterate_position_str(current_position_string[0], 0, 2)
                    new_num = self.iterate_position_str(current_position_string[1], 1, 1)
                elif int(current_position_string[1]) == int(destination_position_string[1]) - 2:
                    new_letter = self.iterate_position_str(current_position_string[0], 0, 1)
                    new_num = self.iterate_position_str(current_position_string[1], 1, 2)
                if new_letter is None or new_num is None:
                    return None
            elif direction == "diagonal down right":
                if int(current_position_string[1]) == int(destination_position_string[1]) + 1:
                    new_letter = self.iterate_position_str(current_position_string[0], 1, 2)
                    new_num = self.iterate_position_str(current_position_string[1], 0, 1)
                elif int(current_position_string[1]) == int(destination_position_string[1]) + 2:
                    new_letter = self.iterate_position_str(current_position_string[0], 1, 1)
                    new_num = self.iterate_position_str(current_position_string[1], 0, 2)
                if new_letter is None or new_num is None:
                    return None
            else:
                if int(current_position_string[1]) == int(destination_position_string[1]) + 1:
                    new_letter = self.iterate_position_str(current_position_string[0], 0, 2)
                    new_num = self.iterate_position_str(current_position_string[1], 0, 1)
                elif int(current_position_string[1]) == int(destination_position_string[1]) + 2:
                    new_letter = self.iterate_position_str(current_position_string[0], 0, 1)
                    new_num = self.iterate_position_str(current_position_string[1], 0, 2)
                if new_letter is None or new_num is None:
                    return None
            next_position_string = new_letter + new_num
        if self.get_type() == "Rook":
            if "diagonal" in direction:
                return None
            elif direction == "up":
                new_num = self.iterate_position_str(current_position_string[1], 1)
                if new_num is None:
                    return None
                next_position_string = current_position_string[0] + new_num
            elif direction == "down":
                new_num = self.iterate_position_str(current_position_string[1], 0)
                if new_num is None:
                    return None
                next_position_string = current_position_string[0] + new_num
            elif direction == "left":
                new_letter = self.iterate_position_str(current_position_string[0], 0)
                if new_letter is None:
                    return None
                next_position_string = new_letter + current_position_string[1]
            else:
                new_letter = self.iterate_position_str(current_position_string[0], 1)
                if new_letter is None:
                    return None
                next_position_string = new_letter + current_position_string[1]
        if self.get_type() == "Queen" or self.get_type() == "King":
            if direction == "up":
                new_num = self.iterate_position_str(current_position_string[1], 1)
                if new_num is None:
                    return None
                next_position_string = current_position_string[0] + new_num
            elif direction == "down":
                new_num = self.iterate_position_str(current_position_string[1], 0)
                if new_num is None:
                    return None
                next_position_string = current_position_string[0] + new_num
            elif direction == "left":
                new_letter = self.iterate_position_str(current_position_string[0], 0)
                if new_letter is None:
                    return None
                next_position_string = new_letter + current_position_string[1]
            elif direction == "right":
                new_letter = self.iterate_position_str(current_position_string[0], 1)
                if new_letter is None:
                    return None
                next_position_string = new_letter + current_position_string[1]
            elif direction == "diagonal up right":
                new_letter = self.iterate_position_str(current_position_string[0], 1)
                new_num = self.iterate_position_str(current_position_string[1], 1)
                if new_letter is None or new_num is None:
                    return None
                next_position_string = new_letter + new_num
            elif direction == "diagonal up left":
                new_letter = self.iterate_position_str(current_position_string[0], 0)
                new_num = self.iterate_position_str(current_position_string[1], 1)
                if new_letter is None or new_num is None:
                    return None
                next_position_string = new_letter + new_num
            elif direction == "diagonal down right":
                new_letter = self.iterate_position_str(current_position_string[0], 1)
                new_num = self.iterate_position_str(current_position_string[1], 0)
                if new_letter is None or new_num is None:
                    return None
                next_position_string = new_letter + new_num
            else:
                new_letter = self.iterate_position_str(current_position_string[0], 0)
                new_num = self.iterate_position_str(current_position_string[1], 0)
                if new_letter is None or new_num is None:
                    return None
                next_position_string = new_letter + new_num
        return board.get_board_position(next_position_string)

    def iterate_position_str(self, character, direction, distance=None):
        """
        Used within the next_position() method to calculate the string representation
        of the next board position. Returns a string representing the iterated portion
        of the board position string. If iteration results in a string that is an invalid
        board position, returns None.

        Accepts the following parameters:
        - character - Single-character string representing the character to be iterated
        - direction - String representing the direction of path from the current position to the destination position
        - distance - Used only for Knight moves. Identifies the amount to which to iterate the character (parameter)
        """

        if self.get_type() != "Knight" or distance == 1:
            if direction == 0:
                if "a" <= character <= "h":
                    if character == "a":
                        return None
                    if character == "b":
                        return "a"
                    if character == "c":
                        return "b"
                    if character == "d":
                        return "c"
                    if character == "e":
                        return "d"
                    if character == "f":
                        return "e"
                    if character == "g":
                        return "f"
                    if character == "h":
                        return "g"
                elif "1" <= character <= "8":
                    if character == "1":
                        return None
                    if character == "2":
                        return "1"
                    if character == "3":
                        return "2"
                    if character == "4":
                        return "3"
                    if character == "5":
                        return "4"
                    if character == "6":
                        return "5"
                    if character == "7":
                        return "6"
                    if character == "8":
                        return "7"
                else:
                    return None
            else:
                if "a" <= character <= "h":
                    if character == "a":
                        return "b"
                    if character == "b":
                        return "c"
                    if character == "c":
                        return "d"
                    if character == "d":
                        return "e"
                    if character == "e":
                        return "f"
                    if character == "f":
                        return "g"
                    if character == "g":
                        return "h"
                    if character == "h":
                        return None
                elif "1" <= character <= "8":
                    if character == "1":
                        return "2"
                    if character == "2":
                        return "3"
                    if character == "3":
                        return "4"
                    if character == "4":
                        return "5"
                    if character == "5":
                        return "6"
                    if character == "6":
                        return "7"
                    if character == "7":
                        return "8"
                    if character == "8":
                        return None
                else:
                    return None
        else:
            if direction == 0:
                if "a" <= character <= "h":
                    if character == "a":
                        return None
                    if character == "b":
                        return None
                    if character == "c":
                        return "a"
                    if character == "d":
                        return "b"
                    if character == "e":
                        return "c"
                    if character == "f":
                        return "d"
                    if character == "g":
                        return "e"
                    if character == "h":
                        return "f"
                elif "1" <= character <= "8":
                    if character == "1":
                        return None
                    if character == "2":
                        return None
                    if character == "3":
                        return "1"
                    if character == "4":
                        return "2"
                    if character == "5":
                        return "3"
                    if character == "6":
                        return "4"
                    if character == "7":
                        return "5"
                    if character == "8":
                        return "6"
                else:
                    return None
            else:
                if "a" <= character <= "h":
                    if character == "a":
                        return "c"
                    if character == "b":
                        return "d"
                    if character == "c":
                        return "e"
                    if character == "d":
                        return "f"
                    if character == "e":
                        return "g"
                    if character == "f":
                        return "h"
                    if character == "g":
                        return None
                    if character == "h":
                        return None
                elif "1" <= character <= "8":
                    if character == "1":
                        return "3"
                    if character == "2":
                        return "4"
                    if character == "3":
                        return "5"
                    if character == "4":
                        return "6"
                    if character == "5":
                        return "7"
                    if character == "6":
                        return "8"
                    if character == "7":
                        return None
                    if character == "8":
                        return None
                else:
                    return None


class Pawn(Piece):
    """
    Defines a Pawn object, which represents a pawn in a game of ChessVar. This class
    is intended (i) to instantiate a pawn and (ii) to hold the special characteristics of the
    pawn subtype of a Piece object, including the piece's specific type.

    Includes the following data members:
        - Inherits all data members from the Piece class.
        - type - This is a string representing the piece's type (i.e., "Pawn")
        - type_abrv - This is an abbreviation of type.

    Includes the following methods (excluding __init__):
        - Inherits all methods from the Piece class.
        - get_type() - Returns the value of type (data member)

    PARAMETERS:
        - Inherits all parameters from the Piece class, including:
            - owner - This is the Player object to which the piece is assigned.
            - position - This is the initial Board Position object to which the piece is assigned.
    RETURNS:  None
    """

    def __init__(self, owner, position):
        """
        Initializes a Piece object with (i) owner (data member) initialized to owner (parameter),
        (ii) position (data member) initialized to position (parameter), and (iii) type (data member)
        initialized to "Pawn".
        """

        super().__init__(owner, position)
        self._type = "Pawn"
        self._type_abrv = "P"

    def get_type(self):
        """
        Returns the value of type (data member).
        """

        return self._type

    def get_type_abrv(self):
        """
        Returns the value of type_abrv (data member).
        """

        return self._type_abrv


class Knight(Piece):
    """
    Defines a Knight object, which represents a Knight in a game of ChessVar. This class
    is intended (i) to instantiate a Knight and (ii) to hold the special characteristics of the
    Knight subtype of a Piece object, including the piece's specific type.

    Includes the following data members:
        - Inherits all data members from the Piece class.
        - type - This is a string representing the piece's type (i.e., "Knight")
        - type_abrv - This is an abbreviation of type.

    Includes the following methods (excluding __init__):
        - Inherits all methods from the Piece class.
        - get_type() - Returns the value of type (data member)

    PARAMETERS:
        - Inherits all parameters from the Piece class, including:
            - owner - This is the Player object to which the piece is assigned.
            - position - This is the initial Board Position object to which the piece is assigned.
    RETURNS:  None
    """

    def __init__(self, owner, position):
        """
        Initializes a Piece object with (i) owner (data member) initialized to owner (parameter),
        (ii) position (data member) initialized to position (parameter), and (iii) type (data member)
        initialized to "Knight".
        """

        super().__init__(owner, position)
        self._type = "Knight"
        self._type_abrv = "Kn"

    def get_type(self):
        """
        Returns the value of type (data member).
        """

        return self._type

    def get_type_abrv(self):
        """
        Returns the value of type_abrv (data member).
        """

        return self._type_abrv


class Bishop(Piece):
    """
    Defines a Bishop object, which represents a Bishop in a game of ChessVar. This class
    is intended (i) to instantiate a Bishop and (ii) to hold the special characteristics of the
    Bishop subtype of a Piece object, including the piece's specific type.

    Includes the following data members:
        - Inherits all data members from the Piece class.
        - type - This is a string representing the piece's type (i.e., "Bishop")
        - type_abrv - This is an abbreviation of type.

    Includes the following methods (excluding __init__):
        - Inherits all methods from the Piece class.
        - get_type() - Returns the value of type (data member)

    PARAMETERS:
        - Inherits all parameters from the Piece class, including:
            - owner - This is the Player object to which the piece is assigned.
            - position - This is the initial Board Position object to which the piece is assigned.
    RETURNS:  None
    """

    def __init__(self, owner, position):
        """
        Initializes a Piece object with (i) owner (data member) initialized to owner (parameter),
        (ii) position (data member) initialized to position (parameter), and (iii) type (data member)
        initialized to "Bishop".
        """

        super().__init__(owner, position)
        self._type = "Bishop"
        self._type_abrv = "B"

    def get_type(self):
        """
        Returns the value of type (data member).
        """

        return self._type

    def get_type_abrv(self):
        """
        Returns the value of type_abrv (data member).
        """

        return self._type_abrv


class Rook(Piece):
    """
    Defines a Rook object, which represents a Rook in a game of ChessVar. This class
    is intended (i) to instantiate a Rook and (ii) to hold the special characteristics of the
    Rook subtype of a Piece object, including the piece's specific type.

    Includes the following data members:
        - Inherits all data members from the Piece class.
        - type - This is a string representing the piece's type (i.e., "Rook")
        - type_abrv - This is an abbreviation of type.

    Includes the following methods (excluding __init__):
        - Inherits all methods from the Piece class.
        - get_type() - Returns the value of type (data member)

    PARAMETERS:
        - Inherits all parameters from the Piece class, including:
            - owner - This is the Player object to which the piece is assigned.
            - position - This is the initial Board Position object to which the piece is assigned.
    RETURNS:  None
    """

    def __init__(self, owner, position):
        """
        Initializes a Piece object with (i) owner (data member) initialized to owner (parameter),
        (ii) position (data member) initialized to position (parameter), and (iii) type (data member)
        initialized to "Rook".
        """

        super().__init__(owner, position)
        self._type = "Rook"
        self._type_abrv = "R"

    def get_type(self):
        """
        Returns the value of type (data member).
        """

        return self._type

    def get_type_abrv(self):
        """
        Returns the value of type_abrv (data member).
        """

        return self._type_abrv


class Queen(Piece):
    """
    Defines a Queen object, which represents a Queen in a game of ChessVar. This class
    is intended (i) to instantiate a Queen and (ii) to hold the special characteristics of the
    Queen subtype of a Piece object, including the piece's specific type.

    Includes the following data members:
        - Inherits all data members from the Piece class.
        - type - This is a string representing the piece's type (i.e., "Queen")
        - type_abrv - This is an abbreviation of type.

    Includes the following methods (excluding __init__):
        - Inherits all methods from the Piece class.
        - get_type() - Returns the value of type (data member)

    PARAMETERS:
        - Inherits all parameters from the Piece class, including:
            - owner - This is the Player object to which the piece is assigned.
            - position - This is the initial Board Position object to which the piece is assigned.
    RETURNS:  None
    """

    def __init__(self, owner, position):
        """
        Initializes a Piece object with (i) owner (data member) initialized to owner (parameter),
        (ii) position (data member) initialized to position (parameter), and (iii) type (data member)
        initialized to "Queen".
        """

        super().__init__(owner, position)
        self._type = "Queen"
        self._type_abrv = "Q"

    def get_type(self):
        """
        Returns the value of type (data member).
        """

        return self._type

    def get_type_abrv(self):
        """
        Returns the value of type_abrv (data member).
        """

        return self._type_abrv


class King(Piece):
    """
    Defines a King object, which represents a King in a game of ChessVar. This class
    is intended (i) to instantiate a King and (ii) to hold the special characteristics of the
    King subtype of a Piece object, including the piece's specific type.

    Includes the following data members:
        - Inherits all data members from the Piece class.
        - type - This is a string representing the piece's type (i.e., "King")
        - type_abrv - This is an abbreviation of type.

    Includes the following methods (excluding __init__):
        - Inherits all methods from the Piece class.
        - get_type() - Returns the value of type (data member)

    PARAMETERS:
        - Inherits all parameters from the Piece class, including:
            - owner - This is the Player object to which the piece is assigned.
            - position - This is the initial Board Position object to which the piece is assigned.
    RETURNS:  None
    """

    def __init__(self, owner, position):
        """
        Initializes a Piece object with (i) owner (data member) initialized to owner (parameter),
        (ii) position (data member) initialized to position (parameter), and (iii) type (data member)
        initialized to "King".
        """

        super().__init__(owner, position)
        self._type = "King"
        self._type_abrv = "K"

    def get_type(self):
        """
        Returns the value of type (data member).
        """

        return self._type

    def get_type_abrv(self):
        """
        Returns the value of type_abrv (data member).
        """

        return self._type_abrv

if __name__ == "__main__":
    pass
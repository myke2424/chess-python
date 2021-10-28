from typing import List


class Move:
    """ Abstraction that represents all the data in a player move. """

    def __init__(self, starting_square: tuple, destination_square: tuple, board: List[List[str]]):
        self.start_row = starting_square.row
        self.start_col = starting_square.col
        self.dest_row = destination_square.row
        self.dest_col = destination_square.col
        self.piece_to_move = board[self.start_row][self.start_col]
        self.piece_to_capture = board[self.dest_row][self.dest_col]  # This can be an empty square

    def __repr__(self) -> str:
        """ Printable representation of a move made in chess notation """
        color = self.piece_to_move[0]
        piece_type = self.piece_to_move[1]

        return f"row: {self.start_row}, col: {self.start_col}"

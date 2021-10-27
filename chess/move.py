from typing import List


class Move:
    """ Abstraction that represents all the data in a player move """

    def __init__(self, starting_square: tuple, destination_square: tuple, board: List[List[str]]):
        self.start_row = starting_square[0]
        self.start_col = starting_square[1]
        self.dest_row = destination_square[0]
        self.dest_col = destination_square[1]
        self.piece_to_move = board[self.start_row][self.start_col]
        self.piece_to_capture = board[self.dest_row][self.dest_col]  # This can be an empty square

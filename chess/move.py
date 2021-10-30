from typing import List

from chess_notation import ChessNotationParser
from square import Square


class Move:
    """ Abstraction that represents all the data in a player move. """

    def __init__(self, start_square: Square, dest_square: Square, board: List[List[str]]):
        self.start_row = start_square.row
        self.start_col = start_square.col
        self.dest_row = dest_square.row
        self.dest_col = dest_square.col
        self.piece_to_move = board[self.start_row][self.start_col]
        self.piece_to_capture = board[self.dest_row][self.dest_col]  # This can be an empty square
        self.maker = self.piece_to_move.color if hasattr(self.piece_to_move, "color") else None

    def __repr__(self) -> str:
        """ Printable representation of a move made in chess notation """
        starting_square_notation = ChessNotationParser.from_row_and_col(row=self.start_row, col=self.start_col)
        destination_square_notation = ChessNotationParser.from_row_and_col(row=self.dest_row, col=self.dest_col)

        return f"Move({self.piece_to_move} {starting_square_notation}->{destination_square_notation})"

    def __eq__(self, other: "Move") -> bool:
        """ Checks if two moves are the same """
        if isinstance(other, Move):
            if (
                self.start_row == other.start_row
                and self.dest_row == other.dest_row
                and self.start_col == other.start_col
                and self.dest_col == other.dest_col
            ):
                return True
        return False

    @classmethod
    def from_chess_notation(cls, starting_square: str, destination_square: str, board: List[List[str]]) -> "Move":
        """ Alternate constructor to create a move obj from standard chess notation """
        pass

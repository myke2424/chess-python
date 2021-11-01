import logging

from chess_notation import ChessNotationParser
from utils import Board, Color, Square

logger = logging.getLogger(__name__)


class Move:
    """ Abstraction that represents all the data in a player move. """

    def __init__(self, start_square: Square, dest_square: Square, board: Board):
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

    def is_pawn_promotion(self) -> bool:
        """ Checks if the move is a pawn promotion for black or white """
        if self.maker == Color.WHITE and self.piece_to_move.value == 1 and self.dest_row == 0:
            return True

        elif self.maker == Color.BLACK and self.piece_to_move.value == 1 and self.dest_row == 7:
            return True

        return False

    def is_check(self) -> bool:
        """ Checks if the move is attacking the other king (check) """
        if (
            hasattr(self.piece_to_capture, "value")
            and self.piece_to_capture.value == 100
            and self.piece_to_capture.color != self.piece_to_move.color
        ):
            return True
        return False

    @classmethod
    def from_chess_notation(cls, notation: str, board: Board) -> "Move":
        """
        Alternate constructor to create a move obj from standard chess notation
        Notation e.g. (e4->e6)
        """
        notation = notation.split("->")
        start_notation, dest_notation = notation[0], notation[1]

        start_square = ChessNotationParser.from_notation(start_notation)
        dest_square = ChessNotationParser.from_notation(dest_notation)

        return cls(start_square=start_square, dest_square=dest_square, board=board)

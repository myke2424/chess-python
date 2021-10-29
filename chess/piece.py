from square import Square
from chess_notation import ChessNotationParser
from enum import Enum


class Color(Enum):
    WHITE = "w"
    BLACK = "b"


class Piece:
    def __init__(self, color: str, row: int, col: int):
        self.color = Color(color)
        self.pos = Square(row, col)
        self.moves_made = 0
        self.name = color + self.__class__.__name__  # name is color + piece type, e.g. bKnight

    @property
    def pos_chess_notation(self) -> str:
        """ Position on the chess board in standard chess notation """
        return ChessNotationParser.from_row_and_col(self.pos.row, self.pos.col)

    def possible_moves(self) -> list:
        """ Polymorphic function we can use to generate all possible moves for the piece """
        pass

    def __repr__(self) -> str:
        """ Return the piece name/color and position on the board in chess notation """
        type_ = self.__class__.__name__
        color = "Black" if self.color == "b" else "White"

        return f"{color} {type_} {self.pos_chess_notation}"


class Pawn(Piece):
    value = 1

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self):
        """ Get all the pawn moves for the pawn in its current position on the board """
        pass


class Bishop(Piece):
    value = 3

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)


class Knight(Piece):
    value = 3

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)


class Rook(Piece):
    value = 5

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)


class Queen(Piece):
    value = 9

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)


class King(Piece):
    value = 100

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

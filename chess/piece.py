from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from chess_notation import ChessNotationParser
from move import Move
from square import Square

EMPTY_SQUARE = "**"


class Color(Enum):
    WHITE = "w"
    BLACK = "b"


class Piece(ABC):
    def __init__(self, color: str, row: int, col: int):
        self.color = Color(color)
        self.pos = Square(row, col)
        self.moves_made = 0
        self.name = color + self.__class__.__name__  # name is color + piece type, e.g. bKnight

    def __repr__(self) -> str:
        """ Return the piece name/color  """
        type_ = self.__class__.__name__
        color = "Black" if self.color == Color.BLACK else "White"

        return f"{color} {type_}"

    def __eq__(self, other: "Piece") -> bool:
        """ Checks if two pieces are equal """
        if isinstance(other, Piece):
            if self.name == other.name and self.pos.row == other.pos.row and self.pos.col == other.pos.col:
                return True
        return False

    @property
    def pos_chess_notation(self) -> str:
        """ Position on the chess board in standard chess notation """
        return ChessNotationParser.from_row_and_col(self.pos.row, self.pos.col)

    def update_position(self, destination_square: Square) -> None:
        """ Update the pieces position to the destination square """
        self.pos = destination_square

    @abstractmethod
    def possible_moves(self, board) -> List[Move]:
        """ Interface we can use to generate all possible moves for the piece given the current state of the board """
        pass


class Pawn(Piece):
    value = 1

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    # White pawns move UP the board
    # Black pawns move DOWN the board
    # Can't move backwards
    # Pawn can move two squares on the first move
    # Capture Diagonally
    def possible_moves(self, board) -> List[Move]:
        """ Get all the pawn moves for its current position on the board """
        moves = []
        if self.color == Color.WHITE:
            # Since we're white, check the square above us and see if its empty
            if board[self.pos.row - 1][self.pos.col] == EMPTY_SQUARE:  # 1 square pawn advance
                square_to_land_on = Square(row=self.pos.row - 1, col=self.pos.col)
                move = Move(starting_square=self.pos, destination_square=square_to_land_on, board=board)
                moves.append(move)

                # Check if the second square above is free (2 square pawn advance)
                if self.moves_made == 0 and board[self.pos.row - 2][self.pos.col] == EMPTY_SQUARE:
                    square_to_land_on = Square(row=self.pos.row - 2, col=self.pos.col)
                    move = Move(starting_square=self.pos, destination_square=square_to_land_on, board=board)
                    moves.append(move)
        elif self.color == Color.BLACK:
            if board[self.pos.row + 1][self.pos.col] == EMPTY_SQUARE:  # 1 square pawn advance
                square_to_land_on = Square(row=self.pos.row + 1, col=self.pos.col)
                move = Move(starting_square=self.pos, destination_square=square_to_land_on, board=board)
                moves.append(move)

                # Check if the second square above is free (2 square pawn advance)
                if self.moves_made == 0 and board[self.pos.row + 2][self.pos.col] == EMPTY_SQUARE:
                    square_to_land_on = Square(row=self.pos.row + 2, col=self.pos.col)
                    move = Move(starting_square=self.pos, destination_square=square_to_land_on, board=board)
                    moves.append(move)
        return moves


class Bishop(Piece):
    value = 3

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board) -> List[Move]:
        return []


class Knight(Piece):
    value = 3

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board) -> List[Move]:
        return []


class Rook(Piece):
    value = 5

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board) -> List[Move]:
        return []


class Queen(Piece):
    value = 9

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board) -> List[Move]:
        return []


class King(Piece):
    value = 100

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board) -> List[Move]:
        return []

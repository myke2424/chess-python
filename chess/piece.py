from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from typing import List, Optional
import uuid

from chess_notation import ChessNotationParser
from constants import EMPTY_SQUARE
from move import Move
from square import Square


class Color(Enum):
    WHITE = "w"
    BLACK = "b"


class Piece(ABC):
    def __init__(self, color: str, row: int, col: int):
        self.color = Color(color)
        self.pos = Square(row, col)
        self.moves_made = 0
        self.name = color + self.__class__.__name__  # name is color + piece type, e.g. bKnight
        self.id = uuid.uuid4()

    def __repr__(self) -> str:
        """ Return the piece name/color  """
        type_ = self.__class__.__name__
        color = "Black" if self.color == Color.BLACK else "White"

        return f"{color} {type_}"

    def __eq__(self, other: "Piece") -> bool:
        """ Checks if two pieces are equal """
        if isinstance(other, Piece):
            return self.id == other.id
        return False

    @property
    def pos_chess_notation(self) -> str:
        """ Position on the chess board in standard chess notation """
        return ChessNotationParser.from_row_and_col(self.pos.row, self.pos.col)

    @abstractmethod
    def possible_moves(self, board) -> List[Move]:
        """ Interface we can use to generate all possible moves for the piece given the current state of the board """
        pass

    def capture(self, board, piece_to_capture: "Piece", moves: list) -> None:
        """ Interface used to generate a capture move on the board and add it to the list of moves """
        if isinstance(piece_to_capture, Piece) and piece_to_capture.color != self.color:
            move = Move(start_square=self.pos, dest_square=deepcopy(piece_to_capture.pos), board=board)
            moves.append(move)


class Pawn(Piece):
    value = 1

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board) -> List[Move]:
        """
        Get all the pawn moves for its current position on the board.
        Pawns can't move backwards
        Pawns can move two squares on the first move
        Pawns Capture Diagonally
        """
        moves = []

        if self.color == Color.WHITE:
            moves.extend(self._possible_moves_for_white(board=board))
        else:
            moves.extend(self._possible_moves_for_black(board=board))

        return moves

    # TODO: black/white same function except black goes down, white goes up, refactor into one.
    def _possible_moves_for_white(self, board) -> List[Move]:
        """ All possible moves for white, white pawns move UP the board """
        moves = []
        row, col = self.pos.row, self.pos.col

        if board[row - 1][col] == EMPTY_SQUARE:
            one_square_advance = Move(start_square=self.pos, dest_square=Square(row - 1, col), board=board)
            moves.append(one_square_advance)

            # 2 square pawn advance if it hasn't moved already
            if self.moves_made == 0 and board[row - 2][col] == EMPTY_SQUARE:
                two_square_advance = Move(start_square=self.pos, dest_square=Square(row - 2, col), board=board)
                moves.append(two_square_advance)

            # Check if were in bounds (going left won't push us off the board)
            if col - 1 >= 0:
                self.capture(board=board, piece_to_capture=board[row - 1][col - 1], moves=moves)

            # Check if were in bounds (going right won't push us off the board)
            if col + 1 <= 7:
                self.capture(board=board, piece_to_capture=board[row - 1][col + 1], moves=moves)

        return moves

    def _possible_moves_for_black(self, board) -> List[Move]:
        """ All possible moves for black, black pawns move DOWN the board """
        moves = []
        row, col = self.pos.row, self.pos.col

        if board[row + 1][col] == EMPTY_SQUARE:
            one_square_advance = Move(start_square=self.pos, dest_square=Square(row + 1, col), board=board)
            moves.append(one_square_advance)

            # 2 square pawn advance if it hasn't moved already
            if self.moves_made == 0 and board[row + 2][col] == EMPTY_SQUARE:
                two_square_advance = Move(start_square=self.pos, dest_square=Square(row + 2, col), board=board)
                moves.append(two_square_advance)

            # Check if were in bounds (going left won't push us off the board)
            if col - 1 >= 0:
                self.capture(board=board, piece_to_capture=board[row + 1][col - 1], moves=moves)

            # Check if were in bounds (going right won't push us off the board)
            if col + 1 <= 7:
                self.capture(board=board, piece_to_capture=board[row + 1][col + 1], moves=moves)

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

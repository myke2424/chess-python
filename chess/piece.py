import logging
import uuid
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List

from chess_notation import ChessNotationParser
from move import Move
from utils import EMPTY_SQUARE, Board, Color, Square

logger = logging.getLogger(__name__)


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
    def possible_moves(self, board: Board) -> List[Move]:
        """ Interface we can use to generate all possible moves for the piece given the current state of the board """
        pass

    def capture(self, board: Board, piece_to_capture: "Piece", moves: list) -> None:
        """ Interface used to generate a capture move on the board and add it to the list of moves """
        if isinstance(piece_to_capture, Piece) and piece_to_capture.color != self.color:
            move = Move(start_square=self.pos, dest_square=deepcopy(piece_to_capture.pos), board=board)
            moves.append(move)


class Pawn(Piece):
    value = 1

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    # TODO: Reduce complexity
    def possible_moves(self, board: Board) -> List[Move]:
        """
        Get all the pawn moves for its current position on the board.
        Pawns can't move backwards
        Pawns can move two squares on the first move
        Pawns Capture Diagonally
        """
        moves = []
        row, col = self.pos.row, self.pos.col

        # TODO: Better way to do this?
        one_square_up = row - 1 if self.color == Color.WHITE else row + 1
        two_square_up = row - 2 if self.color == Color.WHITE else row + 2

        # In bounds
        if 7 >= one_square_up >= 0 and 7 >= col >= 0:
            if board[one_square_up][col] == EMPTY_SQUARE:
                one_square_advance = Move(start_square=self.pos, dest_square=Square(one_square_up, col), board=board)
                moves.append(one_square_advance)

                # 2 square pawn advance if it hasn't moved already
                if self.moves_made == 0 and board[two_square_up][col] == EMPTY_SQUARE:
                    two_square_advance = Move(
                        start_square=self.pos, dest_square=Square(two_square_up, col), board=board
                    )
                    moves.append(two_square_advance)

            # Check if were in bounds (going left won't push us off the board)
            if col - 1 >= 0:
                self.capture(board=board, piece_to_capture=board[one_square_up][col - 1], moves=moves)

            # Check if were in bounds (going right won't push us off the board)
            if col + 1 <= 7:
                self.capture(board=board, piece_to_capture=board[one_square_up][col + 1], moves=moves)

        return moves

    # TODO: Image needs to update... GUI will handle this.
    def promote(self) -> None:
        """ Promote the pawn """
        promote_to = {"q": Queen, "k": Knight, "r": Rook, "b": Bishop}

        while True:
            promoted_type = input("Promote to q (Queen), k (Knight), r (Rook) , b (Bishop) : ")
            if promote_to.get(promoted_type) is not None:
                break
        logger.debug(f"{self} Promoted to {promote_to[promoted_type]}")
        # change the class... this actually works....
        self.__class__ = promote_to[promoted_type]


class Bishop(Piece):
    value = 3

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board: Board) -> List[Move]:
        return []


class Knight(Piece):
    value = 3

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board: Board) -> List[Move]:
        return []


class Rook(Piece):
    value = 5

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board: Board) -> List[Move]:
        """
        Rooks can move left-right-up-down any amount of squares as long as pieces aren't in the way
        A rook can potentially move up to 7 squares (in four directions)
        """
        return []


class Queen(Piece):
    value = 9

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board: Board) -> List[Move]:
        return []


class King(Piece):
    value = 100

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board: Board) -> List[Move]:
        return []

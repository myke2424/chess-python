import logging
import uuid
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List
from collections import namedtuple

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

    def capture(self, board: Board, piece_to_capture: "Piece", moves: List[Move]) -> None:
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

    def promote(self) -> Piece:
        """ Promote the pawn """
        promote_to = {"q": Queen, "k": Knight, "r": Rook, "b": Bishop}

        while True:
            promoted_type = input("Promote to q (Queen), k (Knight), r (Rook) , b (Bishop) : ")
            if promote_to.get(promoted_type) is not None:
                break

        promoted_cls = promote_to[promoted_type]
        logger.debug(f"{self} Promoted to {promoted_cls}")

        return promoted_cls(color=self.color.value, row=self.pos.row, col=self.pos.col)


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
        # (row,col)
        # (-1,0) is UP
        # (1, 0) is DOWN
        # (0, -1) is LEFT
        # (0, 1) is Right
        # directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

        moves = []
        row, col = self.pos.row, self.pos.col

        Directions = namedtuple('Directions', 'up down left right')
        directions = Directions(up=Square(-1, 0), down=Square(1, 0), left=Square(0, -1), right=Square(0, 1))

        for direction in directions:
            for i in range(1, 8):
                r = row + direction.row * i
                c = col + direction.col * i

                # In bounds
                if 0 <= r <= 7 and 0 <= c <= 7:
                    p = board[r][c]

                    # Our piece is blocking the square
                    if isinstance(p, Piece) and p.color == self.color:
                        break
                    # It's empty... VALID MOVE
                    elif p == EMPTY_SQUARE:
                        moves.append(Move(self.pos, Square(r, c), board))

                    # CAPTURE
                    else:
                        self.capture(board, p, moves)
        return moves

        # 0 - 6
        # c = 1
        # for i in range(7):
        #     # move down
        #     if row + c >= 7:
        #         break
        #     next_row = board[row + c][col]
        #     if next_row.id == self.id:
        #         print("YO")
        #         break
        #         # capture
        #     elif isinstance(next_row, Piece) and next_row.color != self.color:
        #         m = Move(self.pos, Square(row + c, col), board)
        #         c += 1
        #         moves.append(m)
        #         break
        #     else:
        #         m = Move(self.pos, Square(row + c, col), board)
        #         c += 1
        #         moves.append(m)
        #
        # return moves


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

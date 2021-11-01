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


# TODO: Refactor potential moves, a lot of repeating logic... BRUTE FORCING for now.


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
    _Directions = namedtuple("Directions", "up_right_diag, up_left_diag down_left_diag down_right_diag")

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    # TODO: Bishop move logic is very similar to rooks, possible refactor (add method on piece?)
    def possible_moves(self, board: Board) -> List[Move]:
        """
        Bishops can only move on diagonals. It can potentially move up to 7 square diagonally if no piece is blocking.
        If it starts on a dark square, it can only attack dark square pieces.
        If it starts on a light square, it can only attack light square pieces
        """
        moves = []
        row, col = self.pos.row, self.pos.col

        directions = self._Directions(
            up_right_diag=Square(-1, 1),
            up_left_diag=Square(-1, -1),
            down_left_diag=Square(1, -1),
            down_right_diag=Square(1, 1),
        )

        for direction in directions:
            for i in range(1, 8):
                row_advancement = row + direction.row * i
                col_advancement = col + direction.col * i

                if 0 <= row_advancement <= 7 and 0 <= col_advancement <= 7:
                    piece = board[row_advancement][col_advancement]
                    if isinstance(piece, Piece) and piece.color == self.color:
                        break
                    elif piece == EMPTY_SQUARE:
                        move = Move(
                            start_square=self.pos, dest_square=Square(row_advancement, col_advancement), board=board
                        )
                        moves.append(move)
                    else:
                        self.capture(board=board, piece_to_capture=piece, moves=moves)
                        break
        return moves


class Knight(Piece):
    value = 3
    _potential_advancements = [(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1)]

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board: Board) -> List[Move]:
        """
        Knights move in L-Shapes on the board and can jump over pieces to reach its destination.
        Two square advancement vertically with one square horizontally or vice versa.
        This means a knight has a maximum of 8 potential landing squares.
        """
        moves = []
        row, col = self.pos.row, self.pos.col
        knight_advancements = [Square(*adv) for adv in self._potential_advancements]

        for advancement in knight_advancements:
            row_advancement = row + advancement.row
            col_advancement = col + advancement.col

            # In bounds
            if 0 <= row_advancement <= 7 and 0 <= col_advancement <= 7:
                piece = board[row_advancement][col_advancement]

                if isinstance(piece, Piece) and piece.color == self.color:
                    continue
                elif piece == EMPTY_SQUARE:
                    move = Move(
                        start_square=self.pos, dest_square=Square(row_advancement, col_advancement), board=board
                    )
                    moves.append(move)
                else:
                    self.capture(board=board, piece_to_capture=piece, moves=moves)

        return moves


class Rook(Piece):
    value = 5
    _Directions = namedtuple("Directions", "up down left right")

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board: Board) -> List[Move]:
        """
        Rooks can move left-right-up-down any amount of squares as long as pieces aren't in the way
        A rook can potentially move up to 7 squares (in four directions)
        """

        moves = []
        row, col = self.pos.row, self.pos.col
        directions = self._Directions(up=Square(-1, 0), down=Square(1, 0), left=Square(0, -1), right=Square(0, 1))

        for direction in directions:
            for i in range(1, 8):
                # Up to 7 square advancements for each direction
                row_advancement = row + direction.row * i
                col_advancement = col + direction.col * i

                # In bounds
                if 0 <= row_advancement <= 7 and 0 <= col_advancement <= 7:
                    piece = board[row_advancement][col_advancement]

                    # Our piece is blocking the square
                    if isinstance(piece, Piece) and piece.color == self.color:
                        break
                    # It's empty... Add the move!
                    elif piece == EMPTY_SQUARE:
                        move = Move(
                            start_square=self.pos, dest_square=Square(row_advancement, col_advancement), board=board
                        )
                        moves.append(move)
                    # Capture enemy piece!
                    else:
                        self.capture(board=board, piece_to_capture=piece, moves=moves)
                        break
        return moves


class Queen(Piece):
    value = 9

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board: Board) -> List[Move]:
        """
        Queens can move any number of unoccupied squares vertically, horizontally or diagonally.
        Thus combining the moves of the rook(vertical/horizontal) and the bishop(diagonal)
        """
        # This feels hacky but this abstraction will work for now
        _rook = Rook(color=self.color.value, row=self.pos.row, col=self.pos.col)
        _bishop = Bishop(color=self.color.value, row=self.pos.row, col=self.pos.col)
        moves = [*_rook.possible_moves(board), *_bishop.possible_moves(board)]

        return moves


class King(Piece):
    value = 100
    _potential_advancements = [(0, -1), (0, 1), (1, -1), (1, 0), (1, 1), (-1, -1), (-1, 0), (-1, 1)]

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color=color, row=row, col=col)

    def possible_moves(self, board: Board) -> List[Move]:
        """
        Kings can only move one space in any direction. Up to 8 potential landing squares.
        The king can never move into a spot where it will be danger (checked)
        """
        moves = []
        row, col = self.pos.row, self.pos.col
        king_advancements = [Square(*adv) for adv in self._potential_advancements]

        for advancement in king_advancements:
            row_advancement = row + advancement.row
            col_advancement = col + advancement.col

            # In bounds
            if 0 <= row_advancement <= 7 and 0 <= col_advancement <= 7:
                piece = board[row_advancement][col_advancement]

                if isinstance(piece, Piece) and piece.color == self.color:
                    continue
                elif piece == EMPTY_SQUARE:
                    move = Move(
                        start_square=self.pos, dest_square=Square(row_advancement, col_advancement), board=board
                    )
                    moves.append(move)
                else:
                    self.capture(board=board, piece_to_capture=piece, moves=moves)

        return moves

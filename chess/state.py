import copy
import logging
from typing import List
from functools import reduce
from itertools import chain

from piece import Piece
from move import Move
from utils import EMPTY_SQUARE, Board, Color, Square

from chess import (
    BLACKS_STARTING_KINGS_ROW,
    BLACKS_STARTING_PAWN_ROW,
    WHITES_STARTING_KINGS_ROW,
    WHITES_STARTING_PAWN_ROW,
)

logger = logging.getLogger(__name__)


class GameState:
    """
    Responsible for storing/updating all the information about the current state of the game.
    Update state (make moves), record move log, keep track of who's got the piece advantage etc."
    """

    def __init__(self):
        """
        board: 8x8 matrix with starting chess pieces for black/white. '**' represents empty squares.
        """

        self.board = self.initial_board_state()
        self.move_log = []
        self.white_turn = True

    def __repr__(self) -> str:
        """ Current chess board state represented in unicode """
        # TODO: Print unicode chess board
        return str(self.board)

    def __len__(self) -> str:
        """ Return the total time elapsed in the game """
        pass

    @staticmethod
    def initial_board_state() -> Board:
        board = [
            [*BLACKS_STARTING_KINGS_ROW],
            [*BLACKS_STARTING_PAWN_ROW],
            [EMPTY_SQUARE for _ in range(8)],
            [EMPTY_SQUARE for _ in range(8)],
            [EMPTY_SQUARE for _ in range(8)],
            [EMPTY_SQUARE for _ in range(8)],
            [*WHITES_STARTING_PAWN_ROW],
            [*WHITES_STARTING_KINGS_ROW],
        ]

        return copy.deepcopy(board)

    @property
    def turn(self) -> str:
        """ Who's turn is it? """
        return "Whites turn" if self.white_turn else "Blacks Turn"

    @property
    def all_pieces(self) -> List[Piece]:
        """ Return a 1D list containing all active pieces on the board"""
        board = copy.deepcopy(self.board)
        flattened_board = list(chain.from_iterable(board))
        return list(filter(lambda p: isinstance(p, Piece), flattened_board))  # filter out empty squares

    @property
    def score(self) -> str:
        """ Who has the piece advantage? """
        white_pieces = list(filter(lambda p: p.color == Color.WHITE, self.all_pieces))
        black_pieces = list(filter(lambda p: p.color == Color.BLACK, self.all_pieces))

        white_score = self._get_total_piece_score(white_pieces)
        black_score = self._get_total_piece_score(black_pieces)

        result = "No player has a piece advantage, the game is even"

        if white_score > black_score:
            result = f"Whites winning with a piece advantage of ({white_score - black_score})"

        elif white_score < black_score:
            result = f"Blacks winning with a piece advantage of ({black_score - white_score})"

        return result

    @staticmethod
    def _get_total_piece_score(pieces: List[Piece]) -> int:
        """ Add up all the values for each piece """
        return reduce(lambda a, b: a + b, [p.value for p in pieces])

    @classmethod
    def is_square_empty(cls, row: int, col: int) -> bool:
        """ Checks if the square (row/col) is empty """
        if cls.board[row][col] == EMPTY_SQUARE:
            return True
        return False

    def make_move(self, move: Move) -> None:
        """ Move a piece on the chess board """
        valid_moves = self.get_valid_moves()
        if move in valid_moves:
            self._update_board_state(move=move)

            if move.is_pawn_promotion():
                promoted = move.piece_to_move.promote()
                self.board[move.dest_row][move.dest_col] = promoted
        else:
            logger.debug(f"{move} isn't a valid move. Please make a valid move")

    # TODO: Refactor
    def _update_board_state(self, move: Move) -> None:
        """ Update the boards state based on the move """
        # Makes original spot empty since we're moving the piece
        piece = move.piece_to_move

        self._make_square_empty(row=move.start_row, col=move.start_col)
        self.board[move.dest_row][move.dest_col] = piece  # Move the piece

        piece.pos = Square(row=move.dest_row, col=move.dest_col)
        piece.moves_made += 1

        logger.debug(f"Move made:{move}")
        self.move_log.append(move)
        self.white_turn = not self.white_turn

    def undo_move(self) -> None:
        """ Undo the previous move """
        if not self.move_log:
            return
        previous_move = self.move_log.pop()
        self.board[previous_move.start_row][previous_move.start_col] = previous_move.piece_to_move
        self.board[previous_move.dest_row][previous_move.dest_col] = previous_move.piece_to_capture
        self.white_turn = not self.white_turn  # Switch the turn back since we undo'd a move

    def redo_move(self) -> None:
        pass

    def reset_game(self) -> None:
        logger.debug("Reset Game")
        self.board = self.initial_board_state()
        self.move_log.clear()
        self.white_turn = True

    def get_valid_moves(self) -> List[Move]:
        """
        Generate all valid moves.
        If the user makes a move, and the game state changes, we should regenerate all moves.
        In order to validate a move, you need to generate all of the opposing color possible moves.
        If your king is safe, it is a valid move.
        """
        valid_moves = []

        if self.white_turn:
            valid_moves.extend(self._get_all_possible_moves_for_color(Color.WHITE))
        else:
            valid_moves.extend(self._get_all_possible_moves_for_color(Color.BLACK))

        return valid_moves

    def print_valid_moves(self) -> None:
        """ Print all valid moves for the current player """
        logger.debug(f"Valid Moves for {self.turn}")
        for move in self.get_valid_moves():
            logger.debug(move)

    def _get_all_possible_moves(self) -> List[Move]:
        """
        All moves without considering check
        Iterate over the entire board evaluating all pieces for the current player
        """
        moves = []
        n = len(self.board)
        for row in range(n):
            for col in range(n):
                piece = self.board[row][col]
                if piece != EMPTY_SQUARE:
                    moves.extend(piece.possible_moves(board=self.board))

        return moves

    def _get_all_possible_moves_for_color(self, color: Color) -> List[Move]:
        """ Get all possible moves for the given color (white or black) """
        return list(filter(lambda m: m.maker == color, self._get_all_possible_moves()))

    def _make_square_empty(self, row: int, col: int) -> None:
        """ Render the square empty on the given row/col"""
        self.board[row][col] = EMPTY_SQUARE

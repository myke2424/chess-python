import copy
import logging
import pygame

from typing import List
from functools import reduce
from itertools import chain

from piece import Piece, King
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
        self.time_elapsed = pygame.time.Clock()

    def __repr__(self) -> str:
        """ Current chess board state represented in unicode """
        # TODO: Print unicode chess board
        return str(self.board)

    def __len__(self) -> str:
        """ Return the total time elapsed in the game """
        return self.time_elapsed

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
    def all_pieces(self) -> List[Piece]:
        """ Return a 1D list containing all active pieces on the board"""
        board = copy.deepcopy(self.board)
        flattened_board = list(chain.from_iterable(board))
        return list(filter(lambda p: isinstance(p, Piece), flattened_board))  # filter out empty squares

    @property
    def current_color(self) -> Color:
        return Color.WHITE if self.white_turn else Color.BLACK

    @staticmethod
    def _get_total_piece_score(pieces: List[Piece]) -> int:
        """ Add up all the values for each piece """
        return reduce(lambda a, b: a + b, [p.value for p in pieces])

    def score(self) -> None:
        """ Who has the piece advantage? """
        logger.debug(f"{self.current_color} Turn")

        white_pieces = list(filter(lambda p: p.color == Color.WHITE, self.all_pieces))
        black_pieces = list(filter(lambda p: p.color == Color.BLACK, self.all_pieces))

        white_score = self._get_total_piece_score(white_pieces)
        black_score = self._get_total_piece_score(black_pieces)

        result = "No player has a piece advantage, the game is even"

        if white_score > black_score:
            result = f"Whites winning with a piece advantage of ({white_score - black_score})"

        elif white_score < black_score:
            result = f"Blacks winning with a piece advantage of ({black_score - white_score})"

        logger.debug(result)

    def king(self, color: Color) -> King:
        """ Return king object given the color """
        return list(filter(lambda p: isinstance(p, King) and p.color == color, self.all_pieces)).pop()

    def make_move(self, move: Move) -> None:
        """ Move a piece on the chess board """
        valid_moves = self.get_valid_moves()
        if move in valid_moves:
            logger.debug(f"Move made: {move}")
            self._make_move(move=move)

            if move.is_pawn_promotion():
                promoted = move.piece_to_move.promote()
                self.board[move.dest_row][move.dest_col] = promoted
        else:
            logger.debug(f"{move} isn't a valid move. Please make a valid move")

    def _make_move(self, move: Move) -> None:
        """ Make a move without validating it """
        # Makes original spot empty since we're moving the piece
        piece = move.piece_to_move

        self._make_square_empty(row=move.start_row, col=move.start_col)
        self.board[move.dest_row][move.dest_col] = piece  # Move the piece

        piece.pos = Square(row=move.dest_row, col=move.dest_col)
        piece.moves_made += 1

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

    # TODO: Improve algorithm. Naive approach generating all moves / future opponent moves
    #  probably a more efficient way to do this
    def get_valid_moves(self) -> List[Move]:
        """
        Gets all valid moves for current player.
        To validate a move, we need to do the following:
        1. Generate every possible move for the current player
        2. Make each move
        3. After each move is made, generate all opponents moves and see if our king is under attack
        4. Evaluate all opponent moves, if ANY of there moves attack your king, your original move isn't valid.
        5. Undo each move

        This algorithm is very expensive... Gotta work on it...
        """
        valid_moves = []

        # Generate all moves for the current player
        possible_moves = self._get_all_possible_moves_for_color(self.current_color)

        for current_move in possible_moves:
            is_valid_move = True
            # Make the move
            self._make_move(move=current_move)
            # Generate opponents moves (color will switch since we made a move)
            opponent_possible_moves = self._get_all_possible_moves_for_color(self.current_color)

            for opponent_move in opponent_possible_moves:
                # Since the opponent move forced a check, our current player move isn't valid.
                if opponent_move.is_check():
                    logger.debug(f"{current_move} is not VALID. {self.current_color} King in check ")
                    is_valid_move = False
                    break

            self.undo_move()

            if is_valid_move:
                valid_moves.append(current_move)

        return valid_moves

    def print_valid_moves(self) -> None:
        """ Print all valid moves for the current player """
        logger.debug(f"Valid Moves for {self.current_color}")
        for move in self.get_valid_moves():
            logger.debug(move)

    def print_move_log(self) -> None:
        logger.debug("--- MOVE LOG ---")
        for move in self.move_log:
            logger.debug(move)

    def _get_all_possible_moves(self) -> List[Move]:
        """
        Generate all possible moves for each piece
        Iterate over the entire board evaluating every pieces potential moves (zero validation done)
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

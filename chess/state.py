import copy
from typing import List

from constants import EMPTY_SQUARE
from move import Move
from piece import Color, Piece
from square import Square

from chess import (BLACKS_STARTING_KINGS_ROW, BLACKS_STARTING_PAWN_ROW,
                   WHITES_STARTING_KINGS_ROW, WHITES_STARTING_PAWN_ROW)


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
    def initial_board_state() -> List[List[str]]:
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
        return "Whites turn" if self.white_turn else "Blacks Turn"

    # TODO: Update it to work with pawn promotion/en passant
    def make_move(self, move: Move) -> None:
        """ Move a piece on the chess board """
        valid_moves = self.get_valid_moves()

        if move in valid_moves:
            self._update_board_state(move=move)

    def _update_board_state(self, move: Move) -> None:
        """ Update the boards state based on the move """
        # Makes original spot empty since we're moving the piece
        piece = move.piece_to_move

        self._make_square_empty(row=move.start_row, col=move.start_col)
        self.board[move.dest_row][move.dest_col] = piece  # Move the piece
        piece.pos = Square(row=move.dest_row, col=move.dest_col)
        piece.moves_made += 1

        print(move.dest_row, move.dest_col)
        print(move)
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
        print("Reset Game")
        self.board = self.initial_board_state()
        self.move_log.clear()
        self.white_turn = True

    # If the user makes a move, and the game state changes, we should regenerate all moves
    # In order to validate the move of a black, you need to generate all of whites possible moves.
    # Make the move, generate all possible moves the opposing player, see if any of the moves attack your king
    # If your king is safe, it is a valid move, and add it to the list, return list of valid moves
    def get_valid_moves(self):
        """ All moves considering check """
        valid_moves = []
        all_possible_moves = self.get_all_possible_moves()

        # Get whites valid moves
        if self.white_turn:
            for m in all_possible_moves:
                if m.piece_to_move.color == Color.WHITE:
                    valid_moves.append(m)
        else:
            for m in all_possible_moves:
                if m.piece_to_move.color == Color.BLACK:
                    valid_moves.append(m)
            # all_possible_moves = filter(lambda m: m.color == Color.BLACK, all_possible_moves)

        return valid_moves

    def get_all_possible_moves(self) -> List[Move]:
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

    def _make_square_empty(self, row: int, col: int) -> None:
        """ Render the square empty on the given row/col"""
        self.board[row][col] = EMPTY_SQUARE

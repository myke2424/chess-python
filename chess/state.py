from move import Move

from chess import (
    BLACKS_STARTING_KINGS_ROW,
    BLACKS_STARTING_PAWN_ROW,
    WHITES_STARTING_KINGS_ROW,
    WHITES_STARTING_PAWN_ROW,
)


class GameState:
    """
    Responsible for storing/updating all the information about the current state of the game.
    Update state (make moves), record move log, keep track of who's got the piece advantage etc."
    """

    EMPTY_SQUARE = "**"

    def __init__(self):
        """
        board: 8x8 matrix with starting chess pieces for black/white. '**' represents empty squares.
        """

        self.board = [
            [*BLACKS_STARTING_KINGS_ROW],
            [*BLACKS_STARTING_PAWN_ROW],
            [self.EMPTY_SQUARE for _ in range(8)],
            [self.EMPTY_SQUARE for _ in range(8)],
            [self.EMPTY_SQUARE for _ in range(8)],
            [self.EMPTY_SQUARE for _ in range(8)],
            [*WHITES_STARTING_PAWN_ROW],
            [*WHITES_STARTING_KINGS_ROW],
        ]

        self.move_log = []
        self.white_turn = True

    def __repr__(self) -> str:
        # TODO: Print unicode chess board
        return str(self.board)

    # TODO: Update it to work with pawn promotion/en passant
    def make_move(self, move: Move) -> None:
        """ Move a piece on the chess board """
        # Makes original spot empty since we're moving the piece
        self._make_square_empty(row=move.start_row, col=move.start_col)
        self.board[move.dest_row][move.dest_col] = move.piece_to_move  # Move the piece

        print(move)
        self.move_log.append(move)
        self.white_turn = False

        # Print the move!

    def undo_move(self):
        """ Undo the previous move """
        if not self.move_log:
            return
        previous_move = self.move_log.pop()
        self.board[previous_move.start_row][previous_move.start_col] = previous_move.piece_to_move
        self.board[previous_move.dest_row][previous_move.dest_col] = previous_move.piece_to_capture
        # TODO: Switch turn back since we undo'd a move.

    def redo_move(self):
        pass

    def _make_square_empty(self, row: int, col: int) -> None:
        """ Render the square empty on the given row/col"""
        self.board[row][col] = self.EMPTY_SQUARE

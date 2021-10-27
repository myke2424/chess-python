from move import Move


class GameState:
    """
    Responsible for storing/updating all the information about the current state of the game.
    Update state (make moves), record move log, keep track of who's got the piece advantage etc."
    """

    def __init__(self):
        """
        board: 8x8 matrix. Each cell has two characters, first char represents the color of the piece,
        second char represents the type. e.g. 'bK' = black king.
        '**' represents empty squares. Each cell has a corresponding image with the same name.
        """

        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["**", "**", "**", "**", "**", "**", "**", "**"],
            ["**", "**", "**", "**", "**", "**", "**", "**"],
            ["**", "**", "**", "**", "**", "**", "**", "**"],
            ["**", "**", "**", "**", "**", "**", "**", "**"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.move_log = []
        self.white_to_move = True

    def __repr__(self) -> str:
        # TODO: Print unicode chess board
        return str(self.board)

    # TODO: Update it to work with pawn promotion/en passant
    def make_move(self, move: Move) -> None:
        """ Move a piece on the chess board """
        # Makes original spot empty since we're moving the piece
        self._make_square_empty(row=move.start_row, col=move.start_col)
        self.board[move.dest_row][move.dest_col] = move.piece_to_move  # Move the piece
        self.move_log.append(move)
        self.white_to_move = False

    def undo_move(self):
        """ Undo the previous move """
        if not self.move_log:
            return
        previous_move = self.move_log.pop()
        self.board[previous_move.start_row][previous_move.start_col] = previous_move.piece_to_move
        self.board[previous_move.dest_row][previous_move.dest_col] = previous_move.piece_to_capture

    def _make_square_empty(self, row: int, col: int) -> None:
        """ Render the square empty on the given row/col"""
        self.board[row][col] = "**"

""" Responsible for storing all the information about the current state of the game. Determine valid moves, move log, etc."""


class GameState:
    def __init__(self):
        # Board 8x8 matrix - each cell has two characters, one representing color of the piece, second representing type
        # -- is an empty space
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.move_log = []
        self.white_to_move = True

    def make_move(self, move):
        # Take piece from starting location, move to end location
        # if self.board[move.start_row][move.start_col] != '--':
        self.board[move.start_col][move.start_col] = '--'  # Makes original spot empty since it move
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # Add to log
        self.white_to_move = not self.white_to_move  # Swap players

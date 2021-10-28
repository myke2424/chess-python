from typing import List


class Move:
    """ Abstraction that represents all the data in a player move. """

    def __init__(self, starting_square: tuple, destination_square: tuple, board: List[List[str]]):
        self.start_row = starting_square.row
        self.start_col = starting_square.col
        self.dest_row = destination_square.row
        self.dest_col = destination_square.col
        self.piece_to_move = board[self.start_row][self.start_col]
        self.piece_to_capture = board[self.dest_row][self.dest_col]  # This can be an empty square

    def __repr__(self) -> str:
        """ Printable representation of a move made in chess notation """
        starting_square_notation = _ChessNotationParser.from_row_and_col(row=self.start_row, col=self.start_col)
        destination_square_notation = _ChessNotationParser.from_row_and_col(row=self.dest_row, col=self.dest_col)

        print(self.dest_row, self.dest_col)
        return starting_square_notation + destination_square_notation

    @classmethod
    def from_chess_notation(cls, starting_square: str, destination_square: str, board: List[List[str]]) -> "Move":
        """ Alternate constructor to create a move obj from standard chess notation """
        pass


class _ChessNotationParser:
    """
    On a chess board, rows  are called RANKS (horizontal)
    On a chess board, columns are called FILES (vertical)
    A square is represented by the FILE character then RANK number
    """

    rows_to_ranks = {7: "1", 6: "2", 5: "3", 4: "4", 3: "5", 2: "6", 1: "7", 0: "8"}
    columns_to_files = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}

    @classmethod
    def from_row_and_col(cls, row: int, col: int) -> str:
        """
        Given a row/col, return its position on the board in standard chess notation
        e.g. row=7 col=0 -> a1
        row 7 would be the last row in the board matrix, but from a player perspective it would be there first row
        col 0 would be the first col of the board, columns are in alphabetical order, resulting in 'a'
        """
        chess_notation = cls.columns_to_files.get(col) + cls.rows_to_ranks.get(row)
        return chess_notation

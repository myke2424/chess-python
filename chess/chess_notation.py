from .utils import Square


class ChessNotationParser:
    """
    On a chess board, rows  are called RANKS (horizontal)
    On a chess board, columns are called FILES (vertical)
    A square is represented by the FILE character then RANK number
    """

    rows_to_ranks = {7: "1", 6: "2", 5: "3", 4: "4", 3: "5", 2: "6", 1: "7", 0: "8"}
    columns_to_files = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    ranks_to_rows = {v: k for k, v in rows_to_ranks.items()}
    files_to_columns = {v: k for k, v in columns_to_files.items()}

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

    @classmethod
    def from_notation(cls, notation: str) -> tuple:
        """ Given a chess notation, return row/col on the board """
        file, rank = notation[0], notation[1]
        return Square(cls.files_to_columns[file], cls.ranks_to_rows[rank])

from collections import namedtuple

# TODO: Fix circular dep issue with square
Square = namedtuple("Square", "row col")


class Piece:
    def __init__(self, color: str, row: int, col: int):
        self.color = color
        self.position = Square(row, col)
        self.moves_made = 0
        self.name = color + self.__class__.__name__  # name is color + piece type, e.g. bKnight

    def __repr__(self) -> str:
        """ Return the piece name and position on the board in chess notation """
        return self.__class__.__name__


class Pawn(Piece):
    value = 1

    def __init__(self, color, row, col):
        super().__init__(color=color, row=row, col=col)


class Bishop(Piece):
    value = 3

    def __init__(self, color, row, col):
        super().__init__(color=color, row=row, col=col)


class Knight(Piece):
    value = 3

    def __init__(self, color, row, col):
        super().__init__(color=color, row=row, col=col)


class Rook(Piece):
    value = 5

    def __init__(self, color, row, col):
        super().__init__(color=color, row=row, col=col)


class Queen(Piece):
    value = 9

    def __init__(self, color, row, col):
        super().__init__(color=color, row=row, col=col)


class King(Piece):
    value = 100

    def __init__(self, color, row, col):
        super().__init__(color=color, row=row, col=col)

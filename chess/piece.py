class Piece:
    def __init__(self, color: str, position):
        self.color = color
        self.position = position
        self.moves_made = 0

    def __repr__(self) -> str:
        pass


class Pawn(Piece):
    value = 1

    def __init__(self, color, position):
        super().__init__(color=color, position=position)


class Bishop(Piece):
    value = 3

    def __init__(self, color, position):
        super().__init__(color=color, position=position)


class Knight(Piece):
    value = 3

    def __init__(self, color, position):
        super().__init__(color=color, position=position)


class Rook(Piece):
    value = 5

    def __init__(self, color, position):
        super().__init__(color=color, position=position)


class Queen(Piece):
    value = 9

    def __init__(self, color, position):
        super().__init__(color=color, position=position)


class King(Piece):
    value = 100

    def __init__(self, color, position):
        super().__init__(color=color, position=position)

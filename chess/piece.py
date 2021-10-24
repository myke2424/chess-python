class Piece:
    def __init__(self, row: int, col: int, color: str):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
